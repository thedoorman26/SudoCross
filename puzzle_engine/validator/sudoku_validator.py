from puzzle_engine.core.grid import Grid


class SudokuValidator:
    def __init__(self, grid: Grid):
        self.grid = grid
        self.size = grid.dimension

    def is_valid(self) -> bool:
        for i in range(self.size):
            if not self._valid_group(self.grid.get_row(i)):
                return False
            if not self._valid_group(self.grid.get_column(i)):
                return False

        # Check all subgrids
        step = self.grid.subgrid_size
        for r in range(0, self.size, step):
            for c in range(0, self.size, step):
                if not self._valid_group(self.grid.get_subgrid(r, c)):
                    return False

        return True

    def _valid_group(self, cells) -> bool:
        values = [cell.value for cell in cells if cell.value is not None]
        return len(values) == len(set(values))