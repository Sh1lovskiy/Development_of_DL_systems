"""Compare reproduced overlays with the saved reference pixels."""

import argparse
from pathlib import Path

from PIL import Image


def images_match(expected_path, actual_path):
    with Image.open(expected_path) as expected, Image.open(actual_path) as actual:
        return (
            expected.size == actual.size
            and expected.convert("RGBA").tobytes() == actual.convert("RGBA").tobytes()
        )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("expected", nargs="?", type=Path, default=Path("/workdir/output/testA_1.jpg"))
    parser.add_argument(
        "actual", nargs="?", type=Path, default=Path("/workdir/output_test/overlay/testA_1.jpg"),
    )
    args = parser.parse_args()
    if not images_match(args.expected, args.actual):
        parser.exit(1, f"Images differ: {args.expected} and {args.actual}\n")
    print(f"Images match: {args.actual}")


if __name__ == "__main__":
    main()
