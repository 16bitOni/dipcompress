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

def build_code_table(root: HffNode) -> Dict[int, str]:
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





