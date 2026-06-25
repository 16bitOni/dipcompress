# dipcompress

Lossless image compression built from scratch — LZ77 + Huffman coding, PNG-style row filters, and a custom `.dip` binary format. Ships with an optional C extension that makes LZ77 significantly faster, with a pure-Python fallback so it works everywhere.

```
512x512 PNG  →  786,432 B  →  301,204 B  (-61.7%)
```

---

## Installation

```bash
pip install dipcompress
```

Requires Python 3.11+. NumPy and Pillow are pulled in automatically.

The C extension is included in the pre-built wheels (Linux x86_64, Windows AMD64, macOS x86_64 + arm64). If you install from source, it compiles automatically via `setup.py`. If compilation fails, the package still works — it just uses the pure-Python LZ77.

---

## CLI

```
dipcompress <command> [options]
```

### compress

```bash
dipcompress compress photo.png photo.dip
dipcompress c photo.png photo.dip          # short alias

dipcompress compress photo.png photo.dip -v   # verbose — shows each pipeline stage
```

Output (non-verbose):
```
512x512  786,432 B  ->  301,204 B  (-61.7%)
```

### decompress

```bash
dipcompress decompress photo.dip restored.png
dipcompress d photo.dip restored.png       # short alias

dipcompress decompress photo.dip restored.png -v
```

### info

Inspect a `.dip` file without decompressing it:

```bash
dipcompress info photo.dip
dipcompress i photo.dip                    # short alias
```

Output:
```
File         : photo.dip
Dimensions   : 512 x 512  (RGB)
Raw size     : 786,432 bytes  (768.0 KB)
Stored size  : 301,204 bytes  (294.1 KB)
Ratio        : 0.383  (61.7% smaller)
Row filters  : {'Paeth': 301, 'Sub': 124, 'Up': 75, 'None': 12}
Format ver   : 1
```

### version

```bash
dipcompress --version
```

---

## Python API

```python
from dipcompress import compress, decompress

# Returns a dict with compression stats
stats = compress("photo.png", "photo.dip")
print(stats["savings_pct"])   # e.g. 61.7

decompress("photo.dip", "restored.png")
```

### `compress(input_path, output_path, verbose=False) -> dict`

| Key | Type | Description |
|---|---|---|
| `original_size` | int | Raw pixel bytes |
| `compressed_size` | int | Final `.dip` file size |
| `ratio` | float | `compressed / original` |
| `savings_pct` | float | Positive = smaller, negative = larger |
| `width` | int | Image width in pixels |
| `height` | int | Image height in pixels |
| `channels` | int | 1 (grayscale), 3 (RGB), 4 (RGBA) |
| `filter_stats` | dict | Count of each row filter type used |

### `decompress(input_path, output_path, verbose=False)`

Reconstructs the original pixel data exactly. Output can be any PIL-supported format (`.png`, `.bmp`, etc.).

### Lower-level utilities

```python
from dipcompress import load_image, save_image, pixels_to_bytes, bytes_to_pixels
from dipcompress import rle_encode, rle_decode
```

### Checking if the C extension loaded

```python
from dipcompress.lz77_fast import using_c
print("C extension active:", using_c)
```

---

## How it works

Each image goes through a four-stage pipeline:

```
Image → Row Filters → LZ77 → Huffman → .dip file
```

**1. Row filters** — each row is encoded as the delta from a predictor (same idea as PNG). Five filter types are tried per row and the one that produces the smallest byte range wins: `None`, `Sub`, `Up`, `Average`, `Paeth`.

**2. LZ77** — a sliding-window compressor that replaces repeated byte sequences with `(distance, length, literal)` tokens. The C extension handles this step when available; otherwise the pure-Python implementation is used.

**3. Huffman coding** — builds a frequency-based prefix code over the LZ77 byte stream and stores the code table in the file header.

**4. `.dip` format** — a custom binary container:

```
[4B magic: DIP\x01] [2B version] [4B width] [4B height]
[1B channels] [1B compression mode] [4B compressed length]
[height × 1B filter table]
[Huffman table]
[compressed payload]
```

Magic bytes: `44 49 50 01`

---

## Building from source

```bash
git clone https://github.com/16bitOni/dipcompress
cd dipcompress
pip install -e ".[dev]"
```

To explicitly build (or rebuild) the C extension:

```bash
python dipcompress/_c_ext/build.py
```

Run the tests:

```bash
pytest
```

---

## Platform support

| Platform | Arch | Pre-built wheel |
|---|---|---|
| Linux | x86_64 | yes |
| Windows | AMD64 | yes |
| macOS | x86_64 | yes |
| macOS | arm64 (Apple Silicon) | yes |
| Any | source install | yes (C ext compiles if toolchain available) |

Python 3.11 and 3.12 are tested in CI.

---

## Project structure

```
dipcompress/
├── __init__.py       # public API surface
├── cli.py            # argparse CLI
├── encoder.py        # compress() — full pipeline
├── decoder.py        # decompress() — full pipeline
├── filters.py        # PNG-style row filters
├── lz77.py           # pure-Python LZ77
├── lz77_fast.py      # C ext wrapper with Python fallback
├── huffman.py        # Huffman encode/decode
├── format.py         # .dip binary format (header, tables)
├── image_io.py       # PIL image load/save helpers
├── bitstream.py      # bit-level I/O
└── _c_ext/           # C source for LZ77
```

---

## License

MIT — see [LICENSE](LICENSE).

---

## Credits

Built by [Subhadip Mondal](https://github.com/16bitOni).

The compression algorithms, binary format, filter logic, and architecture were all designed and written by hand.

The GitHub Actions CI/CD pipeline, `setup.py` C extension build config, and PyPI publishing workflow were put together at the last minute with help from [Claude](https://claude.ai) — because apparently even people who implement Huffman coding from scratch draw the line at YAML indentation errors at 2 AM. No shame.
