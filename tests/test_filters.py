# tests/test_filters.py

from dipcompress.filters import filter_sub, unfilter_sub, filter_up, unfilter_up, filter_paeth, unfilter_paeth
import numpy as np

def test_sub_filter_roundtrip():
    row = bytes([100, 102, 105, 103, 110, 115])
    filtered = filter_sub(row)
    recovered = unfilter_sub(filtered)
    
    assert recovered == row
    print(f"Original:  {list(row)}")
    print(f"Sub-filtered: {list(filtered)}")

def test_up_filter_roundtrip():
    row      = bytes([100, 102, 105, 103])
    prev_row = bytes([98,  101, 104, 100])
    
    filtered = filter_up(row, prev_row)
    recovered = unfilter_up(filtered, prev_row)
    
    assert recovered == row
    print(f"\nUp-filtered: {list(filtered)}")

def test_paeth_roundtrip():
    row      = bytes([100, 102, 105, 103, 110])
    prev_row = bytes([98,  100, 103, 102, 108])
    
    filtered = filter_paeth(row, prev_row)
    recovered = unfilter_paeth(filtered, prev_row)
    
    assert recovered == row
    print(f"\nPaeth-filtered: {list(filtered)}")

def test_filter_makes_data_smaller_to_compress():

    row = bytes(range(50, 100))       
    prev_row = bytes(range(48, 98))  
    
    filtered = filter_up(row, prev_row)
    
    avg_raw = sum(row) / len(row)
    avg_filtered = sum(min(v, 256-v) for v in filtered) / len(filtered)
    
    print(f"\nAverage magnitude — raw: {avg_raw:.1f}, filtered: {avg_filtered:.1f}")
    assert avg_filtered < avg_raw, "Filtering should reduce average magnitude"

if __name__ == "__main__":
    test_sub_filter_roundtrip()
    test_up_filter_roundtrip()
    test_paeth_roundtrip()
    test_filter_makes_data_smaller_to_compress()