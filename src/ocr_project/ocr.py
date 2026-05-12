from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import numpy as np


@dataclass(slots=True)
class OCRItem:
    text: str
    confidence: float
    box: list[tuple[int, int]]


@lru_cache(maxsize=1)
def _get_reader():
    try:
        import easyocr
    except ImportError as exc:
        raise RuntimeError(
            "easyocr is not installed. Run `pip install -r requirements.txt` first."
        ) from exc
    return easyocr.Reader(["en"], gpu=False)


def read_text(image: np.ndarray) -> list[OCRItem]:
    reader = _get_reader()
    results = reader.readtext(image, detail=1, paragraph=False)

    items: list[OCRItem] = []
    for box, text, confidence in results:
        cleaned = "".join(ch for ch in text.upper() if ch.isalpha())
        if cleaned:
            points = [(int(x), int(y)) for x, y in box]
            items.append(OCRItem(text=cleaned, confidence=float(confidence), box=points))
    return items
