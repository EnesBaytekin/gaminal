"""
Pygaminal game builder — compiles game projects into standalone executables
with PyInstaller (--onefile). All assets, scripts, and the framework itself
are bundled into a single binary.
"""

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

# Built-in components from pygaminal.components that are loaded dynamically
# and won't be discovered by PyInstaller's static analysis.
BUILTIN_COMPONENTS = [
    "pygaminal.components.Animation",
    "pygaminal.components.BackgroundMusic",
    "pygaminal.components.Hitbox",
    "pygaminal.components.Image",
    "pygaminal.components.Movability",
    "pygaminal.components.SoundEffect",
    "pygaminal.components.YSort",
]


def find_game_files(game_dir):
    """
    Scan *game_dir* and return (hidden_imports, data_files).

    *hidden_imports* — module names for every ``.py`` file (except *main.py*)
    that the framework loads via ``importlib.import_module()`` at runtime.
    *data_files* — (source, dest) pairs for PyInstaller ``--add-data``,
    covering every non-Python asset (images, sounds, JSON, …) as well as
    the ``.py`` files themselves as a fallback.
    """
    game_dir = Path(game_dir).resolve()
    hidden_imports = []
    data_entries = []

    for root, dirs, files in os.walk(game_dir):
        rel_root = Path(root).relative_to(game_dir)

        # Skip hidden / cache / venv dirs.
        skip = any(
            part.startswith(".") or part in ("__pycache__",)
            for part in rel_root.parts
        )
        if skip:
            continue

        for name in files:
            full = Path(root) / name
            rel = full.relative_to(game_dir)

            if name.endswith(".py"):
                mod = str(rel.with_suffix("")).replace(os.sep, ".")
                if name != "main.py":
                    hidden_imports.append(mod)
                # Include .py as data too, so they exist on disk at runtime.
                data_entries.append((str(full), str(rel.parent)))
            else:
                data_entries.append((str(full), str(rel.parent)))

    return hidden_imports, data_entries


def _launcher_source(scene_files):
    """Return the Python source of the bootstrapper script.

    The bootstrapper handles the ``sys._MEIPASS`` → ``chdir`` dance that
    PyInstaller one-file builds require, then calls ``run_app()``.
    """
    scene_args = ", ".join(repr(s) for s in scene_files)
    return f'''"""Pygaminal game launcher (compiled)."""
import sys
import os

# Tell pygaminal.__init__ to skip change_dir_to_main_dir() — in a
# PyInstaller bundle sys.argv[0] points at the exe, but the data files
# live under sys._MEIPASS, so the normal CWD change would break file
# resolution.
os.environ["_PYGAMINAL_BUILD"] = "1"

# In a PyInstaller --onefile build the exe extracts itself to a temp
# directory (sys._MEIPASS).  Data files live there, so we switch to it
# before the game tries to open relative paths.
if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
    os.chdir(sys._MEIPASS)
    if sys._MEIPASS not in sys.path:
        sys.path.insert(0, sys._MEIPASS)

import pygaminal  # noqa: E402

# Launch the game.
pygaminal.run_app({scene_args})
'''


def _detect_scene_files(game_dir):
    """Return a list of scene files passed to ``run_app()`` in *main.py*.

    Falls back to all ``.json`` files in the root of *game_dir*.
    """
    main_py = Path(game_dir).resolve() / "main.py"
    if not main_py.exists():
        return []

    content = main_py.read_text(encoding="utf-8")
    m = re.search(r"run_app\s*\(([^)]+)\)", content)
    if m:
        parts = [a.strip().strip("\"'") for a in m.group(1).split(",")]
        return [p for p in parts if p]

    # Fallback: any .json at the root.
    return sorted(p.name for p in Path(game_dir).glob("*.json"))


def build(
    game_dir,
    output_dir=None,
    name=None,
    console=True,
):
    """Build a game project into a standalone executable.

    Parameters
    ----------
    game_dir : str or Path
        Path to the game project (must contain *main.py*).
    output_dir : str or Path | None
        Where to put the finished binary.  Defaults to *game_dir*/build.
    name : str | None
        Executable name.  Defaults to the game directory's basename.
    console : bool
        Pass ``--noconsole`` on Windows (no terminal window).  Ignored on
        Linux / macOS where the flag is meaningless.  (Kept for cross-plat.)
    """
    game_dir = Path(game_dir).resolve()
    if not game_dir.is_dir():
        raise NotADirectoryError(f"Not a directory: {game_dir}")

    main_py = game_dir / "main.py"
    if not main_py.exists():
        raise FileNotFoundError(f"No main.py found in {game_dir}")

    if output_dir is None:
        output_dir = game_dir / "build"
    output_dir = Path(output_dir)

    if name is None:
        name = game_dir.name

    # ---------------------------------------------------------------
    # 1.  Analyse the game project
    # ---------------------------------------------------------------
    scene_files = _detect_scene_files(game_dir)
    if not scene_files:
        raise RuntimeError(
            "Could not detect scene files.  "
            "Make sure main.py calls run_app('filename.json') "
            "or place a .json file in the game directory."
        )

    print(f"[*] Scanning {game_dir} …")
    hidden_imports, data_entries = find_game_files(game_dir)
    print(f"    → {len(hidden_imports)} dynamic script(s), "
          f"{len(data_entries)} data file(s)")

    # ---------------------------------------------------------------
    # 2.  Write the bootstrapper entry-point
    # ---------------------------------------------------------------
    launcher = game_dir / "__pyg_launcher__.py"
    launcher.write_text(_launcher_source(scene_files), encoding="utf-8")

    # ---------------------------------------------------------------
    # 3.  Build the PyInstaller command
    # ---------------------------------------------------------------
    sep = ";" if sys.platform == "win32" else ":"
    cache_dir = game_dir / ".pyinstaller_cache"

    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--clean",
        "--distpath", str(output_dir),
        "--workpath", str(cache_dir),
        "--specpath", str(cache_dir),
        "--name", name,
        "--paths", str(game_dir),
    ]

    # Add pygaminal's *parent* directory so PyInstaller can resolve
    # --hidden-import pygaminal.components.Animation etc.
    # (PyInstaller needs the path that *contains* the pygaminal/ package,
    # not the package directory itself.)
    pygaminal_root = Path(__file__).parent.parent
    cmd += ["--paths", str(pygaminal_root)]

    if not console:
        cmd.append("--noconsole")

    # Hidden imports: built-in dynamic components
    for mod in BUILTIN_COMPONENTS:
        cmd += ["--hidden-import", mod]

    # Hidden imports: user scripts loaded via importlib
    for mod in hidden_imports:
        cmd += ["--hidden-import", mod]

    # Data files (everything except main.py's source)
    for src, dst in data_entries:
        cmd += ["--add-data", f"{src}{sep}{dst}"]

    # Entry point
    cmd.append(str(launcher))

    # ---------------------------------------------------------------
    # 4.  Run PyInstaller
    # ---------------------------------------------------------------
    print("[*] Running PyInstaller …")
    result = subprocess.run(cmd, cwd=str(game_dir))

    if result.returncode != 0:
        raise RuntimeError("PyInstaller build failed — see output above.")

    # ---------------------------------------------------------------
    # 5.  Strip the output dir to *only* the final executable
    # ---------------------------------------------------------------
    print("[*] Cleaning up build artifacts …")

    # Remove PyInstaller cache
    if cache_dir.is_dir():
        shutil.rmtree(cache_dir)

    # Remove the temporary launcher
    launcher.unlink(missing_ok=True)

    # Remove .spec file (it lands at game_dir root, not in cache)
    spec = game_dir / f"{name}.spec"
    spec.unlink(missing_ok=True)

    # Anything in output_dir that isn't the executable goes away.
    exe_name = f"{name}.exe" if sys.platform == "win32" else name
    for item in output_dir.iterdir():
        if item.name != exe_name:
            if item.is_dir():
                shutil.rmtree(item)
            else:
                item.unlink()

    exe_path = output_dir / exe_name
    print(f"\n✅ Build complete: {exe_path}")
    return exe_path
