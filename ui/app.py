import tkinter as tk
from tkinter import messagebox

from puzzle_engine.core.grid import Grid
from puzzle_engine.core.enums import CellOrigin
from puzzle_engine.generator.sudoku_solution_generator import (
    SudokuSolutionGenerator,
)
from puzzle_engine.generator.sudoku_puzzle_generator import (
    SudokuPuzzleGenerator,
)
from puzzle_engine.validator.sudoku_validator import SudokuValidator
from puzzle_engine.validator.picross_validator import PicrossValidator
from puzzle_engine.generator.picross_clue_generator import (
    derive_picross_clues,
)
import copy
from puzzle_engine.core.enums import ParityState


class SudokuApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku + Picross")

        self.grid_model = None  # holds the underlying puzzle state
        self.picross_clues = None  # stores derived picross clues
        self.entries = []  # 2d list of entry widgets

        self._generate_new_puzzle()  # build puzzle data first
        self._build_layout()  # then construct GUI from model

    def _generate_new_puzzle(self):
        self.grid_model = Grid()  # fresh grid model

        solution_gen = SudokuSolutionGenerator(self.grid_model)
        solution_gen.generate()  # create full solved sudoku

        self._initialize_parity_states()  # assign parity to given cells only

        solution_copy = copy.deepcopy(self.grid_model)  # preserve solved grid

        self.picross_clues = derive_picross_clues(solution_copy)  # derive picross rules

        puzzle_gen = SudokuPuzzleGenerator(self.grid_model, clues=30)
        puzzle_gen.generate()  # remove values to create playable puzzle

        print("\n=== SOLUTION (DEBUG) ===")
        print(solution_copy)
        print("========================\n")

    def _build_layout(self):
        # column clues on top
        for c in range(9):
            clues = self.picross_clues["columns"][c]
            clue_text = "\n".join(str(n) for n in clues)

            label = tk.Label(
                self.root,
                text=clue_text,
                font=("Arial", 10),
                justify="center",
            )
            label.grid(row=0, column=c + 2, padx=5, pady=5)  # above sudoku grid

        # sudoku grid and row clues
        for r in range(9):
            row_entries = []

            for c in range(9):
                entry = tk.Entry(
                    self.root,
                    width=2,
                    font=("Arial", 16),
                    justify="center",
                )

                # double-click cycles parity marking
                entry.bind(
                    "<Double-Button-1>",
                    lambda event, row=r, col=c: self._cycle_parity(row, col),
                )

                entry.grid(row=r + 1, column=c + 2, padx=1, pady=1)

                cell = self.grid_model.get_cell(r, c)  # underlying model cell

                if cell.value is not None:
                    entry.insert(0, str(cell.value))  # show number in ui

                # given cells colored by parity, no editing
                if cell.origin == CellOrigin.GIVEN:
                    self._apply_initial_parity_color(cell, entry)
                    entry.config(state="disabled")
                else:
                    # editable cells start neutral
                    entry.config(
                        bg="white",
                        disabledbackground="white",
                        disabledforeground="black",
                    )

                row_entries.append(entry)

            self.entries.append(row_entries)

            # row picross clues on left
            row_clue = self.picross_clues["rows"][r]
            clue_text = " ".join(str(n) for n in row_clue)

            label = tk.Label(
                self.root,
                text=clue_text,
                font=("Arial", 10),
                justify="left",
            )
            label.grid(row=r + 1, column=0, padx=10, sticky="e")

        # control buttons
        validate_button = tk.Button(
            self.root,
            text="Validate",
            command=self._validate,  # trigger rule checking
        )
        validate_button.grid(row=10, column=1, columnspan=4, pady=10)

        new_button = tk.Button(
            self.root,
            text="New Puzzle",
            command=self._reset,  # regenerate puzzle
        )
        new_button.grid(row=10, column=5, columnspan=4, pady=10)

    def _cycle_parity(self, row, col):
        entry = self.entries[row][col]
        if entry["state"] == "disabled":  # prevent editing given cells
            return

        cell = self.grid_model.get_cell(row, col)

        # cycle through states
        if cell.parity_state == ParityState.UNKNOWN:
            cell.parity_state = ParityState.FILLED
        elif cell.parity_state == ParityState.FILLED:
            cell.parity_state = ParityState.EMPTY
        else:
            cell.parity_state = ParityState.UNKNOWN

        self._update_cell_display(row, col)  # update visual state

    def _update_cell_display(self, row, col):
        entry = self.entries[row][col]
        cell = self.grid_model.get_cell(row, col)

        # given cells are styled once and disabled
        if cell.origin == CellOrigin.GIVEN:
            return

        if cell.parity_state == ParityState.FILLED:
            color = "#c8f7c5"
        elif cell.parity_state == ParityState.EMPTY:
            color = "#ffb3b3"
        else:
            color = "white"

        entry.config(bg=color, disabledbackground=color, disabledforeground="black")

    def _update_model_from_ui(self):
        for r in range(9):
            for c in range(9):
                cell = self.grid_model.get_cell(r, c)

                # never overwrite givens
                if cell.origin == CellOrigin.GIVEN:
                    continue

                raw = self.entries[r][c].get().strip()

                if raw == "":
                    # clear the cell completely
                    if cell.value is not None or cell.origin is not None:
                        cell.clear_value()
                    continue

                if not raw.isdigit():
                    # invalid input cleared
                    cell.clear_value()
                    self.entries[r][c].delete(0, tk.END)
                    continue

                value = int(raw)

                try:
                    cell.set_value(value, CellOrigin.USER)
                except ValueError:
                    # out of range 
                    cell.clear_value()
                    self.entries[r][c].delete(0, tk.END)

    def _apply_initial_parity_color(self, cell, entry):
        # parity derived from sudoku value
        parity = (
            ParityState.FILLED
            if cell.value % 2 == 0
            else ParityState.EMPTY
        )

        color = "#c8f7c5" if parity == ParityState.FILLED else "#ffb3b3"

        entry.config(
            bg=color,
            disabledbackground=color,  # keep color when disabled
            disabledforeground="black",
        )

    def _initialize_parity_states(self):
        # initialize parity only for given clue cells
        for cell in self.grid_model.all_cells():
            if cell.origin != CellOrigin.GIVEN:
                continue

            cell.parity_state = (
                ParityState.FILLED
                if cell.value % 2 == 0
                else ParityState.EMPTY
            )

    def _validate(self):
        self._update_model_from_ui()  # sync ui to model before checking

        sudoku_valid = SudokuValidator(self.grid_model).is_valid()
        picross_complete = PicrossValidator(self.grid_model).is_complete()

        all_filled = all(
            cell.value is not None for cell in self.grid_model.all_cells()
        )

        # win condition
        if sudoku_valid and picross_complete and all_filled:
            messagebox.showinfo("Success", "Puzzle completed correctly!")
        else:
            messagebox.showerror(
                "Invalid",
                "Puzzle is incomplete or violates rules.",
            )

    def _reset(self):
        # destroy all widgets and rebuild from fresh puzzle
        for widget in self.root.winfo_children():
            widget.destroy()

        self.entries = []
        self._generate_new_puzzle()
        self._build_layout()