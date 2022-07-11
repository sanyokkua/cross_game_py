"""Module represents base class for loading properties and
   work with translation
"""
import configparser
import os

from crossgameui.constants import *


class BaseAppWidget:
    """Base App class created to provide functionality of loading properties
       and manage language variables retrival
    """
    def __init__(self, app_lang: str) -> None:
        self.app_lang = app_lang
        self.base_dir = os.getcwd()
        self.config = configparser.ConfigParser()
        self.config.read(f'{self.base_dir}/resources/lang/langs.ini')
        self.number_rows = 1
        self.number_cols = 1

    def get_text_var(self, key: str, default_value: str) -> str:
        """Base method that provides common method of retrieving properties

        Args:
            key (str): property key
            default_value (str): defaul value if not found

        Returns:
            str: property value
        """
        return self.config.get(self.app_lang, key, fallback=default_value)

    def get_text_app_name(self) -> str:
        """Returns app name

        Returns:
            str: property value
        """
        return self.get_text_var(TEXT_APP_NAME, 'Tic Tac Toe')

    def get_text_finished_msg_box(self) -> str:
        """Returns text for message box about game completion

        Returns:
            str: property value
        """
        return self.get_text_var(TEXT_GAME_FINISHED_MESSAGE_BOX, 'Game Finished')

    def get_text_finished_win(self) -> str:
        """Returns text for winner

        Returns:
            str: property value
        """
        return self.get_text_var(TEXT_GAME_FINISHED_WIN, 'You win')

    def get_text_finished_draw(self) -> str:
        """Returns text for DRAW result

        Returns:
            str: property value
        """
        return self.get_text_var(TEXT_GAME_FINISHED_DRAW, 'DRAW')

    def get_text_lbl_player_1(self) -> str:
        """Returns text for player 1 label

        Returns:
            str: property value
        """
        return self.get_text_var(TEXT_LABEL_PLAYER_1_NAME, 'Player 1')

    def get_text_lbl_player_2(self) -> str:
        """Returns text for player 2 label

        Returns:
            str: property value
        """
        return self.get_text_var(TEXT_LABEL_PLAYER_2_NAME, 'Player 2')

    def get_text_btn_reset(self) -> str:
        """Returns text for button reset

        Returns:
            str: property value
        """
        return self.get_text_var(TEXT_BUTTON_RESET, 'Reset')

    def get_text_btn_start(self) -> str:
        """Returns text for button start

        Returns:
            str: property value
        """
        return self.get_text_var(TEXT_BUTTON_START, 'Start')
