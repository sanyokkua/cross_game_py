"""Represent a widget with Main Menu of Tic Tac Toe Game."""
import logging as log
import tkinter as tk
from tkinter import ttk
from typing import Callable

from crossgameui.w_base import BaseAppWidget


class TicTacToeUiMenuFrame(BaseAppWidget, ttk.Frame):
    """
    Menu frame is a widget extetnded from ttk.Frame.

    Creates menu representation of game
    Consists of:
        Player 1 Name Label: Reset Game Button: Player 2 Name Label
        Player 1 Name Entry: Start Game Button: Player 2 Name Entry
    Args:
        BaseAppWidget (_type_): Required for containing common properties and lan methods
        ttk (_type_): Frame
    """

    def __init__(self, app_lang: str, root_frame: ttk.Frame,
                 var_pl_1_trace: Callable[[object], None],
                 var_pl_2_trace: Callable[[object], None],
                 btn_reset_command: Callable[[], None],
                 btn_start_command: Callable[[], None]) -> None:
        """
        Initialize Menu frame.

        Args:
            app_lang (str): language of the game
            root_frame (ttk.Frame): root widget
            var_pl_1_trace (Callable[[object], None]): callback for changes of the var player 1
            var_pl_2_trace (Callable[[object], None]): callback for changes of the var player 2
            btn_reset_command (Callable[[], None]): callback for clicked event reset button
            btn_start_command (Callable[[], None]): callback for clicked event start button
        """
        BaseAppWidget.__init__(self, app_lang=app_lang)
        ttk.Frame.__init__(self, root_frame)

        self.label_player_1 = ttk.Label(
            self, text=self.get_text_lbl_player_1())
        self.label_player_2 = ttk.Label(
            self, text=self.get_text_lbl_player_2())

        self.var_player_1_name = tk.StringVar()
        self.entry_player_1 = ttk.Entry(
            self, width=7, textvariable=self.var_player_1_name)

        self.var_player_2_name = tk.StringVar()
        self.entry_player_2 = ttk.Entry(
            self, width=7, textvariable=self.var_player_2_name)

        self.button_reset_game = ttk.Button(
            self, text=self.get_text_btn_reset())
        self.button_reset_game.state([f'!{tk.DISABLED}'])

        self.button_start_game = ttk.Button(
            self, text=self.get_text_btn_start())
        self.button_start_game.state([tk.DISABLED])

        self.var_player_1_name.trace(tk.W, var_pl_1_trace)
        self.var_player_2_name.trace(tk.W, var_pl_2_trace)
        self.button_reset_game.configure(command=btn_reset_command)
        self.button_start_game.configure(command=btn_start_command)

        self.grid(sticky=tk.NSEW)

        self.label_player_1.grid(row=0, column=0, sticky=tk.NSEW)
        self.button_reset_game.grid(row=0, column=1, sticky=tk.NSEW)
        self.label_player_2.grid(row=0, column=2, sticky=tk.NSEW)

        self.entry_player_1.grid(row=1, column=0, sticky=tk.NSEW)
        self.button_start_game.grid(row=1, column=1, sticky=tk.NSEW)
        self.entry_player_2.grid(row=1, column=2, sticky=tk.NSEW)

        self.number_rows = 2
        self.number_cols = 3
        for row in range(self.number_rows):
            self.rowconfigure(row, weight=1)
        for col in range(self.number_cols):
            self.columnconfigure(col, weight=1)

    def change_entry_player_1_state(self, is_enabled: bool) -> None:
        """
        Change state of player 1 entry to the is_enabled bool value.

        Args:
            is_enabled (bool): will be used to activate/disable entry
        """
        log.debug('change_entry_player_1_state')
        self.entry_player_1.state(
            [f'!{tk.DISABLED}' if is_enabled else tk.DISABLED])

    def change_entry_player_2_state(self, is_enabled: bool) -> None:
        """
        Change state of player 2 entry to the is_enabled bool value.

        Args:
            is_enabled (bool): will be used to activate/disable entry
        """
        log.debug('change_entry_player_2_state')
        self.entry_player_2.state(
            [f'!{tk.DISABLED}' if is_enabled else tk.DISABLED])

    def change_button_start_state(self, is_enabled: bool) -> None:
        """
        Change state of start game button to the is_enabled bool value.

        Args:
            is_enabled (bool): will be used to activate/disable button
        """
        log.debug('change_button_start_state')
        self.button_start_game.state(
            [f'!{tk.DISABLED}' if is_enabled else tk.DISABLED])
