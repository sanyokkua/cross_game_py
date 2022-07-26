"""Module represent Console version of the game."""

from crossgame.api.controller import Controller
from crossgame.api.persistance import GameStatePersistance
from crossgame.api.player import Player
from crossgame.logic.game import GameStateDto


def new_game() -> None:
    """Start the console version of the game."""
    print('New Game')
    game_persistence = GameStatePersistance()
    controller = Controller(game_persistence)
    print('Player 1 enter the name:')
    player_1_name = input()
    start_game_state = controller.start_game_session(player_1_name)
    print('Player 2 enter the name:')
    player_2_name = input()
    join_game_state = controller.join_to_game_game_session(
        player_2_name, start_game_state.game_id)
    controller.start_game(join_game_state.game_id)

    while True:
        current_state: GameStateDto = controller.get_status(
            start_game_state.game_id)
        for row in current_state.field:
            for column in row:
                print(column, end=' ')
            print()
        active_player: Player = current_state.active_player
        print(
            f'Player - {active_player.player_name} with sign {active_player.sign} please make a move (enter row column')
        input_values = input()
        row, column = input_values.split(' ')
        state_after_move = controller.make_move(
            current_state.game_id, active_player.player_id, int(row), int(column))

        if state_after_move.winner:
            print(
                f'player {state_after_move.winner.player} is won with sign {state_after_move.winner.sign}')
            break
        else:
            print('Next move')


new_game()
