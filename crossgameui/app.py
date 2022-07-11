import logging as log
import tkinter as tk

from crossgameui.w_main_window import TicTacToeUIApp

log.basicConfig(level=log.DEBUG)

root_tk_app = tk.Tk()
gui = TicTacToeUIApp(root=root_tk_app, app_lang='ua')
root_tk_app.mainloop()
