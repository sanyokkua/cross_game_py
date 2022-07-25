import logging as log

from crossgameqt.qtwidgets.qt_main_app import TicTacToeQtApp

log.basicConfig(level=log.DEBUG)


def start_game():
    app = TicTacToeQtApp()
    app.exec()


start_game()
