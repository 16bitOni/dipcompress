import struct
from dataclasses import dataclass
from typing import Optional

MAGIC = b'DIP\x01'
VERSION = 1

COMPRESS_RLE = 0X01
COMPRESS_DEFLATE = 0X02

HEADER_FORMAT = '>4sHIIBBI'

HEADER_SIZE = struct.calcsize(HEADER_FORMAT)

@dataclass
class DipHeader:
    width: int
    height: int
    channels: int
    compression_mode:int
    compressed_length: int
    version: int = VERSION

    def to_bytes(self) -> bytes:
        return struct.pack(
           HEADER_FORMAT,
            MAGIC,
            self.version,
            self.width,
            self.height,
            self.channels,
            self.compression_mode,
            self.compressed_length
        )
    
    @staticmethod
    def from_bytes(data: bytes)->'DipHeader':
        magic,version,width,height,channels,mode,comp_len = struct.unpack(
            HEADER_FORMAT, data[:HEADER_SIZE]
        )
        if magic != MAGIC:
            raise ValueError(f"Not a DipCompress file! Magic: {magic}")
        return DipHeader(
            width=width,
            height=height,
            channels=channels,
            compression_mode=mode,
            compressed_length=comp_len,
            version=version
        )


def encode_filter_table(filter_types: list[int]) -> bytes:
    return bytes(filter_types)


def decode_filter_table(data: bytes) -> list[int]:
    return list(data)


def encode_huffman_table(codes: dict, original_length: int, padding: int) -> bytes:
    entries = []
    entries.append(struct.pack('>IB', original_length, padding))  # 4 bytes length + 1 byte padding
    entries.append(struct.pack('>H', len(codes)))  # Number of entries

    for symbol, code_str in sorted(codes.items()):
        code_len = len(code_str)
        padded = code_str.ljust((code_len + 7) // 8 * 8, '0')
        code_bytes = bytes(int(padded[i:i+8], 2) for i in range(0, len(padded), 8))

        entries.append(struct.pack('BB', symbol, code_len))
        entries.append(code_bytes)

    return b''.join(entries)


def decode_huffman_table(data: bytes) -> tuple[dict, int, int, int]:
    pos = 0
    original_length, padding = struct.unpack('>IB', data[pos:pos+5])
    pos += 5

    num_entries = struct.unpack('>H', data[pos:pos+2])[0]
    pos += 2

    codes = {}
    for _ in range(num_entries):
        symbol, code_len = struct.unpack('BB', data[pos:pos+2])
        pos += 2

        num_bytes = (code_len + 7) // 8
        code_bytes = data[pos:pos+num_bytes]
        pos += num_bytes

        full_bits = ''.join(f'{b:08b}' for b in code_bytes)
        code_str = full_bits[:code_len]

        codes[symbol] = code_str

    return codes, original_length, padding, pos