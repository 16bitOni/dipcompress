# dipcompress/rle.py

def rle_encode(data: bytes) -> bytes:

    if not data:
        return b""
    
    output = []
    
    i = 0
    while i < len(data):
        current_byte = data[i]
        count = 1
        
        while i + count < len(data) and data[i + count] == current_byte and count < 255:
            count += 1
        
        output.append(count)
        output.append(current_byte)
        
        i += count
    
    return bytes(output)


def rle_decode(data: bytes) -> bytes:
    
    if not data:
        return b""
    
    output = []
    
    i = 0
    while i < len(data):
        count = data[i]
        value = data[i + 1]
        
        output.extend([value] * count)
        
        i += 2
    
    return bytes(output)


def rle_compression_ratio(original: bytes) -> float:
    
    encoded = rle_encode(original)
    return len(encoded) / len(original)