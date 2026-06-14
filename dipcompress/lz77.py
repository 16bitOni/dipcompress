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
             next_byte = data[next_pos] if next_pos <len(data) else 0

             tokens.append(LZ77Token(distance=best_distance, length=best_length, next_byte=next_byte))
             pos += best_length + 1
        else:
            tokens.append(LZ77Token(distance=0, length=0, next_byte=data[pos]))
            pos += 1
    return tokens
