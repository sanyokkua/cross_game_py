"""Module represents Tkinter game entry point."""
import logging as log
import tkinter as tk

from crossgameui.w_main_window import TicTacToeUIApp

log.basicConfig(level=log.DEBUG)


def start_game_tk() -> None:
    """Start the TK game app."""
    root_tk_app = tk.Tk()
    TicTacToeUIApp(root=root_tk_app, app_lang='ua')
    root_tk_app.mainloop()


if __name__ == '__main__':
    start_game_tk()
