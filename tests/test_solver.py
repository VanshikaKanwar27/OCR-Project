from ocr_project.solver import solve_word_search


def test_solver_finds_horizontal_and_vertical_words():
    grid_rows = [
        "CATS",
        "XDOG",
        "XAXX",
        "TXHX",
    ]
    words = ["cat", "dog", "math", "bird"]

    _, matches, missing = solve_word_search(grid_rows, words)
    found = {match.word for match in matches}

    assert "CAT" in found
    assert "DOG" in found
    assert "MATH" not in found
    assert "BIRD" in missing
