import logging as log

from crossgameqt.qtwidgets.qt_main_app import TicTacToeQtApp

log.basicConfig(level=log.DEBUG)

app = TicTacToeQtApp()
app.exec()
