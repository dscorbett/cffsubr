import sys
import argparse
from fontTools import ttLib
import cffsubr


def main(args=None):
    """Compress OpenType Font's CFF or CFF2 table by computing subroutines."""

    parser = argparse.ArgumentParser("cffsubr", description=main.__doc__)
    parser.add_argument(
        "input_file", help="input font file. Must contain either CFF or CFF2 table"
    )
    output_group = parser.add_mutually_exclusive_group()
    output_group.add_argument(
        "-o",
        "--output-file",
        default=None,
        help="optional path to output file. By default, dump binary data to stdout",
    )
    output_group.add_argument(
        "-i",
        "--inplace",
        action="store_true",
        help="whether to overwrite the input file",
    )
    parser.add_argument(
        "-f",
        "--cff-version",
        default=None,
        type=int,
        choices=(1, 2),
        help="output CFF table format version",
    )
    parser.add_argument(
        "-N",
        "--no-glyph-names",
        dest="keep_glyph_names",
        action="store_false",
        help="whether to drop postscript glyph names when converting from CFF to CFF2.",
    )
    options = parser.parse_args(args)

    if options.inplace:
        options.output_file = options.input_file
    elif not options.output_file:
        options.output_file = sys.stdout.buffer

    with ttLib.TTFont(options.input_file, lazy=True) as font:
        cffsubr.subroutinize(font, options.cff_version, options.keep_glyph_names)
        font.save(options.output_file)


if __name__ == "__main__":
    main()
