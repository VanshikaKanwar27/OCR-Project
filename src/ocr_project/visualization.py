from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np

from ocr_project.solver import Match


def _grid_centers(image: np.ndarray, rows: int, cols: int) -> dict[tuple[int, int], tuple[int, int]]:
    height, width = image.shape[:2]
    cell_h = height / rows
    cell_w = width / cols
    centers: dict[tuple[int, int], tuple[int, int]] = {}
    for row in range(rows):
        for col in range(cols):
            x = int((col + 0.5) * cell_w)
            y = int((row + 0.5) * cell_h)
            centers[(row, col)] = (x, y)
    return centers


def draw_matches(image: np.ndarray, grid: list[list[str]], matches: list[Match]) -> np.ndarray:
    canvas = image.copy()
    centers = _grid_centers(canvas, len(grid), len(grid[0]))
    colors = [
        (0, 255, 0),
        (255, 0, 0),
        (0, 0, 255),
        (0, 255, 255),
        (255, 255, 0),
        (255, 0, 255),
    ]

    for index, match in enumerate(matches):
        color = colors[index % len(colors)]
        points = [centers[cell] for cell in match.path]
        for point in points:
            cv2.circle(canvas, point, 12, color, 2)
        if len(points) >= 2:
            cv2.line(canvas, points[0], points[-1], color, 3)
            cv2.putText(
                canvas,
                match.word,
                (points[0][0] + 5, max(20, points[0][1] - 10)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                color,
                2,
                cv2.LINE_AA,
            )
    return canvas


def save_outputs(
    output_dir: str,
    solved_image: np.ndarray,
    grid_rows: list[str],
    words: list[str],
) -> None:
    path = Path(output_dir)
    path.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(path / "solved_puzzle.png"), solved_image)
    (path / "recognized_grid.txt").write_text("\n".join(grid_rows) + "\n", encoding="utf-8")
    (path / "recognized_words.txt").write_text("\n".join(words) + "\n", encoding="utf-8")
