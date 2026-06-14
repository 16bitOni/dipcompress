from dataclasses import dataclass
from typing import List


@dataclass
class LZ77Token:
    distance: int
    length: int
    next_byte: int


    def is_literal(self) -> bool:
        return self.distance == 0 and self.length ==0
    

WINDOW_SIZE = 4096
LOOKAHEAD = 18

def lz77_encode(data: bytes)->List[LZ77Token]:

    tokens = []
    pos = 0

    while pos<len(data):

        window_start  =  max(0,pos-WINDOW_SIZE)
        window = data[window_start:pos]

        lookahead_end = min(pos+LOOKAHEAD, len(data))
        lookahead = data[pos:lookahead_end]

        best_distance = 0
        best_length = 0

        for i in range(len(window)):
            match_length = 0

            while (match_length) < len(lookahead) and i+match_length < len(window) and window[i+match_length] == lookahead[match_length]:
                match_length += 1

            if match_length > best_length:
                best_length = match_length
                best_distance = len(window) - i

        if best_length >= 3:
             next_pos = pos + best_length
             if next_pos >= len(data):
                 best_length -= 1
                 next_pos -= 1
             next_byte = data[next_pos]

             tokens.append(LZ77Token(distance=best_distance, length=best_length, next_byte=next_byte))
             pos += best_length + 1
        else:
            tokens.append(LZ77Token(distance=0, length=0, next_byte=data[pos]))
            pos += 1
    return tokens

def lz77_decode(tokens: List[LZ77Token]) -> bytes:

    output = bytearray()
    
    for token in tokens:
        if token.is_literal():
            output.append(token.next_byte)
        else:
            start = len(output) - token.distance
            
            for i in range(token.length):
                output.append(output[start + i])
            
            output.append(token.next_byte)
    
    return bytes(output)

def tokens_to_bytes(tokens: List[LZ77Token]) -> bytes:
   
    output = []
    for token in tokens:
        output.append((token.distance >> 8) & 0xFF)  
        output.append(token.distance & 0xFF)         
        output.append(token.length)
        output.append(token.next_byte)
    return bytes(output)


def bytes_to_tokens(data: bytes) -> List[LZ77Token]:
    
    tokens = []
    i = 0
    while i + 3 < len(data):
        distance = (data[i] << 8) | data[i+1]
        length = data[i+2]
        next_byte = data[i+3]
        tokens.append(LZ77Token(distance, length, next_byte))
        i += 4
    return tokens
