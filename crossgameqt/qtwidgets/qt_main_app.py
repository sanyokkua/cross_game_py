import logging as log

from crossgame.api.controller import Controller
from crossgame.api.persistance import GameStatePersistance
from crossgame.logic.game import GameStateDto
from crossgameqt.qtwidgets.qt_widget_control import TicTacToeControlWidget
from PyQt6.QtWidgets import QApplication


class TicTacToeQtApp(QApplication):
    def __init__(self):
        super().__init__([])
        log.debug('init TicTacToeQtApp')
        self.game_persistence = GameStatePersistance()
        self.controller = Controller(self.game_persistence)
        self.latest_state: GameStateDto = None

        self.w_control = TicTacToeControlWidget(
            self.controller, self.on_state_update)
        self.w_control.show()

    def on_state_update(self, game_state: GameStateDto):
        log.debug('on_state_update was called with %s', game_state)
        self.latest_state = game_state
