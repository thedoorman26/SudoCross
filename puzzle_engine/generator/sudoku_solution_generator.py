import random
from puzzle_engine.core.grid import Grid
from puzzle_engine.core.enums import CellOrigin


class SudokuSolutionGenerator:
    def __init__(self, grid: Grid):
        self.grid = grid
        self.size = grid.dimension
        self.subgrid_size = grid.subgrid_size

    def generate(self) -> bool:
        return self._fill_cell(0, 0)

    def _fill_cell(self, row: int, col: int) -> bool:
        if row == self.size:
            return True  # Grid fully filled

        next_row, next_col = self._next_position(row, col)

        numbers = list(range(1, self.size + 1))
        random.shuffle(numbers)

        for number in numbers:
            if self._is_valid(row, col, number):
                cell = self.grid.get_cell(row, col)
                cell.value = number
                cell.origin = CellOrigin.GIVEN

                if self._fill_cell(next_row, next_col):
                    return True

                # Backtrack
                cell.value = None

        return False

    def _next_position(self, row: int, col: int):
        if col == self.size - 1:
            return row + 1, 0
        return row, col + 1

    def _is_valid(self, row: int, col: int, value: int) -> bool:
        return (
            self._valid_in_row(row, value)
            and self._valid_in_column(col, value)
            and self._valid_in_subgrid(row, col, value)
        )

    def _valid_in_row(self, row: int, value: int) -> bool:
        return all(cell.value != value for cell in self.grid.get_row(row))

    def _valid_in_column(self, col: int, value: int) -> bool:
        return all(cell.value != value for cell in self.grid.get_column(col))

    def _valid_in_subgrid(self, row: int, col: int, value: int) -> bool:
        return all(cell.value != value for cell in self.grid.get_subgrid(row, col))