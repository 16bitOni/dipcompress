import numpy as np

def filter_sub(row: bytes) -> bytes:

    row_arr = list(row)
    result = [row_arr[0]]
    for i in range(1,len(row_arr)):
        result.append((row_arr[i] - row_arr[i-1]) % 256)
    return bytes(result)

def unfilter_sub(row: bytes) -> bytes:

    row_arr = list(row)
    result = [row_arr[0]]
    for i in range(1,len(row_arr)):
        result.append((row_arr[i] + result[i-1]) % 256)
    return bytes(result)

def filter_up(row: bytes, prev_row: bytes) -> bytes:

    result = []
    for curr, prev in zip(row, prev_row):
        result.append((curr - prev) % 256)
    return bytes(result)


def unfilter_up(row: bytes, prev_row: bytes) -> bytes:

    result = []
    for curr, prev in zip(row, prev_row):
        result.append((curr + prev) % 256)
    return bytes(result)

def paeth_predictor(a: int, b: int, c: int) -> int:

    p = a + b - c
    pa = abs(p - a)
    pb = abs(p - b)
    pc = abs(p - c)
    if pa <= pb and pa <= pc:
        return a
    elif pb <= pc:
        return b
    else:
        return c
    
def filter_paeth(row: bytes, prev_row:bytes) -> bytes:

    result = []
    for i, curr in enumerate(row):
        a = row[i-1] if i > 0 else 0
        b = prev_row[i]
        c = prev_row[i-1] if i > 0 else 0
        p = paeth_predictor(a, b, c)
        result.append((curr - p) % 256)
    return bytes(result)

def unfilter_paeth(row: bytes, prev_row:bytes) -> bytes:

    result = []
    for i, curr in enumerate(row):
        a = result[i-1] if i > 0 else 0
        b = prev_row[i]
        c = prev_row[i-1] if i > 0 else 0
        p = paeth_predictor(a, b, c)
        result.append((curr + p) % 256)
    return bytes(result)

def best_filter_for_row(row:bytes, prev_row:bytes) -> int:

    candidates = {
        0: row,
        1: filter_sub(row),
        2: filter_up(row, prev_row),
        4: filter_paeth(row, prev_row)
    }
    def score(filtered:bytes) -> int:
        return sum(min(v,256-v) for v in filtered)
    
    best_type = min(candidates, key=lambda t: score(candidates[t]))
    return best_type, candidates[best_type]

def apply_filters(pixels: np.array) -> list[tuple[int, bytes]]:
    
    if pixels.ndim ==2:
        rows = [bytes(row) for row in pixels]

    else:
        rows = [bytes(row.flatten()) for row in pixels]

    result = []
    prev_row = bytes(len(rows[0]))

    for row in rows:
        filter_type, filtered = best_filter_for_row(row, prev_row)
        result.append((filter_type, filtered))
        prev_row = row

    return result

def remove_filters(filtered_rows: list[tuple[int, bytes]], width: int, channels: int) -> np.ndarray:

    raw_rows = []
    prev_row = bytes(width * channels)

    for filter_type, row_data in filtered_rows:
        if filter_type == 0:
            raw_row = row_data
        elif filter_type == 1:
            raw_row = unfilter_sub(row_data)
        elif filter_type == 2:
            raw_row = unfilter_up(row_data, prev_row)
        elif filter_type == 4:
            raw_row = unfilter_paeth(row_data, prev_row)
        else:
            raise ValueError(f"Unknown filter type: {filter_type}")
        
        raw_rows.append(raw_row)
        prev_row = raw_row


    all_bytes = b''.join(raw_rows)
    arr = np.frombuffer(all_bytes, dtype = np.uint8)

    if channels == 1:
        return arr.reshape(len(raw_rows), width)
    else:
        return arr.reshape(len(raw_rows), width, channels)
