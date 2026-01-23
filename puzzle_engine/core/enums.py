from enum import Enum, auto

class ParityState(Enum): # picross states
    FILLED = auto()  # paired with even sudoku numbers
    EMPTY = auto()   # paired with odd sudoku numbers
    UNKNOWN = auto() # not yet filled


class CellOrigin(Enum): # so GUI knows what can/can't be edited
    GIVEN = auto()      # should be uneditable
    USER = auto()

class GridSize(Enum):
    STANDARD = 9 # regular sudoku size