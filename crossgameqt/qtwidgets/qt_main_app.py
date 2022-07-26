"""Module contains Min Application QT class."""

import logging as log

from PyQt6.QtWidgets import QApplication

from crossgame.api.controller import Controller
from crossgame.api.persistance import GameStatePersistance
from crossgameqt.qtwidgets.qt_widget_control import TicTacToeControlWidget


class TicTacToeQtApp(QApplication):
    """TicTacToeQtApp is a main class that contains logic of running Application."""

    def __init__(self, game_lang: str) -> None:
        """Initialize Application."""
        super().__init__([])
        log.debug('TicTacToeQtApp.__init__')
        self.game_persistence = GameStatePersistance()
        self.controller = Controller(self.game_persistence)
        self.w_control = TicTacToeControlWidget(self.controller, game_lang)
        self.w_control.show()
