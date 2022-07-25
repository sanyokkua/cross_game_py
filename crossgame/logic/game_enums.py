"""This Module will contain Objects required for fields."""
import enum


class Sign(enum.Enum):
    """This enum contains possible values for the Game Tic-Tac-Toe."""

    X = 1
    O = 2


class GameStatus(enum.Enum):
    """
    Indicatee game status.

    Args:
        enum (_type_): GameStatus
    """
    IN_PROGRESS = 1
    FINISHED = 2
    DRAW = 3
