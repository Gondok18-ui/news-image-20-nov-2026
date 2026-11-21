#!/usr/bin/env python3
"""Entry program for make.fun's "Sum up 20 November's world news in one
image" bounty.

The artwork (entry.png, drawn by draw.py) sits beside this file; the program
copies it, byte for byte, to entry.png in the output directory. It uses only
the standard library, needs no network, and is deterministic: every run
writes exactly the same bytes.
"""
import os
import shutil
from pathlib import Path


def find_image() -> Path:
    here = Path(__file__).resolve().parent
    for candidate in (here / 'entry.png', Path('/bot/entry.png'), Path.cwd() / 'entry.png'):
        if candidate.is_file():
            return candidate
    raise FileNotFoundError('entry.png not found next to main.py')


def main() -> None:
    out_dir = Path(os.environ.get('MAKEFUN_OUTPUT_DIR', '/output'))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / 'entry.png'
    shutil.copyfile(find_image(), target)
    print('wrote', target, target.stat().st_size, 'bytes')


if __name__ == '__main__':
    main()
