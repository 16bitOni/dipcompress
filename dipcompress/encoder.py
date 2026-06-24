# dipcompress/encoder.py

import numpy as np
from .image_io import load_image, pixels_to_bytes
from .filters import apply_filters
from .lz77_fast import lz77_encode, using_c as _lz77_using_c
from .lz77 import tokens_to_bytes
from .huffman import huffman_encode
from .format import DipHeader, COMPRESS_DEFLATE, encode_filter_table, encode_huffman_table


def compress(input_path: str, output_path: str, verbose: bool = False) -> dict:
    """
    Compress an image file to .dip format.
    
    Args:
        input_path: path to PNG/JPEG/any PIL-supported image
        output_path: path to write the .dip file
        verbose: print progress information
    
    Returns:
        dict with compression statistics
    """

    if verbose: print(f"Loading {input_path}...")
    pixels, meta = load_image(input_path)
    width = meta['width']
    height = meta['height']
    channels = meta['channels']
    original_size = width * height * channels
    
    if verbose: print("Applying filters...")
    filtered_rows = apply_filters(pixels)
    filter_types = [ft for ft, _ in filtered_rows]
    filtered_data = b''.join(row for _, row in filtered_rows)
    
    if verbose:
        backend = "C" if _lz77_using_c else "Python"
        print(f"Running LZ77 ({backend})...")
    lz77_tokens = lz77_encode(filtered_data)
    lz77_bytes = tokens_to_bytes(lz77_tokens)
    
    if verbose: print("Running Huffman coding...")
    huffman_compressed, huffman_meta = huffman_encode(lz77_bytes)
    codes = huffman_meta['codes']
    original_length = huffman_meta['original_length']
    padding = huffman_meta['padding']

    if verbose: print("Assembling .dip file...")

    filter_table_bytes = encode_filter_table(filter_types)
    huffman_table_bytes = encode_huffman_table(codes, original_length, padding)
    
    payload = huffman_table_bytes + huffman_compressed
    
    header = DipHeader(
        width=width,
        height=height,
        channels=channels,
        compression_mode=COMPRESS_DEFLATE,
        compressed_length=len(payload)
    )
    
    with open(output_path, 'wb') as f:
        f.write(header.to_bytes())
        f.write(filter_table_bytes)  
        f.write(payload)
    
    compressed_size = header.to_bytes().__len__() + len(filter_table_bytes) + len(payload)
    
    stats = {
        'original_size': original_size,
        'compressed_size': compressed_size,
        'ratio': compressed_size / original_size,
        'savings_pct': (1 - compressed_size / original_size) * 100,
        'width': width,
        'height': height,
        'channels': channels,
        'filter_stats': _count_filters(filter_types),
    }
    
    if verbose:
        print(f"\n✓ Compression complete!")
        print(f"  Original:   {original_size:,} bytes ({original_size/1024:.1f} KB)")
        print(f"  Compressed: {compressed_size:,} bytes ({compressed_size/1024:.1f} KB)")
        print(f"  Ratio:      {stats['ratio']:.3f} ({stats['savings_pct']:.1f}% smaller)")
    
    return stats


def _count_filters(filter_types: list) -> dict:
    from collections import Counter
    filter_names = {0: 'None', 1: 'Sub', 2: 'Up', 3: 'Average', 4: 'Paeth'}
    counts = Counter(filter_types)
    return {filter_names.get(k, k): v for k, v in counts.items()}