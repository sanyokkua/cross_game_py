"""
Represent Tic-Tac-Toe Game State.

Raises:
    IncorrectFieldSize: can be raised if class initialized with incorrect params
    CellIsAlreadyBusy: can be raised if will be a try to put value in the cell that already has a value
"""
import logging as log
from dataclasses import dataclass

from crossgame.exceptions.game_exceptions import (CellIsAlreadyBusyException,
                                                  IncorrectFieldSizeException)
from crossgame.logic.game_enums import GameStatus, Sign


@dataclass
class State:
    """Keep information about game round after check."""

    status: GameStatus
    sign: Sign | None = None


class GameState:
    """Represent state of the game and provides an ability to change this state."""

    def __init__(self, width: int = 3, height: int = 3) -> None:
        """
        Initialize games state.

        Initializes game state field with default or passed width and heights

        Args:
            width (int, optional): Defaults to 3.
            height (int, optional): Defaults to 3.

        Raises:
            IncorrectFieldSizeException: _description_
        """
        if width != height or width % 2 == 0 or width < 3 or height < 3:
            raise IncorrectFieldSizeException(
                'Field width and height should be equal')
        line = [None for i in range(height)]
        self.field = [[x for x in line] for i in range(width)]
        log.info('Game Field was generated: %s',
                 GameState.make_pritty_array_str(self.field))

    def get_game_state(self) -> list[list[Sign]]:
        """
        Retrieve and returns Game State.

        Returns:
            list: field with values
        """
        game_state = [item for item in self.field]
        log.debug('Game state: %s', GameState.make_pritty_array_str(game_state))
        return game_state

    def make_move(self, x_coordinate: int, y_coordinate: int, sign: Sign) -> None:
        """
        Put a Sign (X or O) to the field with its coordinates x and y.

        Args:
            x (int): row of the field
            y (int): column of the field
            sign (Sign): Move Sign (X or O)

        Raises:
            CellIsAlreadyBusy: Raises eception if there is a try to put value in the cell that already has a value
        """
        if self.is_cell_empty(x_coordinate, y_coordinate):
            log.debug('Cell %s:%s will be set to %s',
                      x_coordinate, y_coordinate, sign)
            self.field[x_coordinate][y_coordinate] = sign
        else:
            raise CellIsAlreadyBusyException(
                f'Cell {x_coordinate}:{y_coordinate} already has a value')

    def is_cell_empty(self, x: int, y: int) -> bool:
        """
        Check if the sell does have a value or not.

        Args:
            x (int): row of the field
            y (int): column of the field

        Returns:
            bool: if cell is empty will be returned True, if not - False
        """
        res = not self.field[x][y]  # True if self.field[x][y] is None else False
        log.debug('Cell %s:%s has value = %s', x, y, res)
        return res

    def game_is_finished(self) -> State:
        """
        Check if the game was finished or it is still alive.

        Returns:
            tuple: (Bool, Sign)
        """
        arrays_to_check = [arr for arr in self.field]
        arrays_to_check.append([self.field[i][i]
                                for i in range(len(self.field))])
        arrays_to_check.append([self.field[i][len(self.field) - i - 1]
                                for i in range(len(self.field))])
        for i in range(len(self.field)):
            arr_to_append = []
            for j in range(len(self.field)):
                arr_to_append.append(self.field[j][i])
            arrays_to_check.append(arr_to_append)

        log.debug('Lines to be checked: %s', arrays_to_check)
        for arr in arrays_to_check:
            check_res = GameState.check_line(arr)
            is_all_eq, first_sign = check_res
            if is_all_eq:
                log.debug('Check Result, is_finished = %s, checked_symbol=%s',
                          is_all_eq, first_sign)
                return State(GameStatus.FINISHED, first_sign)
        game_status = GameStatus.DRAW
        for row in self.field:
            for col in row:
                if col is None:
                    game_status = GameStatus.IN_PROGRESS
        return State(game_status, None)

    @staticmethod
    def check_line(line: list[Sign]) -> tuple[bool, Sign]:
        """
        Verify if the each item in the line has the same value (excluding None values).

        Args:
            line (list): array with values []

        Returns:
            tuple: (Bool, Sign) first value represents if the all values are equal, the second - value in the first position
        """
        first_item = line[0]
        values = [item for item in line if item == first_item and item is not None]
        return (len(values) == len(line), first_item)

    @staticmethod
    def make_pritty_array_str(array: list[list[Sign]]) -> str:
        r"""
        Transform multy-dimension array (matrix).

        Transforms to the next view:

        Values1  Values2  Values3
        Values4  Values5  Values6
        Values7  Values8  Values9

        Args:
            array (list): [[],[],[]]

        Returns:
            str: "val\tval\tval\t\n...val\tval\tval\t\n"
        """
        strings: list[str] = []
        for row in array:
            for val in row:
                strings.append(f'{val}\t')
            strings.append('\n')
        return ''.join(strings)
