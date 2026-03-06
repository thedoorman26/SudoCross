import tkinter as tk
from tkinter import messagebox
import copy

from puzzle_engine.core.grid import Grid
from puzzle_engine.core.enums import CellOrigin, ParityState
from puzzle_engine.generator.sudoku_solution_generator import SudokuSolutionGenerator
from puzzle_engine.generator.sudoku_puzzle_generator import SudokuPuzzleGenerator
from puzzle_engine.generator.picross_clue_generator import derive_picross_clues
from puzzle_engine.validator.sudoku_validator import SudokuValidator
from puzzle_engine.validator.picross_validator import PicrossValidator


class SudokuApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SudoCross")
        self.root.minsize(400, 400)

        self.grid_model = None          # underlying puzzle state (Grid)
        self.picross_clues = None       # {"rows": [...], "columns": [...]}
        self.entries = []               # 2D list of Entry widgets

        self.menu_frame = None
        self.game_frame = None
        self.current_clues = 30         # default; menu overwrites

        self._show_main_menu()

    # ----------------------------
    # Screen management
    # ----------------------------
    def _clear_root(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def _show_main_menu(self):
        self._clear_root()

        self.menu_frame = tk.Frame(self.root, padx=20, pady=20)
        self.menu_frame.pack()

        title = tk.Label(
            self.menu_frame,
            text="SudoCross",
            font=("Arial", 22, "bold"),
            pady=10,
        )
        title.pack()

        subtitle = tk.Label(
            self.menu_frame,
            text="Select a difficulty:",
            font=("Arial", 12),
            pady=10,
        )
        subtitle.pack()

        tk.Button(
            self.menu_frame,
            text="Easy (40 clues)",
            width=22,
            command=lambda: self._start_game(40),
        ).pack(pady=5)

        tk.Button(
            self.menu_frame,
            text="Medium (35 clues)",
            width=22,
            command=lambda: self._start_game(35),
        ).pack(pady=5)

        tk.Button(
            self.menu_frame,
            text="Hard (30 clues)",
            width=22,
            command=lambda: self._start_game(30),
        ).pack(pady=5)

        tk.Button(
            self.menu_frame,
            text="Tutorial",
            width=22,
            command=self._show_tutorial,
        ).pack(pady=15)

    def _start_game(self, clues: int):
        self.current_clues = clues

        self._clear_root()

        self.game_frame = tk.Frame(self.root)
        self.game_frame.pack()

        self.entries = []
        self._generate_new_puzzle(clues=self.current_clues)
        self._build_layout(parent=self.game_frame)

    # ----------------------------
    # Puzzle generation
    # ----------------------------
    def _generate_new_puzzle(self, clues: int):
        self.grid_model = Grid()

        # 1) Create full solved Sudoku (all GIVEN)
        solution_gen = SudokuSolutionGenerator(self.grid_model)
        solution_gen.generate()

        # 2) Initialize parity state for GIVEN cells (based on value parity)
        self._initialize_parity_states()

        # 3) Copy solved grid and derive Picross clues from solution parity pattern
        solution_copy = copy.deepcopy(self.grid_model)
        self.picross_clues = derive_picross_clues(solution_copy)

        # 4) Remove values to create playable Sudoku puzzle
        puzzle_gen = SudokuPuzzleGenerator(self.grid_model, clues=clues)
        puzzle_gen.generate()

        # Debug (optional)
        # print("\n=== SOLUTION (DEBUG) ===")
        # print(solution_copy)
        # print("========================\n")

    def _initialize_parity_states(self):
        # Initialize parity only for GIVEN clue cells
        for cell in self.grid_model.all_cells():
            if cell.origin != CellOrigin.GIVEN:
                continue

            cell.parity_state = (
                ParityState.FILLED if cell.value % 2 == 0 else ParityState.EMPTY
            )

    # ----------------------------
    # UI build
    # ----------------------------
    def _build_layout(self, parent):
        # ---- Column Clues (Top) ----
        for c in range(9):
            clues = self.picross_clues["columns"][c]
            clue_text = "\n".join(str(n) for n in clues)

            label = tk.Label(
                parent,
                text=clue_text,
                font=("Arial", 10),
                justify="center",
            )
            label.grid(row=0, column=c + 2, padx=5, pady=5)

        # ---- Sudoku Grid + Row Clues ----
        for r in range(9):
            row_entries = []

            # Row Picross clues on left
            row_clue = self.picross_clues["rows"][r]
            row_clue_text = " ".join(str(n) for n in row_clue)

            label = tk.Label(
                parent,
                text=row_clue_text,
                font=("Arial", 10),
                justify="left",
            )
            label.grid(row=r + 1, column=0, padx=10, sticky="e")

            for c in range(9):
                entry = tk.Entry(
                    parent,
                    width=2,
                    font=("Arial", 16),
                    justify="center",
                )

                # Double-click cycles parity marking
                entry.bind(
                    "<Double-Button-1>",
                    lambda event, row=r, col=c: self._cycle_parity(row, col),
                )

                entry.grid(row=r + 1, column=c + 2, padx=1, pady=1)

                cell = self.grid_model.get_cell(r, c)

                if cell.value is not None:
                    entry.insert(0, str(cell.value))

                # GIVEN cells: color by parity and lock editing
                if cell.origin == CellOrigin.GIVEN:
                    self._apply_initial_parity_color(cell, entry)
                    entry.config(state="disabled")
                else:
                    entry.config(
                        bg="white",
                        disabledbackground="white",
                        disabledforeground="black",
                    )

                row_entries.append(entry)

            self.entries.append(row_entries)

        # ---- Control buttons ----
        validate_button = tk.Button(
            parent,
            text="Validate",
            command=self._validate,
        )
        validate_button.grid(row=10, column=1, columnspan=3, pady=10)

        new_button = tk.Button(
            parent,
            text="New Puzzle",
            command=self._reset,
        )
        new_button.grid(row=10, column=4, columnspan=3, pady=10)

        menu_button = tk.Button(
            parent,
            text="Main Menu",
            command=self._show_main_menu,
        )
        menu_button.grid(row=10, column=7, columnspan=3, pady=10)

    def _apply_initial_parity_color(self, cell, entry):
        parity = ParityState.FILLED if cell.value % 2 == 0 else ParityState.EMPTY
        color = "#c8f7c5" if parity == ParityState.FILLED else "#ffb3b3"

        entry.config(
            bg=color,
            disabledbackground=color,
            disabledforeground="black",
        )

    # ----------------------------
    # User interactions
    # ----------------------------
    def _cycle_parity(self, row, col):
        entry = self.entries[row][col]
        if entry["state"] == "disabled":
            return

        cell = self.grid_model.get_cell(row, col)

        # Cycle UNKNOWN → FILLED → EMPTY → UNKNOWN
        if cell.parity_state == ParityState.UNKNOWN:
            cell.parity_state = ParityState.FILLED
        elif cell.parity_state == ParityState.FILLED:
            cell.parity_state = ParityState.EMPTY
        else:
            cell.parity_state = ParityState.UNKNOWN

        self._update_cell_display(row, col)

    def _update_cell_display(self, row, col):
        entry = self.entries[row][col]
        cell = self.grid_model.get_cell(row, col)

        # Don't restyle givens here (they are styled once and disabled)
        if cell.origin == CellOrigin.GIVEN:
            return

        if cell.parity_state == ParityState.FILLED:
            color = "#4CBB17"
        elif cell.parity_state == ParityState.EMPTY:
            color = "#FF0000"
        else:
            color = "white"

        entry.config(
            bg=color,
            disabledbackground=color,
            disabledforeground="black",
        )

    def _update_model_from_ui(self):
        # Pull sudoku values from Entry widgets into the grid model.
        for r in range(9):
            for c in range(9):
                cell = self.grid_model.get_cell(r, c)

                if cell.origin == CellOrigin.GIVEN:
                    continue

                entry = self.entries[r][c]
                raw = entry.get().strip()

                if raw == "":
                    if cell.value is not None or cell.origin is not None:
                        cell.clear_value()
                    self._update_cell_display(r, c)
                    continue

                if not raw.isdigit():
                    entry.delete(0, tk.END)
                    cell.clear_value()
                    self._update_cell_display(r, c)
                    continue

                value = int(raw)
                try:
                    cell.set_value(value, CellOrigin.USER)
                except ValueError:
                    entry.delete(0, tk.END)
                    cell.clear_value()

                self._update_cell_display(r, c)

    # ----------------------------
    # Validate / reset / tutorial
    # ----------------------------
    def _validate(self):
        self._update_model_from_ui()

        sudoku_valid = SudokuValidator(self.grid_model).is_valid()
        picross_complete = PicrossValidator(self.grid_model).is_complete()

        all_filled = all(cell.value is not None for cell in self.grid_model.all_cells())

        if sudoku_valid and picross_complete and all_filled:
            messagebox.showinfo("Success", "Puzzle completed correctly!")
        else:
            messagebox.showerror("Invalid", "Puzzle is incomplete or violates rules.")

    def _reset(self):
        # Rebuild game screen with same difficulty
        self._clear_root()
        self.game_frame = tk.Frame(self.root)
        self.game_frame.pack()

        self.entries = []
        self._generate_new_puzzle(clues=self.current_clues)
        self._build_layout(parent=self.game_frame)

    def _show_tutorial(self):
        messagebox.showinfo(
            "Tutorial",
            "Goal: Solve the Sudoku and the Picross together on the same grid.\n\n"
            "The rules interact like so:\n"
            "Even numbers correspond to FILLED squares\n"
            "Odd numbers correspond to EMPTY squares\n\n"
            "Use Picross clues (runs of filled squares) shown on the top and left.\n"
            "Double-click an editable cell to cycle markings:\n"
            "UNKNOWN → FILLED → EMPTY → UNKNOWN\n\n"
            "Press Validate when you think you're done."
        )