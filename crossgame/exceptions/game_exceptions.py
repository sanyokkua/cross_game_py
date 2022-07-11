"""Game Exceptions"""


class CellIsAlreadyBusyException(Exception):
    """CellIsAlreadyBusyException

    Args:
        Exception (_type_): CellIsAlreadyBusyException
    """

    def __init__(self, *args: object) -> None:
        Exception.__init__(self, *args)


class IncorrectFieldSizeException(Exception):
    """IncorrectFieldSizeException

    Args:
        Exception (_type_): IncorrectFieldSizeException
    """

    def __init__(self, *args: object) -> None:
        Exception.__init__(self, *args)


class GameIdException(Exception):
    """GameIdException

    Args:
        Exception (_type_): GameIdException
    """

    def __init__(self, *args: object) -> None:
        Exception.__init__(self, *args)


class NumberOfPlayersException(Exception):
    """NumberOfPlayersException

    Args:
        Exception (_type_): NumberOfPlayersException
    """

    def __init__(self, *args: object) -> None:
        Exception.__init__(self, *args)


class GameNotFoundException(Exception):
    """Raised when game is concrete id is not created (doesn't exist in the DB)

    Args:
        Exception (_type_): GameNotFoundException
    """

    def __init__(self, *args: object) -> None:
        Exception.__init__(self, *args)


class CurrentPlayerCantMakeAmoveException(Exception):
    """This exception can be raised if player doesn't have permission to make a move (not active)
    or if current player have used wrong column and/or row

    Args:
        Exception (_type_): CurrentPlayerCantMakeAmoveException
    """

    def __init__(self, *args: object) -> None:
        Exception.__init__(self, *args)


class PlayerNotFoundException(Exception):
    """Raised when player is not found in the list of players

    Args:
        Exception (_type_): _description_
    """

    def __init__(self, *args: object) -> None:
        Exception.__init__(self, *args)
