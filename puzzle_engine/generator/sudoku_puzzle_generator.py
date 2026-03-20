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

            if self._can_clear(cell.row, cell.col):
                cell.value = None
                cell.origin = CellOrigin.USER
                cleared += 1

    def _can_clear(self, row: int, col: int) -> bool:
        row_filled = sum(
            1 for cell in self.grid.get_row(row) if cell.value is not None
        )
        col_filled = sum(
            1 for cell in self.grid.get_column(col) if cell.value is not None
        )
        subgrid_filled = sum(
            1 for cell in self.grid.get_subgrid(row, col) if cell.value is not None
        )

        # Don't clear if it would leave too few clues in any group
        if row_filled <= 3:
            return False
        if col_filled <= 3:
            return False
        if subgrid_filled <= 3:
            return False

        return True