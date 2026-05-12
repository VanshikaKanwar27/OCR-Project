from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ocr_project.ocr import OCRItem, read_text
from ocr_project.preprocessing import preprocess_image
from ocr_project.solver import Match, solve_word_search
from ocr_project.visualization import draw_matches, save_outputs


@dataclass(slots=True)
class PipelineResult:
    grid_rows: list[str]
    words: list[str]
    matches: list[Match]
    missing: list[str]
    solved_image: np.ndarray
    rotation_angle: float


def _box_center(item: OCRItem) -> tuple[float, float]:
    xs = [point[0] for point in item.box]
    ys = [point[1] for point in item.box]
    return sum(xs) / len(xs), sum(ys) / len(ys)


def _group_letters_into_rows(items: list[OCRItem]) -> list[str]:
    if not items:
        raise ValueError("No single-letter OCR items were detected.")

    sorted_items = sorted(items, key=lambda item: _box_center(item)[1])
    heights = [max(point[1] for point in item.box) - min(point[1] for point in item.box) for item in items]
    tolerance = max(12.0, float(np.median(heights)) * 0.8)

    grouped: list[list[OCRItem]] = []
    for item in sorted_items:
        _, center_y = _box_center(item)
        if not grouped:
            grouped.append([item])
            continue
        previous_center_y = np.mean([_box_center(existing)[1] for existing in grouped[-1]])
        if abs(center_y - previous_center_y) <= tolerance:
            grouped[-1].append(item)
        else:
            grouped.append([item])

    rows = []
    for group in grouped:
        ordered = sorted(group, key=lambda item: _box_center(item)[0])
        rows.append("".join(item.text[0] for item in ordered if item.text))
    return rows


def _split_grid_and_word_candidates(items: list[OCRItem]) -> tuple[list[OCRItem], list[str]]:
    single_letters = [item for item in items if len(item.text) == 1]
    words = [item.text for item in items if len(item.text) > 1]
    if not single_letters:
        raise ValueError(
            "OCR did not detect enough single-letter cells to reconstruct the puzzle grid."
        )
    return single_letters, words


def run_pipeline(image_path: str, output_dir: str, min_word_length: int = 3) -> PipelineResult:
    preprocessed = preprocess_image(image_path)
    items = read_text(preprocessed.rotated)
    grid_items, words = _split_grid_and_word_candidates(items)
    grid_rows = _group_letters_into_rows(grid_items)
    grid, matches, missing = solve_word_search(grid_rows, words, min_length=min_word_length)
    solved_image = draw_matches(preprocessed.rotated, grid, matches)
    save_outputs(output_dir, solved_image, grid_rows, words)

    return PipelineResult(
        grid_rows=grid_rows,
        words=words,
        matches=matches,
        missing=missing,
        solved_image=solved_image,
        rotation_angle=preprocessed.angle,
    )
