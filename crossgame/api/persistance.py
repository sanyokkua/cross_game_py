"""
Module contains logic to manage game state.

    Raises:
        GameNotFoundException: raised if the game_id is not found

    Returns:
        _type_: GameStateInMemoryPersistence, SavedGameInfo
"""
import logging as log

from crossgame.api.player import Player
from crossgame.exceptions.game_exceptions import GameNotFoundException
from crossgame.logic.game import TicTacToeGame


class SavedGameInfo:
    """SavedGameInfo is a object that contains information for saving in the scope of the session."""

    def __init__(self, game_id: str, players: list[Player], game: TicTacToeGame = None,
                 is_started: bool = False) -> None:
        """
        Initialize SavedGameInfo object.

        Args:
            game_id (str): game ID
            players (list[Player]): player name list
            game (TicTacToeGame, optional): current game. Defaults to None.
            is_started (bool): true if game was started
        """
        self.game: TicTacToeGame = game
        self.players: list[Player] = players
        self.game_id: str = game_id
        self.is_started: bool = is_started


class GameStateInMemoryPersistence:
    """STUB persistence service that works in memory."""

    def __init__(self) -> None:
        """Initialize Game State Persistence Stub."""
        self.game_info_dict: dict[str, SavedGameInfo] = {}

    def save_game_info(self, game_id: str, game_info: SavedGameInfo) -> None:
        """
        Save game info.

        Args:
            game_id (str): unique id of the game session
            game_info (SavedGameInfo): object that contains current state of the game and players
        """
        self.game_info_dict[game_id] = game_info

    def get_game_info(self, game_id: str) -> SavedGameInfo:
        """
        Retrieve game info.

        Args:
            game_id (str): unique id of the game session

        Raises:
            GameNotFoundException: raised if the passed id doesn't exist

        Returns:
            SavedGameInfo: information about saved game session
        """
        if game_id not in self.game_info_dict:
            raise GameNotFoundException(f'Game with id {game_id} is not found')
        return self.game_info_dict.get(game_id)  # type: ignore

    def remove_game_info(self, game_id: str) -> None:
        """
        Remove game info.

        Args:
            game_id (str): unique id of the game session
        """
        if game_id not in self.game_info_dict:
            log.warning(
                'Game with %s id is not found, will be skipped', game_id)
        else:
            del self.game_info_dict[game_id]
