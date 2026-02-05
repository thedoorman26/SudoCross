from typing import List, Dict
from puzzle_engine.core.grid import Grid


def _derive_line_clues(cells: List[bool]) -> List[int]:
    clues = []
    run_length = 0

    for filled in cells:
        if filled:
            run_length += 1
        else:
            if run_length > 0:
                clues.append(run_length)
                run_length = 0

    if run_length > 0:
        clues.append(run_length)

    return clues


def derive_picross_clues(grid: Grid) -> Dict[str, List[List[int]]]:
    size = grid.dimension

    # Build parity grid from cell values
    parity_grid = [
        [
            grid.get_cell(r, c).value % 2 == 0
            for c in range(size)
        ]
        for r in range(size)
    ]

    row_clues = []
    col_clues = []

    # Rows
    for row in parity_grid:
        row_clues.append(_derive_line_clues(row))

    # Columns
    for c in range(size):
        column = [parity_grid[r][c] for r in range(size)]
        col_clues.append(_derive_line_clues(column))

    return {
        "rows": row_clues,
        "columns": col_clues
    }
