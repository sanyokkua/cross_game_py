"""Main module that initializes QT Implementation of the game."""
import logging as log

from crossgameqt.qtwidgets.qt_main_app import TicTacToeQtApp

log.basicConfig(level=log.DEBUG)


def start_game() -> None:
    """Start the Qt Game."""
    app = TicTacToeQtApp('ua')
    app.exec()


if __name__ == '__main__':
    start_game()
