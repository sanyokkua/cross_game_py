"""This module represents Field Frame implementation
"""
import logging as log
import tkinter as tk
from tkinter import ttk
from typing import Callable

from crossgame.logic.game_enums import Sign

from crossgameui.w_base import BaseAppWidget


class TicTacToeUiFieldFrame(BaseAppWidget, ttk.Frame):
    """Class represents a field Frame widget

    Args:
        BaseAppWidget (_type_): Required for containing common properties and lan methods
        ttk (_type_): Frame
    """

    def __init__(self, app_lang: str, root_frame: ttk.Frame, on_field_click_command: Callable) -> None:
        BaseAppWidget.__init__(self, app_lang=app_lang)
        ttk.Frame.__init__(self, root_frame)

        self.field_buttons: list[list[ttk.Button]] = []
        self.on_field_click_command: Callable = on_field_click_command

        log.debug('Base dir of the module %s', self.base_dir)
        self.img_cross: tk.PhotoImage = tk.PhotoImage(
            file=f"{self.base_dir}/resources/img/img_cross.png")
        self.img_zero: tk.PhotoImage = tk.PhotoImage(
            file=f"{self.base_dir}/resources/img/img_zero.png")
        log.debug('Cross image %s', self.img_cross)
        log.debug('Zero image %s', self.img_zero)
        self.grid(sticky=tk.NSEW)

    def build_field_view(self, field: list[list[Sign]]):
        """This method builds a button grid inside frame (self) based on the
           passed game field

        Args:
            field (list): Matrix ([[]]) of the current game field
        """
        log.debug('build_field_view()')
        rows = 0
        cols = 0
        while rows < len(field):
            row_buttons = []
            cols = 0
            while cols < len(field[rows]):
                button = ttk.Button(self)
                button.grid(row=rows, column=cols, sticky=tk.NSEW)
                button.configure(command=(
                    lambda row=rows, col=cols, button=button: self.on_field_click_command(row, col, button)))
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

    def disable_fields(self):
        """Disables all field buttons
        """
        for row_buttons in self.field_buttons:
            for button in row_buttons:
                button.state([tk.DISABLED])

    def clear_field(self):
        """Remove all the field buttons
        """
        for row_buttons in self.field_buttons:
            for button in row_buttons:
                button.grid_remove()
        del self.field_buttons
        self.field_buttons = []
