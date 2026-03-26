from typing import Optional
from puzzle_engine.core.enums import ParityState, CellOrigin


class Cell:
    def __init__(self, row: int, col: int):
        self.row = row
        self.col = col

        self.value: Optional[int] = None  # sudoku stuff
        self.origin: Optional[CellOrigin] = None

        self.parity_state: ParityState = (
            ParityState.UNKNOWN
        )  # picross stuff

    def set_value(self, value: int, origin: CellOrigin):
        if self.origin == CellOrigin.GIVEN: 
            raise ValueError(
                f"Cannot change a given cell at ({self.row},{self.col})"
            )

        if not 1 <= value <= 9:
            raise ValueError("Sudoku values must be between 1 and 9")

        self.value = value
        self.origin = origin

    def set_parity_state(self, state: ParityState):  # picross marking
        self.parity_state = state

    def clear_value(self):
        if self.origin == CellOrigin.GIVEN:
            raise ValueError("Cannot clear a given cell")

        self.value = None
        self.origin = None
        self.parity_state = ParityState.UNKNOWN

    def clear_if_user_entered(self):
        if self.origin == CellOrigin.USER:
            self.value = None
            self.origin = None
            self.parity_state = ParityState.UNKNOWN

    def is_empty(self) -> bool:
        return self.value is None