from puzzle_engine.core.grid import Grid
from puzzle_engine.core.enums import GridSize
from puzzle_engine.generator.sudoku_solution_generator import SudokuSolutionGenerator

def main():
    grid = Grid(GridSize.STANDARD)
    generator = SudokuSolutionGenerator(grid)

    success = generator.generate()
    print("Generation success:", success)
    print()
    print(grid)


if __name__ == "__main__":
    main()