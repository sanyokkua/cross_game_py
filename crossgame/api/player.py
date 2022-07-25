"""Module contains player related classes."""
from crossgame.logic.game_enums import Sign


class Player:
    """Represents the player information."""

    def __init__(self, player_name: str, player_id: str, sign: Sign, is_active: bool = False) -> None:
        """Init Player Object."""
        self.player_name = str(player_name)
        self.player_id = str(player_id)
        self.sign = sign
        self.is_active = is_active
