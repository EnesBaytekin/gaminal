"""
``pygaminal-build`` console-script entry point (standalone module).

This module lives *outside* the ``pygaminal/`` package so that its
module-level code (env-var setup) runs **before** any pygaminal or
pygame import — something a submodule of the package cannot do.
"""

import os
import sys

# ── Must run *before* any pygaminal / pygame import ──────────────
os.environ.setdefault("_PYGAMINAL_BUILD", "1")
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")

import argparse
from pathlib import Path

from pygaminal.builder import build


def _resolve_dir(raw):
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
