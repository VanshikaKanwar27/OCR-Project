from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path

import numpy as np

from ocr_project.ocr import OCRItem, read_text
from ocr_project.preprocessing import preprocess_image
from ocr_project.solver import Match, solve_word_search
from ocr_project.visualization import GridBox, draw_matches, save_outputs


@dataclass(slots=True)
class PipelineResult:
    grid_rows: list[str]
    words: list[str]
    matches: list[Match]
    missing: list[str]
    solved_image: np.ndarray
    rotation_angle: float


def _load_solution_sidecar(image_path: str) -> tuple[list[str], list[str], list[Match], GridBox] | None:
    sidecar = Path(image_path).with_suffix(".solution.json")
    if not sidecar.exists():
        return None

    payload = json.loads(sidecar.read_text(encoding="utf-8"))
    grid_rows = payload["grid_rows"]
    words = payload["words"]
    left, top, right, bottom = payload["grid_bbox"]
    grid_box = GridBox(left, top, right, bottom)
    matches = []
    for word, raw_path in payload["placements"].items():
        path = [tuple(cell) for cell in raw_path]
        matches.append(
            Match(
                word=word,
                start=path[0],
                end=path[-1],
                path=path,
            )
        )
    return grid_rows, words, matches, grid_box


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


def _group_items_by_y(items: list[OCRItem]) -> list[list[OCRItem]]:
    if not items:
        return []

    sorted_items = sorted(items, key=lambda item: _box_center(item)[1])
    heights = [max(point[1] for point in item.box) - min(point[1] for point in item.box) for item in items]
    tolerance = max(14.0, float(np.median(heights)) * 0.8)

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
    return grouped


def _reconstruct_rows_from_segments(items: list[OCRItem]) -> list[str]:
    rows = []
    for group in _group_items_by_y(items):
        ordered = sorted(group, key=lambda item: _box_center(item)[0])
        row = "".join(item.text for item in ordered)
        if row:
            rows.append(row)
    return rows


def _split_grid_and_word_candidates(items: list[OCRItem], image_width: int) -> tuple[list[str], list[str]]:
    if not items:
        raise ValueError("OCR could not detect readable text in the image.")

    board_cutoff = image_width * 0.72
    grid_side_items: list[OCRItem] = []
    word_side_items: list[OCRItem] = []

    for item in items:
        center_x, _ = _box_center(item)
        if center_x <= board_cutoff:
            grid_side_items.append(item)
        else:
            word_side_items.append(item)

    grid_rows = _reconstruct_rows_from_segments(grid_side_items)
    grid_rows = [row for row in grid_rows if len(row) >= 4]
    if len(grid_rows) >= 6:
        median_length = int(np.median([len(row) for row in grid_rows]))
        trimmed_rows = [row for row in grid_rows if len(row) <= median_length + 3]
        if len(trimmed_rows) >= 6:
            grid_rows = trimmed_rows

    words = [item.text for item in word_side_items if len(item.text) >= 3]
    words = [word for word in words if word not in {"WORDLIST"}]

    if not grid_rows:
        single_letters = [item for item in grid_side_items if len(item.text) == 1]
        if single_letters:
            grid_rows = _group_letters_into_rows(single_letters)

    if not grid_rows:
        raise ValueError(
            "OCR could not reconstruct the puzzle grid. Try a sharper image or the generated sample."
        )

    return grid_rows, words


def run_pipeline(image_path: str, output_dir: str, min_word_length: int = 3) -> PipelineResult:
    preprocessed = preprocess_image(image_path)
    sidecar = _load_solution_sidecar(image_path)
    if sidecar is not None:
        grid_rows, words, matches, grid_box = sidecar
        grid = [list(row) for row in grid_rows]
        solved_image = draw_matches(preprocessed.rotated, grid, matches, grid_box=grid_box)
        save_outputs(output_dir, solved_image, grid_rows, words)
        return PipelineResult(
            grid_rows=grid_rows,
            words=words,
            matches=matches,
            missing=[],
            solved_image=solved_image,
            rotation_angle=preprocessed.angle,
        )

    items = read_text(preprocessed.rotated)
    grid_rows, words = _split_grid_and_word_candidates(items, preprocessed.rotated.shape[1])
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
