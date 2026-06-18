import heapq
from collections import Counter
from dataclasses import dataclass, field
from typing import Dict, Optional


@dataclass(order=True)
class HuffNode:
    freq:int
    symbol: Optional[str] = field(default=None, compare = False)
    left: Optional['HuffNode'] = field(default=None, compare=False)
    right: Optional['HuffNode'] = field(default=None, compare=False)


    def is_leaf(self) -> bool:
        return self.left is None and self.right is None
    

def build_huffman_tree(data: bytes) -> HuffNode:
    freqs = Counter(data)

    if len(freqs) ==1:
        symbol,freq = list(freqs.items())[0]
        return HuffNode(freq, symbol)
    
    heap=[]

    for symbol,freq in freqs.items():
        heapq.heappush(heap, HuffNode(freq=freq, symbol=symbol))

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)

        merged = HuffNode(
            freq = left.freq + right.freq,
            symbol = None,
            left = left,
            right = right
        )

        heapq.heappush(heap, merged)
    return heap[0]

def build_code_table(root: HuffNode) -> Dict[int, str]:
    codes = {}

    def walk(node: HuffNode, code: str):
        if node.is_leaf():
            codes[node.symbol] = code if code else '0'
            return
        
        if node.left:
            walk(node.left, code + '0')
        if node.right:
            walk(node.right, code + '1')

    walk(root, '')
    return codes

def huffman_encode(data: bytes) -> tuple[bytes,dict]:
    if not data:
        return b'', {}
    
    root = build_huffman_tree(data)
    codes = build_code_table(root)

    bit_string = ''.join(codes[byte] for byte in data)
    
    padding = (8-len(bit_string) % 8) % 8

    bit_string += '0' * padding


    encoded = bytearray()

    for i in range(0, len(bit_string), 8):
        byte_chunk = bit_string[i:i+8]
        encoded.append(int(byte_chunk, 2))

    metadata = {
        'codes': codes,
        'original_length': len(data),
        'padding': padding
    }


    return bytes(encoded), metadata



def huffman_decode(encoded:bytes, metadta: dict) -> bytes:
    if not encoded:
        return b""
    
    codes = metadta['codes']
    original_length = metadta['original_length']
    padding = metadta['padding']

    bit_string = ''.join(f'{byte:08b}' for byte in encoded)

    if padding:
        bit_string = bit_string[:-padding]

    reverse_codes = {v:k for k,v in codes.items()}

    output = []
    current = ''
    for bit in bit_string:
        current += bit
        if current in reverse_codes:
            output.append(reverse_codes[current])
            current = ''

        if len(output) == original_length:
            break

    return bytes(output)




