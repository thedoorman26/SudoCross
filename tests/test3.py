from puzzle_engine.core.grid import Grid
from puzzle_engine.core.enums import CellOrigin
from puzzle_engine.generator.sudoku_solution_generator import SudokuSolutionGenerator
from puzzle_engine.generator.sudoku_puzzle_generator import SudokuPuzzleGenerator
from puzzle_engine.validator.sudoku_validator import SudokuValidator


def test_generate_playable_sudoku_puzzle():
    print("Running Test 4.3: Generate a playable Sudoku puzzle")

    requested_clues = 30

    # Step 1: Generate a valid Sudoku solution
    grid = Grid()
    solution_generator = SudokuSolutionGenerator(grid)
    success = solution_generator.generate()

    if not success:
        print("FAIL: Sudoku solution generator did not complete successfully.")
        return

    # Step 2: Remove values to create a puzzle with a specified number of clues
    puzzle_generator = SudokuPuzzleGenerator(grid, clues=requested_clues)
    puzzle_generator.generate()

    # Count remaining given cells
    given_cells = [
        cell for cell in grid.all_cells()
        if cell.value is not None and cell.origin == CellOrigin.GIVEN
    ]
    given_count = len(given_cells)

    if given_count != requested_clues:
        print("FAIL: Clue count is incorrect.")
        print(f"Expected clue count: {requested_clues}")
        print(f"Actual clue count:   {given_count}")
        return

    # Step 3: Run the Sudoku validator on the resulting grid
    validator = SudokuValidator(grid)
    is_valid = validator.is_valid()

    if not is_valid:
        print("FAIL: Sudoku validator reported the puzzle as invalid.")
        return

    print("PASS: Puzzle has the correct clue count and remains Sudoku-valid.")
    print(f"Given clue count: {given_count}")

    print("\nGenerated Puzzle:")
    print(grid)


if __name__ == "__main__":
    test_generate_playable_sudoku_puzzle()