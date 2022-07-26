"""Contains all the API Data Transfer Objects."""

from crossgame.api.player import Player
from crossgame.logic.game import GameStateDto


class SessionStateDto:
    """DTO class keeps Session Data."""

    def __init__(self, game_id: str) -> None:
        """
        Init Session DTO class.

        Args:
            game_id (str): ID of the game
        """
        self.game_id = game_id
        self.players_list: list[Player] = []
        self.game_state_dto: GameStateDto  # type: ignore
