"""
Represent the main logic of the game (game handler).

    Raises:
        GameIdException: Raised when problems with game_id
        NumberOfPlayersException: Raised if the number of players is not 2
        CurrentPlayerCantMakeAmoveException: Raised when active player tries to
                                                make move to the non empty cell
        PlayerNotFoundException: Raised if the player by some criteria is not found
        PlayerNotFoundException: Raised if the player by some criteria is not found
        PlayerNotFoundException: Raised if the player by some criteria is not found
"""

from dataclasses import dataclass

from crossgame.api.player import Player
from crossgame.exceptions.game_exceptions import (
    CurrentPlayerCantMakeAmoveException, GameIdException,
    NumberOfPlayersException, PlayerNotFoundException)
from crossgame.logic.game_enums import GameStatus, Sign
from crossgame.logic.state import GameState


@dataclass
class WinnerInfo:
    """Keep information about winner such as Player and Sign (X or O)."""

    player: Player | None
    sign: Sign | None
    is_draw: bool = False


@dataclass
class GameStateDto:
    """Represent current game status."""

    game_id: str
    player_names: list[str]
    active_player: Player | None = None
    field: list[list[str | None]] | None = None
    winner: WinnerInfo | None = None


class TicTacToeGame:
    """Base Tic-Tac-Toe game class."""

    def __init__(self, game_id: str, players: list[Player], row: int = 3, column: int = 3) -> None:
        """
        Create an instance of TicTacToeGame.

        Args:
            game_id (str): unique game id
            players (list[Player]): list of players
            row (int, optional): number of rows. Defaults to 3.
            column (int, optional): number of columns. Defaults to 3.

        Raises:
            GameIdException: raised if no game_id is passed
            NumberOfPlayersException: raised when number of players not a 2
        """
        if game_id is None or len(str(game_id)) < 1:
            raise GameIdException('Incorrect ID passed')
        if players is None or len(players) != 2:
            raise NumberOfPlayersException('Number of players should be 2')
        self.game_id = str(game_id)
        self.players = players
        self.game_state = GameState(row, column)
        self.game_status = GameStatus.IN_PROGRESS
        self.winner = None

    def make_move(self, player_id: str, row: int, column: int) -> GameStateDto:
        """
        Represent move operation of the player.

        Puts player Sign into the cell by coordinates row and column

        Args:
            player_id (str): player unique ID
            row (int): row number (started from 0)
            column (int): column number (started from 0)

        Raises:
            CurrentPlayerCantMakeAmoveException: Raised if the client can't put its Sign to the cell

        Returns:
            GameStateDto: Game State information
        """
        current_player: Player = self.__get_player_by_id(player_id)
        if current_player.is_active:
            self.game_state.make_move(row, column, current_player.sign)
            current_player.is_active = False
            next_player: Player = self.__get_other_player(player_id)
            next_player.is_active = True
            return self.get_game_state()
        else:
            raise CurrentPlayerCantMakeAmoveException

    def __get_player_by_id(self, player_id: str) -> Player:
        for player in self.players:
            if player.player_id == player_id:
                return player
        raise PlayerNotFoundException(f"Player with {player_id} is not found")

    def __get_other_player(self, player_id: str) -> Player:
        for player in self.players:
            if player.player_id != player_id:
                return player
        raise PlayerNotFoundException(f"Player with {player_id} is not found")

    def __get_active_player(self) -> Player:
        for player in self.players:
            if player.is_active:
                return player
        raise PlayerNotFoundException(
            'No player in the list with is_active = True')

    def __get_player_by_sign(self, sign: Sign) -> Player:
        for player in self.players:
            if player.sign == sign:
                return player
        raise PlayerNotFoundException('Player with passed sign not found')

    def get_game_state(self) -> GameStateDto:
        """
        Generate game state information.

        Based on the internal state of game objects

        Returns:
            GameStateDto: Game State information
        """
        player_names_list = [player.player_name for player in self.players]
        active_player = self.__get_active_player()
        state = self.game_state.game_is_finished()
        self.game_status = GameStatus.FINISHED
        if GameStatus.FINISHED == state.status:
            self.winner = WinnerInfo(
                self.__get_player_by_sign(state.sign), state.sign)
            return GameStateDto(self.game_id, player_names_list, active_player, self.get_field(), self.winner)
        elif GameStatus.DRAW == state.status:
            self.winner = WinnerInfo(None, None, True)
            return GameStateDto(self.game_id, player_names_list, active_player, self.get_field(), self.winner)
        else:
            return GameStateDto(self.game_id, player_names_list, active_player, self.get_field())

    def get_field(self) -> list[list[Sign]]:
        """
        Return a copy of the game field (matrix).

        Returns:
            _type_: [[]]
        """
        return self.game_state.get_game_state()


class TicTacToeGameClassic(TicTacToeGame):
    """Classic Tic-Tac-Toe game implementation"""

    def __init__(self, game_id: str, players: list[Player]) -> None:
        TicTacToeGame.__init__(self, game_id, players, 3, 3)
