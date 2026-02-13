from puzzle_engine.core.grid import Grid
from puzzle_engine.core.enums import GridSize
from puzzle_engine.core.enums import ParityState
from puzzle_engine.generator.sudoku_solution_generator import SudokuSolutionGenerator
from puzzle_engine.generator.sudoku_puzzle_generator import SudokuPuzzleGenerator
from puzzle_engine.generator.picross_clue_generator import derive_picross_clues
from puzzle_engine.validator.sudoku_validator import SudokuValidator
from puzzle_engine.validator.picross_validator import PicrossValidator

def main():
    print("=== Validator Sanity Check ===\n")

    grid = Grid()
    generator = SudokuSolutionGenerator(grid)
    generator.generate()

    print("Generated Sudoku solution:\n")
    print(grid)

    sudoku_validator = SudokuValidator(grid)
    print("\nSudoku valid (should be True):", sudoku_validator.is_valid())

    cell_0_0 = grid.get_cell(0, 0)
    cell_0_1 = grid.get_cell(0, 1)

    original_value = cell_0_1.value
    cell_0_1.value = cell_0_0.value  # force duplicate

    print("\nAfter forcing duplicate in row 1:")
    print(grid)
    print("Sudoku valid (should be False):", sudoku_validator.is_valid())

    cell_0_1.value = original_value
    print("\nSudoku restored:")
    print("Sudoku valid (should be True):", sudoku_validator.is_valid())

    for cell in grid.all_cells():
        if cell.value % 2 == 0:
            cell.set_parity_state(ParityState.FILLED)
        else:
            cell.set_parity_state(ParityState.EMPTY)

    picross_validator = PicrossValidator(grid)
    print("\nPicross valid (should be True):", picross_validator.is_valid())
    print("Picross complete (should be True):", picross_validator.is_complete())

    test_cell = grid.get_cell(0, 0)
    if test_cell.parity_state == ParityState.FILLED:
        test_cell.set_parity_state(ParityState.EMPTY)
    else:
        test_cell.set_parity_state(ParityState.FILLED)

    print("\nAfter incorrect parity marking at (0,0):")
    print("Picross valid (should be False):", picross_validator.is_valid())
    print("Picross complete (should be False):", picross_validator.is_complete())

if __name__ == "__main__":
    main()