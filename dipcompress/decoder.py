# dipcompress/decoder.py

import numpy as np
from .image_io import save_image, bytes_to_pixels
from .filters import remove_filters
from .lz77 import bytes_to_tokens, lz77_decode
from .huffman import huffman_decode
from .format import DipHeader, HEADER_SIZE, decode_filter_table, decode_huffman_table


def decompress(input_path: str, output_path: str, verbose: bool = False) -> None:
    """
    Decompress a .dip file back to an image.
    
    Args:
        input_path: path to the .dip file
        output_path: path to write the reconstructed image (PNG recommended)
        verbose: print progress information
    """
    with open(input_path, 'rb') as f:
        raw = f.read()
    
    # Step 1: Parse header
    if verbose: print("Parsing header...")
    header = DipHeader.from_bytes(raw)
    pos = HEADER_SIZE
    
    width = header.width
    height = header.height
    channels = header.channels
    
    # Step 2: Read filter table (one byte per row)
    filter_types = decode_filter_table(raw[pos:pos+height])
    pos += height
    
    # Step 3: Read and parse Huffman table from payload
    if verbose: print("Reading Huffman table...")
    payload = raw[pos:]
    codes, original_length, padding, table_size = decode_huffman_table(payload)

    huffman_compressed = payload[table_size:]

    # Step 4: Huffman decode
    if verbose: print("Huffman decoding...")
    huffman_meta = {
        'codes': codes,
        'original_length': original_length,
        'padding': padding,
    }
    lz77_bytes = huffman_decode(huffman_compressed, huffman_meta)
    
    if verbose: print("LZ77 decoding...")
    lz77_tokens = bytes_to_tokens(lz77_bytes)
    filtered_data = lz77_decode(lz77_tokens)
    
    if verbose: print("Removing filters...")
    row_width = width * channels
    filtered_rows_data = [
        (ft, filtered_data[i*row_width:(i+1)*row_width])
        for i, ft in enumerate(filter_types)
    ]
    pixels = remove_filters(filtered_rows_data, width, channels)
    
    mode = {1: 'L', 3: 'RGB', 4: 'RGBA'}.get(channels, 'RGB')
    save_image(pixels, output_path, mode=mode)
    
    if verbose:
        print(f"\n✓ Decompression complete!")
        print(f"  Image: {width}x{height} {mode}")
        print(f"  Saved to: {output_path}")