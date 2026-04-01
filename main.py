from puzzle_engine.core.grid import Grid
from puzzle_engine.core.enums import GridSize
from puzzle_engine.core.enums import ParityState
from puzzle_engine.generator.sudoku_solution_generator import SudokuSolutionGenerator
from puzzle_engine.generator.sudoku_puzzle_generator import SudokuPuzzleGenerator
from puzzle_engine.generator.picross_clue_generator import derive_picross_clues
from puzzle_engine.validator.sudoku_validator import SudokuValidator
from puzzle_engine.validator.picross_validator import PicrossValidator
from tkinter import Tk
from ui.app import SudoCross

def main():
    root = Tk()
    app = SudoCross(root)
    root.mainloop()

if __name__ == "__main__":
    main()