"""
Build the lz77_cext Python extension module.

Usage (run from the repo root):
    python dipcompress/_c_ext/build.py

Output: dipcompress/lz77_cext.<platform-tag>.pyd  (Windows)
        dipcompress/lz77_cext.<platform-tag>.so   (Linux/macOS)

The built module is placed in-place inside the dipcompress package so that
`from dipcompress import lz77_cext` works immediately without installation.
"""
import os
import sys
from pathlib import Path

# Run from the repo root so setuptools resolves relative source paths correctly.
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
os.chdir(REPO_ROOT)


def build():
    from setuptools import Extension
    from setuptools.dist import Distribution
    from setuptools.command.build_ext import build_ext

    ext = Extension(
        'dipcompress.lz77_cext',
        sources=['dipcompress/_c_ext/compress.c'],
    )

    dist = Distribution(attrs={'ext_modules': [ext]})
    cmd  = build_ext(dist)
    cmd.inplace = True          # place .pyd/.so next to the package source
    cmd.ensure_finalized()
    cmd.run()

    print('\nBuild complete — lz77_cext is ready.')


if __name__ == '__main__':
    build()
