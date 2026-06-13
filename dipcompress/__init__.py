# dipcompress/__init__.py
# This is what users see when they do: import dipcompress

__version__ = "0.1.0"
__author__ = "Subhadip"

from .encoder import compress
from .decoder import decompress

__all__ = ["compress", "decompress"]