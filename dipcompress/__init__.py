# dipcompress/__init__.py
# This is what users see when they do: import dipcompress

__version__ = "0.1.1"
__author__ = "Subhadip"

from .encoder import compress
from .decoder import decompress
from .image_io import load_image, save_image, pixels_to_bytes, bytes_to_pixels
from .rle import rle_encode, rle_decode

__all__ = ["compress", "decompress", "load_image", "save_image", "pixels_to_bytes", "bytes_to_pixels", "rle_encode", "rle_decode"]