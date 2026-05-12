from __future__ import annotations

from dataclasses import dataclass


Grid = list[list[str]]


@dataclass(slots=True)
class Match:
    word: str
    start: tuple[int, int]
    end: tuple[int, int]
    path: list[tuple[int, int]]


DIRECTIONS = (
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, -1),
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1),
)


def normalize_grid(rows: list[str]) -> Grid:
    normalized = ["".join(ch for ch in row.upper() if ch.isalpha()) for row in rows]
    normalized = [row for row in normalized if row]
    if not normalized:
        raise ValueError("The OCR grid is empty.")

    width = len(normalized[0])
    if any(len(row) != width for row in normalized):
        raise ValueError("The recognized grid rows do not have a consistent width.")
    return [list(row) for row in normalized]


def normalize_words(words: list[str], min_length: int = 3) -> list[str]:
    normalized = []
    for word in words:
        cleaned = "".join(ch for ch in word.upper() if ch.isalpha())
        if len(cleaned) >= min_length:
            normalized.append(cleaned)
    return sorted(set(normalized))


def find_word(grid: Grid, word: str) -> Match | None:
    rows = len(grid)
    cols = len(grid[0])
    for row in range(rows):
        for col in range(cols):
            if grid[row][col] != word[0]:
                continue
            for d_row, d_col in DIRECTIONS:
                path = []
                for offset, expected in enumerate(word):
                    next_row = row + d_row * offset
                    next_col = col + d_col * offset
                    if not (0 <= next_row < rows and 0 <= next_col < cols):
                        break
                    if grid[next_row][next_col] != expected:
                        break
                    path.append((next_row, next_col))
                else:
                    return Match(
                        word=word,
                        start=path[0],
                        end=path[-1],
                        path=path,
                    )
    return None


def solve_word_search(grid_rows: list[str], words: list[str], min_length: int = 3) -> tuple[Grid, list[Match], list[str]]:
    grid = normalize_grid(grid_rows)
    normalized_words = normalize_words(words, min_length=min_length)
    matches: list[Match] = []
    missing: list[str] = []

    for word in normalized_words:
        match = find_word(grid, word)
        if match is None:
            missing.append(word)
        else:
            matches.append(match)

    return grid, matches, missing
