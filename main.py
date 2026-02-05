from puzzle_engine.core.grid import Grid
from puzzle_engine.core.enums import GridSize
from puzzle_engine.generator.sudoku_solution_generator import SudokuSolutionGenerator
from puzzle_engine.generator.sudoku_puzzle_generator import SudokuPuzzleGenerator
from puzzle_engine.generator.picross_clue_generator import derive_picross_clues

def prompt_for_clue_count() -> int:
    while True:
        try:
            clues = int(input("Enter number of Sudoku clues (17–81 recommended): "))
            if 1 <= clues <= 81:
                return clues
            print("Please enter a number between 1 and 81.")
        except ValueError:
            print("Please enter a valid integer.")


def main():
    print("=== SudoCross Prototype ===\n")

    clue_count = prompt_for_clue_count()

    grid = Grid()

    solution_generator = SudokuSolutionGenerator(grid)
    solution_generator.generate()
    print("Use this as a reference when complete. Do not peek.")
    print(grid)
    print()

    picross_clues = derive_picross_clues(grid)

    puzzle_generator = SudokuPuzzleGenerator(grid, clues=clue_count)
    puzzle_generator.generate()

    print("\nSudoku Puzzle Grid:")
    print("(Use this only as number clues; Picross logic is separate)\n")
    print(grid)

    print("\nPicross Row Clues:")
    for i, row in enumerate(picross_clues["rows"], start=1):
        print(f"Row {i}: {row}")

    print("\nPicross Column Clues:")
    for i, col in enumerate(picross_clues["columns"], start=1):
        print(f"Col {i}: {col}")
    print()
    print("Use the Picross clues to sketch the parity grid by hand.")

if __name__ == "__main__":
    main()