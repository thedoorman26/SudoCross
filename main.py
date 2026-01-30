from puzzle_engine.core.grid import Grid
from puzzle_engine.core.enums import GridSize
from puzzle_engine.generator.sudoku_solution_generator import SudokuSolutionGenerator
from puzzle_engine.generator.sudoku_puzzle_generator import SudokuPuzzleGenerator

def main():
    grid1 = Grid(GridSize.STANDARD)
    generator1 = SudokuSolutionGenerator(grid1)

    success = generator1.generate()
    print("First board generation success:", success)
    print()
    print(grid1)

    SudokuPuzzleGenerator(grid1, clues=35).generate()
    print()
    print("35 clues")
    print()
    print(grid1)

if __name__ == "__main__":
    main()