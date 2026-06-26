"""
Pygaminal CLI — ``pygaminal-build`` command-line tool.

Usage
-----
    pygaminal-build [OPTIONS] [GAME_DIR]

Build the game project at *GAME_DIR* (default: current directory) into a
standalone executable via PyInstaller.
"""

import argparse
import os
import sys
from pathlib import Path

# ── Suppress side effects ─────────────────────────────────────────────
# These env vars must be set *before* any pygaminal / pygame import so
# that the build tool doesn't print the pygame banner or change the CWD
# at import time.
os.environ.setdefault("_PYGAMINAL_BUILD", "1")
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")

from pygaminal.builder import build  # noqa: E402


def _resolve_dir(raw):
    """Return a resolved Path, or ``None`` if it doesn't exist."""
    p = Path(raw).resolve()
    return p if p.is_dir() else None


def main():
    parser = argparse.ArgumentParser(
        prog="pygaminal-build",
        description="Build a Pygaminal game project into a single executable.",
    )
    parser.add_argument(
        "game_dir",
        nargs="?",
        default=".",
        type=_resolve_dir,
        help="Path to the game project directory (default: current dir).",
    )
    parser.add_argument(
        "-o", "--output-dir",
        default=None,
        help="Where to place the binary (default: GAME_DIR/build).",
    )
    parser.add_argument(
        "-n", "--name",
        default=None,
        help="Executable name (default: the game directory name).",
    )
    parser.add_argument(
        "--console",
        action="store_true",
        default=True,
        help="Show a terminal/console window (Windows only; default).",
    )
    parser.add_argument(
        "--no-console",
        action="store_false",
        dest="console",
        help="Hide the console window (Windows only).",
    )

    args = parser.parse_args()

    if args.game_dir is None:
        print(f"Error: directory not found: {sys.argv[1]}", file=sys.stderr)
        sys.exit(1)

    try:
        build(
            game_dir=args.game_dir,
            output_dir=args.output_dir,
            name=args.name,
            console=args.console,
        )
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
