# tests/test_image_io.py

from dipcompress.image_io import load_image, save_image, pixels_to_bytes, bytes_to_pixels
import numpy as np

def test_image_roundtrip():
    """Can we turn an image into bytes and back perfectly?"""
    from PIL import Image
    
    # Create a tiny test image — 4x4 grayscale
    test_pixels = np.array([
        [0,   64,  128, 192],
        [255, 200, 100, 50 ],
        [10,  20,  30,  40 ],
        [100, 100, 100, 100],
    ], dtype=np.uint8)
    
    # Convert to bytes
    raw_bytes = pixels_to_bytes(test_pixels)
    assert len(raw_bytes) == 16  # 4x4 = 16 bytes for grayscale
    
    # Convert back
    recovered = bytes_to_pixels(raw_bytes, width=4, height=4, channels=1)
    
    # Must be identical
    assert np.array_equal(test_pixels, recovered), "Pixel roundtrip failed!"
    print("✓ Image IO works — pixels survive the bytes trip intact")

if __name__ == "__main__":
    test_image_roundtrip()