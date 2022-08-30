"""Represents main window module of the game."""
import logging as log
import tkinter as tk
from tkinter import NSEW, messagebox, ttk

from crossgame.api.controller import Controller
from crossgame.api.persistance import GameStateInMemoryPersistence
from crossgame.logic.game import GameStateDto, WinnerInfo
from crossgame.logic.game_enums import Sign
from crossgameui.w_base import BaseAppWidget
from crossgameui.w_field import TicTacToeUiFieldFrame
from crossgameui.w_menu import TicTacToeUiMenuFrame


class TicTacToeUIApp(BaseAppWidget, ttk.Frame):
    """
    Represent main window (frame) of the Tic Tac Toe Game.

    Args:
        BaseAppWidget (_type_): Required for containing common properties and lan methods
        ttk (_type_): Frame
    """

    def __init__(self, app_lang: str, root: tk.Tk) -> None:
        """Initialize Game App."""
        BaseAppWidget.__init__(self, app_lang=app_lang)
        ttk.Frame.__init__(self, root)

        self.game_persistence = GameStateInMemoryPersistence()
        self.controller = Controller(self.game_persistence)
        self.latest_state: GameStateDto | None = None

        root.wm_title(self.get_text_app_name())
        self.frame_menu = TicTacToeUiMenuFrame(app_lang=app_lang, root_frame=self,
                                               var_pl_1_trace=self.var_player_1_name,
                                               var_pl_2_trace=self.var_player_2_name,
                                               btn_reset_command=self.button_reset_game,
                                               btn_start_command=self.button_start_game)
        self.frame_field = TicTacToeUiFieldFrame(app_lang=app_lang, root_frame=self,
                                                 on_field_click_command=self.on_field_click_command)

        root.rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)
        self.grid(row=0, column=0, sticky=tk.NSEW)

        self.frame_menu.grid(row=0, column=0, sticky=NSEW)
        self.frame_field.grid(row=1, column=0, sticky=NSEW)

        self.number_rows = 2
        self.number_cols = 1
        for row in range(self.number_rows):
            self.rowconfigure(row, weight=1)
        for col in range(self.number_cols):
            self.columnconfigure(col, weight=1)

    def var_player_1_name(self, *args) -> None:
        """Triggered by entry var variable changes on Player 1 entry field."""
        self.enable_button_start()

    def var_player_2_name(self, *args) -> None:
        """Triggered by entry var variable changes on Player 2 entry field."""
        self.enable_button_start()

    def enable_button_start(self) -> None:
        """
        Check values of player names.

        If values are not empty -> enables start button
        If the both or at least one entry doesn't have a value -> start button will be
        disabled.
        """
        if self.frame_menu.var_player_1_name.get().strip() and self.frame_menu.var_player_2_name.get().strip():
            self.frame_menu.change_button_start_state(is_enabled=True)
        else:
            self.frame_menu.change_button_start_state(is_enabled=False)

    def button_reset_game(self) -> None:
        """
        Cleanup game session.

        If this method called, the game field will be cleaned up,
        player name entries will be cleaned up,
        start game button will be disabled
        """
        self.frame_menu.change_button_start_state(is_enabled=False)
        self.frame_menu.var_player_1_name.set('')
        self.frame_menu.var_player_2_name.set('')
        self.frame_menu.change_entry_player_1_state(is_enabled=True)
        self.frame_menu.change_entry_player_2_state(is_enabled=True)
        self.frame_field.disable_fields()
        self.frame_field.clear_field()

    def button_start_game(self) -> None:
        """
        Prepare and start game.

        Fetches values of player names and create new game session
        Disables start button after game was started
        """
        self.frame_menu.change_entry_player_1_state(is_enabled=False)
        self.frame_menu.change_entry_player_2_state(is_enabled=False)
        self.frame_menu.change_button_start_state(is_enabled=False)
        self.latest_state = self.controller.start_game_session(
            self.frame_menu.entry_player_1.get().strip())
        self.latest_state = self.controller.join_to_game_game_session(
            self.frame_menu.entry_player_1.get().strip(), self.latest_state.game_id)
        self.latest_state = self.controller.start_game(
            self.latest_state.game_id)
        self.frame_field.build_field_view(self.latest_state.field)

    def on_field_click_command(self, row: int, col: int, button: ttk.Button):
        """
        It is a handler of the field button clicked event.

        Args:
            row (int): row of the button
            col (int): columns of the button
            button (ttk.Button): button that was clicked
        """
        log.debug('on_field_button_click')
        button.state([f'{tk.DISABLED}'])
        text: str | None = None
        if Sign.X is self.latest_state.active_player.sign:
            text = 'X'
        else:
            text = 'O'
        button.configure(text=text)
        self.latest_state = self.controller.make_move(
            self.latest_state.game_id, self.latest_state.active_player.player_id, row, col)
        if self.latest_state.winner:
            self.frame_field.disable_fields()
            self.notify_game_result(self.latest_state.winner)

    def notify_game_result(self, winner: WinnerInfo) -> None:
        """
        Will start the process of notifying about game results.

        Args:
            winner (WinnerInfo): Represents game status after its end
        """
        text = None
        if winner.is_draw:
            text = self.get_text_finished_draw()
        else:
            val = self.get_text_finished_win()
            text = f'{val} - {winner.sign.name}'
        self.after(ms=200, func=(lambda: self.end_game_notify_dialog(text)))

    def end_game_notify_dialog(self, message: str):
        """
        Display dialog window with notification about finished game result.

        Aasks if the players want to start again

        Args:
            message (str): Message that will be displayed
        """
        is_yes: bool = messagebox.askokcancel(
            title=self.get_text_finished_msg_box(), message=message)
        if is_yes:
            self.frame_menu.change_button_start_state(is_enabled=True)
            self.frame_field.disable_fields()
            self.frame_field.clear_field()
            self.button_start_game()
