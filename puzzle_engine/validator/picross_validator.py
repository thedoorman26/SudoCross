from puzzle_engine.core.grid import Grid
from puzzle_engine.core.enums import ParityState


class PicrossValidator:
    def __init__(self, grid: Grid):
        self.grid = grid
        self.size = grid.dimension

    def is_valid(self) -> bool:
        for cell in self.grid.all_cells():
            if cell.value is None:
                continue

            true_parity = (
                ParityState.FILLED
                if cell.value % 2 == 0
                else ParityState.EMPTY
            )

            if (
                cell.parity_state != ParityState.UNKNOWN
                and cell.parity_state != true_parity
            ):
                return False

        return True

    def is_complete(self) -> bool:
        for cell in self.grid.all_cells():
            if cell.value is None:
                return False

            true_parity = (
                ParityState.FILLED
                if cell.value % 2 == 0
                else ParityState.EMPTY
            )

            if cell.parity_state != true_parity:
                return False

        return True
