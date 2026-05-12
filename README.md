# OCR Project

Author: Vanshika Kanwar

This project is a Python recreation of the OCR word-search solver idea from `oceanedel/Projet_OCR`, adapted for a clean Visual Studio Code workflow. It takes a word-search puzzle image, preprocesses it, reads letters and candidate words with OCR, solves the puzzle, and exports a highlighted result image.

## Features

- Automatic image preprocessing and thresholding
- Rotation correction helper for skewed puzzle images
- OCR-based extraction of grid letters and word-list candidates
- Word-search solver with 8-direction path detection
- Annotated output image with highlighted solutions
- VS Code-friendly Python package layout

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

## Setup In VS Code

1. Open the `OCR-Project` folder in VS Code.
2. Create a virtual environment:

```powershell
python -m venv .venv
```

3. Activate it:

```powershell
.venv\Scripts\Activate.ps1
```

4. Install dependencies:

```powershell
pip install -e .[dev]
```

## Run The Project

Place a puzzle image in `assets/`, then run:

```powershell
python main.py --image assets\puzzle.png
```

Optional arguments:

```powershell
python main.py --image assets\puzzle.png --output output --min-word-length 3
```

The solver writes:

- `output/recognized_grid.txt`
- `output/recognized_words.txt`
- `output/solved_puzzle.png`

## Run Tests

```powershell
pytest
```

## Push To GitHub

After creating an empty GitHub repository, run these commands inside `OCR-Project`:

```powershell
git init
git add .
git commit -m "Initial Python OCR project"
git branch -M main
git remote add origin <your-github-repo-url>
git push -u origin main
```

## Notes

- OCR quality depends heavily on image clarity, letter spacing, and puzzle contrast.
- `easyocr` is used so the project stays Python-based.
- For best results, use straight-on screenshots or scans with clear word lists.
