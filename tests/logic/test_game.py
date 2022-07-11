from unittest import TestCase

from crossgame.api.player import Player
from crossgame.exceptions.game_exceptions import (
    CurrentPlayerCantMakeAmoveException, PlayerNotFoundException)
from crossgame.logic.game import TicTacToeGameClassic
from crossgame.logic.game_enums import GameStatus, Sign


class TestTicTacToeGameClassic(TestCase):
    def test_game_creation(self):
        game_id = 'test-game-id-1'
        player1 = Player('great_pl1', 'play-1-id', Sign.X, True)
        player2 = Player('bad_pl2', 'play-2-id', Sign.O, False)
        game = TicTacToeGameClassic(game_id, [player1, player2])
        self.assertIsNotNone(game)
        self.assertIsNotNone(game.game_state)
        self.assertEqual(2, len(game.players))
        self.assertEqual([player1, player2], game.players)
        self.assertEqual(GameStatus.IN_PROGRESS, game.game_status)
        self.assertIsNone(game.winner)

    def test_make_move(self):
        game_id = 'test-game-id-1'
        player1 = Player('great_pl1', 'play-1-id', Sign.X, True)
        player2 = Player('bad_pl2', 'play-2-id', Sign.O, False)
        game = TicTacToeGameClassic(game_id, [player1, player2])

        game.make_move(player1.player_id, 0, 0)
        self.assertTrue(player2.is_active)
        self.assertFalse(player1.is_active)
        self.assertEqual(Sign.X, game.get_field()[0][0])
        self.assertIsNone(game.get_field()[0][1])
        self.assertIsNone(game.get_field()[1][0])

        game.make_move(player2.player_id, 1, 1)
        self.assertFalse(player2.is_active)
        self.assertTrue(player1.is_active)
        self.assertEqual(Sign.O, game.get_field()[1][1])
        self.assertIsNone(game.get_field()[0][1])
        self.assertIsNone(game.get_field()[1][0])

        self.assertRaises(CurrentPlayerCantMakeAmoveException,
                          game.make_move, player2.player_id, 1, 2)
        self.assertRaises(PlayerNotFoundException,
                          game.make_move, 'no-existing-id', 1, 2)

        game.game_state.field = [[Sign.X, Sign.O, None],
                                 [Sign.X, Sign.O, None],
                                 [None, None, None]]
        game_state_dto = game.make_move(player1.player_id, 2, 0)
        self.assertTrue(player2.is_active)
        self.assertFalse(player1.is_active)
        self.assertIsNotNone(game.game_status)
        self.assertEqual(GameStatus.FINISHED, game.game_status)
        self.assertIsNotNone(game_state_dto)
        self.assertEqual(game_id, game_state_dto.game_id)
        self.assertEqual(player2, game_state_dto.active_player)
        self.assertEqual(['great_pl1', 'bad_pl2'], game_state_dto.player_names)
        self.assertEqual(player1, game_state_dto.winner.player)
        self.assertEqual(Sign.X, game_state_dto.winner.sign)
