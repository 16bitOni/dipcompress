from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext


class OptionalBuildExt(build_ext):
    """Build the C extension, but don't fail the whole install if it errors.
    The pure-Python fallback in lz77_fast.py handles the missing extension."""

    def build_extension(self, ext):
        try:
            super().build_extension(ext)
        except Exception as e:
            print(f"\nWARNING: could not build C extension '{ext.name}': {e}")
            print("         dipcompress will run in pure-Python mode (slower).\n")


setup(
    ext_modules=[
        Extension(
            'dipcompress.lz77_cext',
            sources=['dipcompress/_c_ext/compress.c'],
        )
    ],
    cmdclass={'build_ext': OptionalBuildExt},
)
