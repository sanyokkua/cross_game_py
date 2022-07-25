"""Module Contains main Class with Control Widget Implementation."""
import logging as log
import os
import sys

from PyQt6.QtCore import QSize, QTimer
from PyQt6.QtGui import QAction, QIcon, QPixmap
from PyQt6.QtWidgets import (QGridLayout, QGroupBox, QLabel, QLineEdit,
                             QMainWindow, QMenu, QMessageBox, QPushButton,
                             QSizePolicy, QVBoxLayout, QWidget)

from crossgame.api.controller import Controller
from crossgame.logic.game import WinnerInfo
from crossgame.logic.game_enums import Sign
from crossgameqt.qtwidgets.qt_widget_field import TicTacToeFieldWidget


class TicTacToeControlWidget(QMainWindow):
    """_summary_

    Args:
        QMainWindow (_type_): _description_
    """

    def __init__(self, controller: Controller) -> None:
        """_summary_

        Args:
            controller (Controller): _description_
        """
        super().__init__()
        self.controller = controller

        self.base_dir = os.getcwd()
        self.img_cross: QIcon = QIcon(
            QPixmap(f"{self.base_dir}/resources/img/img_cross.png"))
        self.img_zero: QIcon = QIcon(
            QPixmap(f"{self.base_dir}/resources/img/img_zero.png"))

        self.field_widget: TicTacToeFieldWidget = TicTacToeFieldWidget(
            self.on_field_button_click)
        self.control_widget_group: QGroupBox = None
        self.label_player_1: QLabel = None
        self.label_player_2: QLabel = None
        self.line_edit_pl_1: QLineEdit = None
        self.line_edit_pl_2: QLineEdit = None
        self.button_start: QPushButton = None

        self.setWindowTitle('Tic Tac Toe QT Game')
        size = QSize(200, 500)
        self.setMinimumSize(size)
        self.setBaseSize(size)
        self._init_menu()
        self._init_controls()
        self._init_layout()

    def _init_menu(self) -> None:
        menu_bar = self.menuBar()
        menu_game = QMenu('Game', menu_bar)

        action_reset = QAction('Reset Game', menu_game)
        action_exit = QAction('Exit Game', menu_game)

        action_reset.triggered.connect(self.on_reset_game)
        action_exit.triggered.connect(self.on_exit_game)

        menu_game.addActions([action_reset, action_exit])
        menu_bar.addMenu(menu_game)

    def _init_controls(self) -> None:
        self.control_widget_group = QGroupBox()
        grid_layout_group = QGridLayout()

        self.label_player_1 = QLabel('Player 1')
        self.label_player_2 = QLabel('Player 2')
        self.line_edit_pl_1 = QLineEdit()
        self.line_edit_pl_2 = QLineEdit()
        self.button_start = QPushButton('Start Game')
        self.button_start.setEnabled(False)

        self.line_edit_pl_1.textChanged.connect(self.on_player_1_name_change)
        self.line_edit_pl_2.textChanged.connect(self.on_player_2_name_change)
        self.button_start.clicked.connect(self.on_game_start_button_push)

        self.label_player_1.setSizePolicy(QSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
        self.label_player_2.setSizePolicy(QSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
        self.line_edit_pl_1.setSizePolicy(QSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
        self.line_edit_pl_2.setSizePolicy(QSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
        self.button_start.setSizePolicy(QSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))

        grid_layout_group.addWidget(self.label_player_1, 0, 0)
        grid_layout_group.addWidget(self.label_player_2, 0, 2)
        grid_layout_group.addWidget(self.line_edit_pl_1, 1, 0)
        grid_layout_group.addWidget(self.line_edit_pl_2, 1, 2)
        grid_layout_group.addWidget(self.button_start, 1, 1)

        self.control_widget_group.setLayout(grid_layout_group)
        self.control_widget_group.setMinimumSize(200, 100)
        self.control_widget_group.setMaximumHeight(100)

    def _init_layout(self) -> None:
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.menuBar())
        main_layout.addWidget(self.control_widget_group)
        main_layout.addWidget(self.field_widget)
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def on_exit_game(self) -> None:
        sys.exit()

    def on_reset_game(self) -> None:
        log.debug('on_reset_game')
        self.button_start.setEnabled(False)
        self.line_edit_pl_1.setText('')
        self.line_edit_pl_2.setText('')
        self.line_edit_pl_1.setEnabled(True)
        self.line_edit_pl_2.setEnabled(True)
        self.field_widget.disable_fields()
        self.field_widget.clear_field()

    def on_player_1_name_change(self, text: str) -> None:
        log.debug('on_player_1_name_change: %s', text)
        self.enable_button_start()

    def on_player_2_name_change(self, text: str) -> None:
        log.debug('on_player_2_name_change: %s', text)
        self.enable_button_start()

    def on_game_start_button_push(self) -> None:
        log.debug('on_game_start_button_push')
        self.line_edit_pl_1.setEnabled(False)
        self.line_edit_pl_2.setEnabled(False)
        self.button_start.setEnabled(False)

        player_1_name = self.line_edit_pl_1.text().strip()
        player_2_name = self.line_edit_pl_2.text().strip()

        self.latest_state = self.controller.start_game_session(player_1_name)
        self.latest_state = self.controller.join_to_game_game_session(
            player_2_name, self.latest_state.game_id)
        self.latest_state = self.controller.start_game(
            self.latest_state.game_id)

        self.field_widget.build_field_view(self.latest_state.field)
        self.on_state_update(self.latest_state)  # TODO: remove

    def enable_button_start(self) -> None:
        log.debug('enable_button_start')
        name_1 = self.line_edit_pl_1.text()
        name_2 = self.line_edit_pl_2.text()
        if name_1.strip() and name_2.strip():
            self.button_start.setEnabled(True)
            log.debug('enable_button_start --> True')
        else:
            self.button_start.setEnabled(False)
            log.debug('enable_button_start --> False')

    def on_field_button_click(self, row: int, col: int, button: QPushButton) -> None:
        log.debug('on_field_button_click, row: %d, col: %d', row, col)
        button.setEnabled(False)
        img: QIcon = None  # Can be used to put on button after click
        if Sign.X is self.latest_state.active_player.sign:
            img = self.img_cross
        else:
            img = self.img_zero
        button.setIcon(img)
        self.latest_state = self.controller.make_move(
            self.latest_state.game_id, self.latest_state.active_player.player_id, row, col)
        if self.latest_state.winner:
            self.field_widget.disable_fields()
            self.notify_game_result(self.latest_state.winner)

    def notify_game_result(self, winner: WinnerInfo):
        text = None
        if winner.is_draw:
            text = 'DRAW'
        else:
            text = f'Winner - {winner.sign.name}'
        QTimer.singleShot(500, lambda: self.end_game_notify_dialog(text))

    def end_game_notify_dialog(self, message: str):
        msg = QMessageBox()
        msg.setText(message)
        msg.setStandardButtons(
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msg.setDefaultButton(QMessageBox.StandardButton.Yes)
        res_btn = msg.exec()
        if (QMessageBox.StandardButton.Yes == res_btn):
            self.button_start.setEnabled(True)
            self.field_widget.disable_fields()
            self.field_widget.clear_field()
            self.on_game_start_button_push()
