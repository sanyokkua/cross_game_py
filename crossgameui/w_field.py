"""This module represents Field Frame implementation."""

import logging as log
import tkinter as tk
from tkinter import ttk
from typing import Callable

from crossgame.logic.game_enums import Sign
from crossgameui.w_base import BaseAppWidget


class TicTacToeUiFieldFrame(BaseAppWidget, ttk.Frame):
    """
    Class represents a field Frame widget.

    Args:
        BaseAppWidget (_type_): Required for containing common properties and lan methods
        ttk (_type_): Frame
    """

    def __init__(self, app_lang: str, root_frame: ttk.Frame, on_field_click_command: Callable[[object], None]) -> None:
        """
        Initialize Field Class Implementation.

        Args:
            app_lang (str): language of the game
            root_frame (ttk.Frame): Root frame
            on_field_click_command (Callable): function that will process click on the field button
        """
        BaseAppWidget.__init__(self, app_lang=app_lang)
        ttk.Frame.__init__(self, root_frame)
        self.field_buttons: list[list[ttk.Button]] = []
        self.on_field_click_command: Callable[[object], None] = on_field_click_command
        self.grid(sticky=tk.NSEW)

    def build_field_view(self, field: list[list[Sign]]) -> None:
        """
        Build button grid.

        This method builds a button grid inside frame (self) based on the
           passed game field.

        Args:
            field (list): Matrix ([[]]) of the current game field
        """
        log.debug('build_field_view()')
        rows: int = 0
        cols: int = 0
        while rows < len(field):
            row_buttons: list[ttk.Button] = []
            cols = 0
            while cols < len(field[rows]):
                button = ttk.Button(self)
                button.grid(row=rows, column=cols, sticky=tk.NSEW)
                btn_command: Callable[[int, int, ttk.Button], None] = (lambda row=rows, col=cols, button=button:
                                                                       self.on_field_click_command(row, col, button))
                button.configure(command=btn_command)
                row_buttons.append(button)
                self.columnconfigure(cols, weight=1)
                cols += 1
            self.field_buttons.append(row_buttons)
            self.rowconfigure(rows, weight=1)
            rows += 1
        self.number_rows = rows
        self.number_cols = cols
        for row in range(self.number_rows):
            self.rowconfigure(row, weight=1)
        for col in range(self.number_cols):
            self.columnconfigure(col, weight=1)

    def disable_fields(self) -> None:
        """Disables all field buttons."""
        for row_buttons in self.field_buttons:
            for button in row_buttons:
                button.state([tk.DISABLED])

    def clear_field(self) -> None:
        """Remove all the field buttons."""
        for row_buttons in self.field_buttons:
            for button in row_buttons:
                button.grid_remove()
        del self.field_buttons
        self.field_buttons = []
