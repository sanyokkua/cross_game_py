import logging as log
from enum import Enum
from uuid import uuid4

from crossgame.api.api_dto import GameStateDto
from crossgame.api.persistance import GameStatePersistance, SavedGameInfo
from crossgame.api.player import Player
from crossgame.logic.game import TicTacToeGameClassic
from crossgame.logic.game_enums import Sign

#TODO: implement


class PlayerType(Enum):
    """Type of the player that will be used for creating of the game

    Args:
        Enum (_type_): PlayerType
    """
    PLAYER = 1
    AI_EASY = 2
    AI_GOOD = 3


class Controller:
    """Represents the main API to control the game flow"""

    def __init__(self, persistance: GameStatePersistance) -> None:
        self.persistance = persistance

    def start_game_session(self, player_name: str) -> GameStateDto:
        """Creates a game session objects and saves to persistance service
        This method creates a game_id and creates a first player with sign X

        Args:
            player_name (str): name of the first player

        Returns:
            GameStateDto: current game status
        """
        game_id: str = str(uuid4())
        player_id: str = str(uuid4())
        player: Player = Player(player_name, player_id, Sign.X, True)
        self.persistance.save_game_info(
            game_id, SavedGameInfo(game_id, [player]))
        game_state = GameStateDto(game_id, [player.player_name], player)
        log.debug('Created game session, game_id %s, player_id %s',
                  game_id, player)
        return game_state

    def join_to_game_game_session(self, player_name: str, game_id: str) -> GameStateDto:
        """Joins a player to the game session by it ID, create second player with sign O

        Args:
            player_name (str): second player name that joins
            game_id (str): unique id of the game session

        Returns:
            GameStateDto: current game status
        """
        game_state: SavedGameInfo = self.persistance.get_game_info(game_id)
        player_id: str = str(uuid4())
        player: Player = Player(player_name, player_id, Sign.O, False)

        game_info = self.persistance.get_game_info(game_id)
        game_info.players.append(player)

        self.persistance.save_game_info(game_state.game_id, game_info)
        game_state = GameStateDto(
            game_id, [player.player_name for player in game_info.players], player)
        log.debug('Joined to game session, game_id %s, player_id %s',
                  game_id, player)
        return game_state

    def start_game(self, game_id: str) -> GameStateDto:
        """Initializes game, creates game field, prepare everything to make a first move

        Args:
            game_id (str): unique id of the game session

        Returns:
            GameStateDto: current game status
        """
        game_info = self.persistance.get_game_info(game_id)
        game_info.game = TicTacToeGameClassic(game_id, game_info.players)
        self.persistance.save_game_info(game_id, game_info)
        game_state = game_info.game.get_game_state()
        log.debug('Started game session, game_id %s', game_id)
        return game_state

    def make_move(self, game_id: str, player_id: str, row: int, column: int) -> GameStateDto:
        """Player that is active makes a move passing coordinates where he wants to put its sign

        Args:
            game_id (str): unique id of the game session
            player_id (str): player ID that was assigned during creation of player
            row (int): int value of row
            column (int): int value of column

        Returns:
            GameStateDto: current game status
        """
        current_game: SavedGameInfo = self.persistance.get_game_info(game_id)
        current_game.game.make_move(player_id, row, column)
        self.persistance.save_game_info(game_id, current_game)
        game_state = current_game.game.get_game_state()
        log.debug('Started game session, game_id %s', game_id)
        return game_state

    def get_status(self, game_id: str) -> GameStateDto:
        """Just get current game state

        Args:
            game_id (str): unique id of the game session

        Returns:
            GameStateDto: current game status
        """
        current_game = self.persistance.get_game_info(game_id)
        game_state = current_game.game.get_game_state()
        log.debug('Started game session, game_id %s', game_id)
        return game_state
