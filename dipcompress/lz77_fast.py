"""
LZ77 encode wrapper — uses the compiled C extension when available,
falls back to the pure-Python implementation transparently.

To build the C extension:
    python dipcompress/_c_ext/build.py
"""
from typing import List

from .lz77 import LZ77Token, bytes_to_tokens, lz77_encode as _py_encode

try:
    from . import lz77_cext as _cext
    using_c = True
except ImportError:
    _cext   = None
    using_c = False


def lz77_encode(data: bytes) -> List[LZ77Token]:
    if _cext is None:
        return _py_encode(data)
    return bytes_to_tokens(_cext.lz77_encode(data))
