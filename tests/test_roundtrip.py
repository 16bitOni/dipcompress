# tests/test_roundtrip.py

"""
THE most important test: compress an image, decompress it, 
confirm every single pixel is identical to the original.
This is the proof that DipCompress works.
"""

import numpy as np
from PIL import Image
import tempfile
import os
from dipcompress import compress, decompress

def create_test_image(width: int, height: int, mode: str = 'L') -> str:
    """Create a synthetic test image and save it. Returns path."""
    if mode == 'L':
        # Grayscale gradient with some noise
        data = np.zeros((height, width), dtype=np.uint8)
        for y in range(height):
            for x in range(width):
                data[y, x] = (x * 255 // width + y * 128 // height) % 256
    else:
        # RGB — different gradient per channel
        data = np.zeros((height, width, 3), dtype=np.uint8)
        for y in range(height):
            for x in range(width):
                data[y, x, 0] = (x * 255 // width) % 256           # Red
                data[y, x, 1] = (y * 255 // height) % 256          # Green
                data[y, x, 2] = ((x + y) * 128 // (width+height)) % 256  # Blue
    
    path = tempfile.mktemp(suffix='.png')
    Image.fromarray(data, mode=mode).save(path)
    return path, data


def test_roundtrip_grayscale():
    """Compress and decompress a grayscale image — pixels must be identical."""
    original_path, original_pixels = create_test_image(64, 64, 'L')
    compressed_path = tempfile.mktemp(suffix='.dip')
    recovered_path  = tempfile.mktemp(suffix='.png')
    
    try:
        stats = compress(original_path, compressed_path, verbose=True)
        decompress(compressed_path, recovered_path, verbose=True)
        
        recovered_pixels = np.array(Image.open(recovered_path))
        
        if np.array_equal(original_pixels, recovered_pixels):
            print(f"\n✓✓✓ PERFECT ROUNDTRIP — every pixel matches!")
        else:
            diff = np.abs(original_pixels.astype(int) - recovered_pixels.astype(int))
            print(f"✗ Pixels differ! Max diff: {diff.max()}, Mean diff: {diff.mean():.4f}")
            assert False, "Roundtrip failed"
        
        print(f"\nStats: {stats}")
    
    finally:
        for p in [original_path, compressed_path, recovered_path]:
            if os.path.exists(p): os.remove(p)


if __name__ == "__main__":
    test_roundtrip_grayscale()