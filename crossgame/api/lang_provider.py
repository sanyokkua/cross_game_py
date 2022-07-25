"""Module contains functionality to load lang variables."""

import configparser
import os

TEXT_APP_NAME = 'app_win_name_text'
TEXT_GAME_FINISHED_MESSAGE_BOX = 'game_finished_msg_box_text'
TEXT_GAME_FINISHED_WIN = 'game_finished_win_text'
TEXT_GAME_FINISHED_DRAW = 'game_finished_draw_text'
TEXT_LABEL_PLAYER_1_NAME = 'text_lbl_pl_1_name'
TEXT_LABEL_PLAYER_2_NAME = 'text_lbl_pl_2_name'
TEXT_BUTTON_RESET = 'text_btn_res'
TEXT_BUTTON_START = 'text_btn_start'


class LangProvider:
    """
    Base App class.

    Created to provide functionality of loading properties and manage language variables retrival.
    """

    def __init__(self, app_lang: str) -> None:
        """
        Initialize common variables.

        Args:
            app_lang (str): _description_
        """
        self.app_lang = app_lang
        self.base_dir = os.getcwd()
        self.config = configparser.ConfigParser()
        self.config.read(f'{self.base_dir}/resources/lang/langs.ini')

    def get_text_var(self, key: str, default_value: str) -> str:
        """
        Provide common method of retrieving properties.

        Args:
            key (str): property key
            default_value (str): defaul value if not found

        Returns:
            str: property value
        """
        return self.config.get(self.app_lang, key, fallback=default_value)

    def get_text_app_name(self) -> str:
        """
        Return app name.

        Returns:
            str: property value
        """
        return self.get_text_var(TEXT_APP_NAME, 'Tic Tac Toe')

    def get_text_finished_msg_box(self) -> str:
        """
        Return text for message box about game completion.

        Returns:
            str: property value
        """
        return self.get_text_var(TEXT_GAME_FINISHED_MESSAGE_BOX, 'Game Finished')

    def get_text_finished_win(self) -> str:
        """
        Return text for winner.

        Returns:
            str: property value
        """
        return self.get_text_var(TEXT_GAME_FINISHED_WIN, 'You win')

    def get_text_finished_draw(self) -> str:
        """
        Return text for DRAW result.

        Returns:
            str: property value
        """
        return self.get_text_var(TEXT_GAME_FINISHED_DRAW, 'DRAW')

    def get_text_lbl_player_1(self) -> str:
        """
        Return text for player 1 label.

        Returns:
            str: property value
        """
        return self.get_text_var(TEXT_LABEL_PLAYER_1_NAME, 'Player 1')

    def get_text_lbl_player_2(self) -> str:
        """
        Return text for player 2 label.

        Returns:
            str: property value
        """
        return self.get_text_var(TEXT_LABEL_PLAYER_2_NAME, 'Player 2')

    def get_text_btn_reset(self) -> str:
        """
        Return text for button reset.

        Returns:
            str: property value
        """
        return self.get_text_var(TEXT_BUTTON_RESET, 'Reset')

    def get_text_btn_start(self) -> str:
        """
        Return text for button start.

        Returns:
            str: property value
        """
        return self.get_text_var(TEXT_BUTTON_START, 'Start')
