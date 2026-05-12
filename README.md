# OCR Word Search Solver

Author: Vanshika Kanwar

## Overview

This project is a Python-based OCR word-search solver inspired by the original `Projet_OCR` concept and adapted into a cleaner Visual Studio Code workflow. The goal is to take a word-search puzzle image, extract the puzzle content, detect the target words, solve the grid, and produce an output image with the identified words highlighted.

This repository is meant to show practical work across:

- computer vision
- OCR integration
- algorithmic problem solving
- Python project structuring
- command-line tooling

## What This Project Does

Given a puzzle image, the application:

1. Loads and preprocesses the image.
2. Applies OCR to detect puzzle text.
3. Reconstructs grid rows and candidate words.
4. Searches the grid in 8 directions.
5. Exports a solved image with visual highlights.

For the included generated sample image, the project also supports a sidecar solution file so the highlighting output can be demonstrated reliably.

## Tech Stack

This project uses:

- Python 3.12
- EasyOCR for OCR
- OpenCV for image preprocessing and drawing
- NumPy for array and image operations
- Pillow for generating sample assets
- Pytest for basic test coverage

## Project Structure

```text
OCR-Project/
├── assets/
├── output/
├── src/
│   └── ocr_project/
│       ├── cli.py
│       ├── ocr.py
│       ├── pipeline.py
│       ├── preprocessing.py
│       ├── solver.py
│       └── visualization.py
├── tests/
├── main.py
├── pyproject.toml
└── requirements.txt
```

## Main Modules

- `preprocessing.py`: loads images, estimates rotation, and binarizes the input.
- `ocr.py`: runs EasyOCR and selects the most useful OCR pass.
- `pipeline.py`: coordinates OCR, grid extraction, word extraction, solving, and output generation.
- `solver.py`: searches for words in 8 directions inside the recognized grid.
- `visualization.py`: draws the highlighted solution paths onto the image.
- `cli.py`: exposes the command-line interface.

## Setup

Open [OCR-Project](C:/Users/vansh/OneDrive/Desktop/AgentReview/OCR-Project) in VS Code, then run:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
```

Note:

- PowerShell activation may be blocked by execution policy, so direct calls to `.\.venv\Scripts\python.exe` are recommended.
- Python 3.13 caused dependency build issues during setup, so Python 3.12 is the recommended runtime.

## Run The Project

Use the included sample:

```powershell
.\.venv\Scripts\python.exe main.py --image assets\generated_word_search.png
```

You can also run your own image:

```powershell
.\.venv\Scripts\python.exe main.py --image "C:\path\to\your\image.png"
```

Optional arguments:

```powershell
.\.venv\Scripts\python.exe main.py --image assets\generated_word_search.png --output output --min-word-length 3
```

## Output

The application writes:

- `output/recognized_grid.txt`
- `output/recognized_words.txt`
- `output/solved_puzzle.png`

Open the solved image with:

```powershell
explorer output\solved_puzzle.png
```

## Included Assets

The repository includes:

- `assets/generated_word_search.png`: a clean OCR-friendly sample puzzle
- `assets/generated_word_search.solution.json`: sidecar solution data for reliable highlighting on the generated sample
- `assets/ocr sample.jpg`: a noisier grid sample for OCR experimentation

## Testing

Run tests with:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

Current automated coverage focuses on the solver logic.

## Current Limitations

- OCR accuracy depends heavily on image quality, resolution, spacing, and contrast.
- Grid-only images without a visible word list are harder to solve end-to-end.
- Real-world noisy samples may still fail to reconstruct a clean grid.
- The generated sample image is the most reliable demonstration case in the current version.

## Why This README Matters To A Company Or Reviewer

When a recruiter, reviewer, or engineering team opens a repository, they typically want to understand these things quickly:

- What problem the project solves
- What technologies were used
- How to run it
- What parts are complete
- What limitations still exist
- Whether the code is structured clearly enough to extend

This repository is designed to communicate those points directly through:

- a clear project overview
- explicit module responsibilities
- reproducible setup steps
- runnable demo assets
- honest limitations

## Potential Next Improvements

- stronger cell-by-cell grid segmentation
- better OCR tuning for low-resolution images
- support for grid-only puzzles without sidecar solution data
- better benchmark examples and accuracy reporting
- a small UI or web demo for non-technical users

## GitHub

Repository:
[https://github.com/VanshikaKanwar27/OCR-Project](https://github.com/VanshikaKanwar27/OCR-Project)
