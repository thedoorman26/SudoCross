import random
from puzzle_engine.core.enums import CellOrigin
from puzzle_engine.core.grid import Grid


class SudokuPuzzleGenerator:
    def __init__(self, grid: Grid, clues: int = 30):
        self.grid = grid
        self.clues = clues

    def generate(self):
        all_cells = self.grid.all_cells()
        random.shuffle(all_cells)

        cells_to_clear = len(all_cells) - self.clues

        cleared = 0
        for cell in all_cells:
            if cleared >= cells_to_clear:
                break

            cell.value = None
            cell.origin = CellOrigin.USER
            cleared += 1
