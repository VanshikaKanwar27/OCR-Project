from __future__ import annotations

import argparse
from pathlib import Path

from ocr_project.pipeline import run_pipeline


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Solve a word-search puzzle image using a Python OCR pipeline."
    )
    parser.add_argument("--image", required=True, help="Path to the puzzle image.")
    parser.add_argument(
        "--output",
        default="output",
        help="Directory where recognized text files and the solved image will be saved.",
    )
    parser.add_argument(
        "--min-word-length",
        type=int,
        default=3,
        help="Minimum word length to keep from OCR results.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    image_path = Path(args.image)
    if not image_path.exists():
        parser.error(f"Image not found: {image_path}")

    result = run_pipeline(
        image_path=str(image_path),
        output_dir=args.output,
        min_word_length=args.min_word_length,
    )

    print(f"Rotation corrected: {result.rotation_angle:.2f} degrees")
    print(f"Grid rows detected: {len(result.grid_rows)}")
    print(f"Words detected: {len(result.words)}")
    print(f"Words solved: {len(result.matches)}")
    if result.missing:
        print("Missing words:")
        for word in result.missing:
            print(f" - {word}")
    print(f"Saved outputs to: {Path(args.output).resolve()}")
    return 0
