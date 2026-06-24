import argparse
import sys
import os

from . import __version__


def _cmd_compress(args):
    from .encoder import compress
    if not os.path.isfile(args.input):
        print(f"error: input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    stats = compress(args.input, args.output, verbose=args.verbose)

    if not args.verbose:
        pct = stats['savings_pct']
        sign = '-' if pct >= 0 else '+'
        print(f"{stats['width']}x{stats['height']}  "
              f"{stats['original_size']:,} B  ->  {stats['compressed_size']:,} B  "
              f"({sign}{abs(pct):.1f}%)")


def _cmd_decompress(args):
    from .decoder import decompress
    if not os.path.isfile(args.input):
        print(f"error: input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    decompress(args.input, args.output, verbose=args.verbose)

    if not args.verbose:
        print(f"saved -> {args.output}")


def _cmd_info(args):
    from .format import DipHeader, HEADER_SIZE, decode_filter_table
    from collections import Counter

    if not os.path.isfile(args.file):
        print(f"error: file not found: {args.file}", file=sys.stderr)
        sys.exit(1)

    with open(args.file, 'rb') as f:
        raw = f.read()

    header = DipHeader.from_bytes(raw)
    filter_bytes = raw[HEADER_SIZE: HEADER_SIZE + header.height]
    filter_types = decode_filter_table(filter_bytes)
    filter_names = {0: 'None', 1: 'Sub', 2: 'Up', 3: 'Average', 4: 'Paeth'}
    filter_counts = {filter_names.get(k, k): v
                     for k, v in Counter(filter_types).most_common()}

    channels_label = {1: 'grayscale', 3: 'RGB', 4: 'RGBA'}.get(header.channels, str(header.channels))
    raw_size = header.width * header.height * header.channels

    print(f"File         : {args.file}")
    print(f"Dimensions   : {header.width} x {header.height}  ({channels_label})")
    print(f"Raw size     : {raw_size:,} bytes  ({raw_size/1024:.1f} KB)")
    print(f"Stored size  : {len(raw):,} bytes  ({len(raw)/1024:.1f} KB)")
    print(f"Ratio        : {len(raw)/raw_size:.3f}  ({(1-len(raw)/raw_size)*100:.1f}% smaller)")
    print(f"Row filters  : {filter_counts}")
    print(f"Format ver   : {header.version}")


def build_parser():
    parser = argparse.ArgumentParser(
        prog='dipcompress',
        description='DipCompress — lossless image compression.',
    )
    parser.add_argument('--version', action='version', version=f'dipcompress {__version__}')

    sub = parser.add_subparsers(dest='command', metavar='command')
    sub.required = True

    # compress
    p_c = sub.add_parser('compress', aliases=['c'],
                         help='compress an image to .dip format')
    p_c.add_argument('input',  help='input image (PNG, JPEG, …)')
    p_c.add_argument('output', help='output .dip file')
    p_c.add_argument('-v', '--verbose', action='store_true')
    p_c.set_defaults(func=_cmd_compress)

    # decompress
    p_d = sub.add_parser('decompress', aliases=['d'],
                         help='decompress a .dip file back to an image')
    p_d.add_argument('input',  help='input .dip file')
    p_d.add_argument('output', help='output image (PNG recommended)')
    p_d.add_argument('-v', '--verbose', action='store_true')
    p_d.set_defaults(func=_cmd_decompress)

    # info
    p_i = sub.add_parser('info', aliases=['i'],
                         help='show metadata stored in a .dip file')
    p_i.add_argument('file', help='.dip file to inspect')
    p_i.set_defaults(func=_cmd_info)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
