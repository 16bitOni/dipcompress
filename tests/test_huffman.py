# tests/test_huffman.py

from dipcompress.huffman import huffman_encode, huffman_decode, build_huffman_tree, build_code_table

def test_huffman_roundtrip():
    original = b"AAAAABBBCCDDDDDEEEE"
    
    encoded, meta = huffman_encode(original)
    recovered = huffman_decode(encoded, meta)
    
    assert recovered == original
    ratio = len(encoded) / len(original)
    print(f"Original:  {len(original)} bytes")
    print(f"Encoded:   {len(encoded)} bytes (ratio {ratio:.2f})")
    
    # Print the codes to see what it did
    print("\nHuffman codes:")
    codes = meta['codes']
    for byte_val, code in sorted(codes.items(), key=lambda x: len(x[1])):
        print(f"  {chr(byte_val) if 32 <= byte_val <= 126 else byte_val:4} → {code}")

def test_huffman_lorem():
    """Test on English-like text where E is most common."""
    original = b"the quick brown fox jumps over the lazy dog the end"
    
    encoded, meta = huffman_encode(original)
    recovered = huffman_decode(encoded, meta)
    
    assert recovered == original
    codes = meta['codes']
    
    # 'e' should get a shorter code than 'q' (more common)
    e_code = codes[ord('e')]
    q_code = codes[ord('q')]
    print(f"\n'e' code: {e_code} (length {len(e_code)})")
    print(f"'q' code: {q_code} (length {len(q_code)})")
    assert len(e_code) <= len(q_code), "Common letters should have shorter codes"

if __name__ == "__main__":
    test_huffman_roundtrip()
    test_huffman_lorem()