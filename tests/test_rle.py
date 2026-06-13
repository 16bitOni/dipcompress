# tests/test_rle.py

from dipcompress.rle import rle_encode, rle_decode

def test_rle_basic():
    original = bytes([0, 0, 0, 0, 0, 100, 100, 50])
    encoded = rle_encode(original)
    decoded = rle_decode(encoded)
    
    assert decoded == original, "RLE must reconstruct original exactly"
    assert len(encoded) < len(original), "Should compress repeated bytes"
    print(f"Original: {len(original)} bytes")
    print(f"Encoded:  {len(encoded)} bytes")
    print(f"Ratio:    {len(encoded)/len(original):.2f}")

def test_rle_single_bytes():
    """What happens with no runs? Every byte is different."""
    original = bytes(range(50))  # [0, 1, 2, 3, ... 49]
    encoded = rle_encode(original)
    decoded = rle_decode(encoded)
    
    assert decoded == original
    # It will be 2x larger — this is expected behavior!
    print(f"No-run case: {len(original)} bytes → {len(encoded)} bytes")

def test_rle_all_same():
    """Best case: all bytes identical."""
    original = bytes([42] * 200)
    encoded = rle_encode(original)
    decoded = rle_decode(encoded)
    
    assert decoded == original
    assert len(encoded) == 2, f"Got {len(encoded)} bytes, expected 2"
    print(f"All-same: {len(original)} bytes → {len(encoded)} bytes")

if __name__ == "__main__":
    test_rle_basic()
    test_rle_single_bytes()
    test_rle_all_same()