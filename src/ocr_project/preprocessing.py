from __future__ import annotations

from dataclasses import dataclass

import cv2
import numpy as np


@dataclass(slots=True)
class PreprocessedImage:
    original: np.ndarray
    rotated: np.ndarray
    grayscale: np.ndarray
    binary: np.ndarray
    angle: float


def load_image(path: str) -> np.ndarray:
    image = cv2.imread(path)
    if image is None:
        raise FileNotFoundError(f"Unable to load image: {path}")
    return image


def estimate_rotation_angle(image: np.ndarray) -> float:
    grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(grayscale, 50, 150)
    lines = cv2.HoughLinesP(
        edges,
        rho=1,
        theta=np.pi / 180,
        threshold=100,
        minLineLength=max(40, image.shape[1] // 5),
        maxLineGap=20,
    )
    if lines is None:
        return 0.0

    angles: list[float] = []
    for line in lines[:, 0]:
        x1, y1, x2, y2 = line
        angle = np.degrees(np.arctan2(y2 - y1, x2 - x1))
        if -45 <= angle <= 45:
            angles.append(angle)

    if not angles:
        return 0.0
    return float(np.median(angles))


def rotate_image(image: np.ndarray, angle: float) -> np.ndarray:
    height, width = image.shape[:2]
    center = (width // 2, height // 2)
    matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    return cv2.warpAffine(
        image,
        matrix,
        (width, height),
        flags=cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_REPLICATE,
    )


def binarize(image: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(grayscale, (5, 5), 0)
    binary = cv2.adaptiveThreshold(
        blurred,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        31,
        12,
    )
    return grayscale, binary


def preprocess_image(path: str) -> PreprocessedImage:
    original = load_image(path)
    angle = estimate_rotation_angle(original)
    rotated = rotate_image(original, -angle) if abs(angle) > 0.5 else original.copy()
    grayscale, binary = binarize(rotated)
    return PreprocessedImage(
        original=original,
        rotated=rotated,
        grayscale=grayscale,
        binary=binary,
        angle=angle,
    )
