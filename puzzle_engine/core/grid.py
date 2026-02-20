from typing import List
from puzzle_engine.core.cell import Cell
from puzzle_engine.core.enums import GridSize


class Grid:
    def __init__(self, size: GridSize = GridSize.STANDARD):
        self.size = size
        self.dimension = size.value  # should be 9
        self.subgrid_size = int(self.dimension ** 0.5)

        self.cells: List[List[Cell]] = [
            [Cell(row, col) for col in range(self.dimension)]
            for row in range(self.dimension)
        ]

    def get_cell(self, row: int, col: int) -> Cell:
        return self.cells[row][col]

    def get_row(self, row: int) -> List[Cell]:
        return self.cells[row]

    def get_column(self, col: int) -> List[Cell]:
        return [self.cells[row][col] for row in range(self.dimension)]

    def get_subgrid(self, row: int, col: int) -> List[Cell]:
        start_row = (row // self.subgrid_size) * self.subgrid_size
        start_col = (col // self.subgrid_size) * self.subgrid_size

        return [
            self.cells[r][c]
            for r in range(start_row, start_row + self.subgrid_size)
            for c in range(start_col, start_col + self.subgrid_size)
        ]

    def all_cells(self) -> List[Cell]:
        return [cell for row in self.cells for cell in row]

    def clear_user_entries(self):
        for cell in self.all_cells():
            cell.clear_if_user_entered()

    def __str__(self) -> str:
        rows = []
        for r in range(self.dimension):
            row_values = []
            for c in range(self.dimension):
                value = self.cells[r][c].value
                row_values.append(
                    str(value) if value is not None else "."
                )
            rows.append(" ".join(row_values))
        return "\n".join(rows)