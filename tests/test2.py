from puzzle_engine.core.grid import Grid
from puzzle_engine.generator.sudoku_solution_generator import SudokuSolutionGenerator
from puzzle_engine.generator.picross_clue_generator import derive_picross_clues


def derive_expected_line_clues(parity_line):
    clues = []
    run_length = 0

    for filled in parity_line:
        if filled:
            run_length += 1
        else:
            if run_length > 0:
                clues.append(run_length)
                run_length = 0

    if run_length > 0:
        clues.append(run_length)

    return clues


def test_derive_picross_clues_from_parity():
    print("Running Test 4.2: Derive Picross clues from Sudoku parity")

    # Step 1: Generate a valid Sudoku solution
    grid = Grid()
    generator = SudokuSolutionGenerator(grid)
    success = generator.generate()

    if not success:
        print("FAIL: Sudoku solution generator did not complete successfully.")
        return

    # Step 2: Derive Picross clues from the solution
    derived_clues = derive_picross_clues(grid)

    # Step 3: Convert the solution into a parity grid
    parity_grid = [
        [grid.get_cell(r, c).value % 2 == 0 for c in range(9)]
        for r in range(9)
    ]

    # Step 4: Compare the derived clues to the parity grid

    # Check row clues
    for r in range(9):
        expected_row_clues = derive_expected_line_clues(parity_grid[r])
        actual_row_clues = derived_clues["rows"][r]

        if actual_row_clues != expected_row_clues:
            print(f"FAIL: Row clue mismatch.")
            return

    # Check column clues
    for c in range(9):
        column = [parity_grid[r][c] for r in range(9)]
        expected_col_clues = derive_expected_line_clues(column)
        actual_col_clues = derived_clues["columns"][c]

        if actual_col_clues != expected_col_clues:
            print(f"FAIL: Column clue mismatch.")
            return

    print("PASS: All Picross clues correctly match the parity runs in the Sudoku solution.")

    print("\nDerived Row Clues:")
    for i, clues in enumerate(derived_clues["rows"], start=1):
        print(f"Row {i}: {clues}")

    print("\nDerived Column Clues:")
    for i, clues in enumerate(derived_clues["columns"], start=1):
        print(f"Column {i}: {clues}")


if __name__ == "__main__":
    test_derive_picross_clues_from_parity()