import logging as log
from typing import Callable

from crossgame.logic.game_enums import Sign
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (QGridLayout, QGroupBox, QPushButton, QSizePolicy,
                             QToolButton, QVBoxLayout, QWidget)


class TicTacToeFieldWidget(QWidget):
    def __init__(self, on_field_click: Callable[[int, int, QPushButton], None]) -> None:
        super().__init__()
        self.on_field_click = on_field_click
        self.field_buttons: list[list[QPushButton]] = []
        self.main_layout: QVBoxLayout = None
        self.field_group: QGroupBox = None
        self.field_group_layout: QGridLayout = None
        self._init_view()

    def _init_view(self):
        self.main_layout = QVBoxLayout()
        self.field_group = QGroupBox()
        self.field_group_layout = QGridLayout()
        self.field_group.setLayout(self.field_group_layout)
        self.main_layout.addWidget(self.field_group)
        self.setLayout(self.main_layout)

    def build_field_view(self, field: list[list[Sign]]):
        log.debug('build_field_view()')
        size_policy = QSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        cur_row = 0
        while cur_row < len(field):
            row_buttons = []
            cur_col = 0
            while cur_col < len(field[cur_row]):
                btn = QToolButton()
                btn.setSizePolicy(size_policy)
                btn.setMinimumSize(100, 100)
                log.debug('build_field_view, row: %d, col: %d',
                          cur_row, cur_col)
                btn.clicked.connect(
                    lambda state, x=cur_row, y=cur_col, button=btn: self.on_field_click(x, y, button))
                self.field_group_layout.addWidget(btn, cur_row, cur_col)
                self.field_group_layout.setColumnMinimumWidth(cur_col, 100)
                row_buttons.append(btn)
                cur_col += 1
            self.field_buttons.append(row_buttons)
            self.field_group_layout.setRowMinimumHeight(cur_row, 100)
            cur_row += 1

    def disable_fields(self):
        for row_buttons in self.field_buttons:
            for button in row_buttons:
                button.setEnabled(False)

    def clear_field(self):
        for row_buttons in self.field_buttons:
            for button in row_buttons:
                button.setIcon(QIcon())
                self.field_group_layout.removeWidget(button)
        del self.field_buttons
        self.field_buttons = []
