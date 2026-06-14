# tests/test_lz77.py

from dipcompress.lz77 import lz77_encode, lz77_decode, tokens_to_bytes, bytes_to_tokens

def test_lz77_roundtrip():
    """Can we compress and decompress back to identical data?"""
    original = b"abcdefabcdefabcdef this is a test of the lz77 algorithm"
    
    tokens = lz77_encode(original)
    recovered = lz77_decode(tokens)
    
    assert recovered == original, f"Mismatch!\nOriginal: {original}\nGot:      {recovered}"
    
    # Measure
    serialized = tokens_to_bytes(tokens)
    ratio = len(serialized) / len(original)
    print(f"Original:  {len(original)} bytes")
    print(f"Tokens:    {len(tokens)} tokens")
    print(f"Serialized: {len(serialized)} bytes")
    print(f"Ratio:     {ratio:.2f}")

def test_lz77_repetitive():
    """Test with very repetitive data — LZ77 should excel here."""
    original = b"AAABBBAAABBBAAABBB" * 10
    
    tokens = lz77_encode(original)
    recovered = lz77_decode(tokens)
    
    assert recovered == original
    serialized = tokens_to_bytes(tokens)
    ratio = len(serialized) / len(original)
    print(f"\nRepetitive data: {len(original)} bytes → {len(serialized)} bytes (ratio {ratio:.2f})")
    assert ratio < 0.5, "LZ77 should compress repetitive data significantly"

def test_token_serialization():
    """Tokens must survive serialize → deserialize."""
    original = b"hello world, hello world again and again and again"
    
    tokens = lz77_encode(original)
    serialized = tokens_to_bytes(tokens)
    recovered_tokens = bytes_to_tokens(serialized)
    recovered = lz77_decode(recovered_tokens)
    
    assert recovered == original, "Full pipeline failed"
    print("\n✓ LZ77 token serialization roundtrip works")

if __name__ == "__main__":
    test_lz77_roundtrip()
    test_lz77_repetitive()
    test_token_serialization()