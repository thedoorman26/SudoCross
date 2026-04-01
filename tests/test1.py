from puzzle_engine.core.grid import Grid
from puzzle_engine.generator.sudoku_solution_generator import SudokuSolutionGenerator
from puzzle_engine.validator.sudoku_validator import SudokuValidator


def test_generate_complete_valid_sudoku():
    print("Running Test 4.1: Generate a complete and valid Sudoku grid")

    # Step 1: Run the Sudoku solution generator
    grid = Grid()
    generator = SudokuSolutionGenerator(grid)
    success = generator.generate()

    # Check generator succeeded
    if not success:
        print("FAIL: Sudoku solution generator did not complete successfully.")
        return

    # Step 2: Produce a completed 9x9 grid
    all_filled = all(cell.value is not None for cell in grid.all_cells())
    if not all_filled:
        print("FAIL: Generated grid is not completely filled.")
        return

    # Step 3: Run the Sudoku validator on the grid
    validator = SudokuValidator(grid)
    is_valid = validator.is_valid()

    if not is_valid:
        print("FAIL: Sudoku validator reported the grid as invalid.")
        return

    print("PASS: Generated Sudoku grid is complete and valid.")
    print("\nGenerated Grid:")
    print(grid)


if __name__ == "__main__":
    test_generate_complete_valid_sudoku()