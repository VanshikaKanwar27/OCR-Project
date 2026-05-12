from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import cv2
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
    variants = [image]

    if image.ndim == 3:
        grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        grayscale = image

    enlarged = cv2.resize(
        grayscale,
        None,
        fx=3.0,
        fy=3.0,
        interpolation=cv2.INTER_CUBIC,
    )
    thresholded = cv2.adaptiveThreshold(
        enlarged,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        11,
    )
    variants.extend([grayscale, enlarged, thresholded])

    best_items: list[OCRItem] = []
    for variant in variants:
        results = reader.readtext(variant, detail=1, paragraph=False)
        items: list[OCRItem] = []
        for box, text, confidence in results:
            cleaned = "".join(ch for ch in text.upper() if ch.isalpha())
            if cleaned:
                points = [(int(x), int(y)) for x, y in box]
                items.append(OCRItem(text=cleaned, confidence=float(confidence), box=points))
        if len(items) > len(best_items):
            best_items = items
        if best_items:
            break
    return best_items
