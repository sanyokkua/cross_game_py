from unittest import TestCase

from crossgame.api.controller import Controller
from crossgame.api.persistance import GameStatePersistance
from crossgame.logic.game_enums import Sign


class TestController(TestCase):
    def test_controller_creation(self):
        persistance = GameStatePersistance()
        controller = Controller(persistance)
        self.assertIsNotNone(controller)
        self.assertIsNotNone(controller.persistance)
        self.assertEqual(0, len(controller.persistance.game_info_dict))

    def test_start_game_session(self):
        persistance = GameStatePersistance()
        controller = Controller(persistance)
        game_state_dto = controller.start_game_session('player-1')
        self.assertIsNotNone(game_state_dto)
        self.assertEqual(1, len(controller.persistance.game_info_dict))
        players = game_state_dto.player_names
        player = game_state_dto.active_player
        winner = game_state_dto.winner
        field = game_state_dto.field
        self.assertIsNotNone(players)
        self.assertIsNotNone(player)
        self.assertIsNone(field)
        self.assertIsNone(winner)
        self.assertEqual(['player-1'], players)
        self.assertIsNotNone(player.player_id)
        self.assertIsNotNone(player.player_name)
        self.assertEqual(Sign.X, player.sign)
        self.assertTrue(player.is_active)

    def test_join_to_game_game_session(self):
        persistance = GameStatePersistance()
        controller = Controller(persistance)
        game_id = controller.start_game_session('player-1').game_id
        game_state_dto = controller.join_to_game_game_session(
            'player-2', game_id)
        self.assertIsNotNone(game_state_dto)
        players = game_state_dto.player_names
        player = game_state_dto.active_player
        winner = game_state_dto.winner
        field = game_state_dto.field
        self.assertIsNotNone(players)
        self.assertIsNotNone(player)
        self.assertIsNone(field)
        self.assertIsNone(winner)
        self.assertEqual(['player-1', 'player-2'], players)
        self.assertIsNotNone(player.player_id)
        self.assertIsNotNone(player.player_name)
        self.assertEqual(Sign.O, player.sign)
        self.assertFalse(player.is_active)

    def test_start_game(self):
        persistance = GameStatePersistance()
        controller = Controller(persistance)
        game_id = controller.start_game_session('player-1').game_id
        controller.join_to_game_game_session('player-2', game_id)
        game_state_dto = controller.start_game(game_id)
        field = game_state_dto.field
        self.assertIsNotNone(field)
        self.assertEqual(3, len(field))
        game_state_info = controller.persistance.get_game_info(game_id)
        self.assertIsNotNone(game_state_info)
        self.assertIsNotNone(game_state_info.game)

    def test_make_move(self):
        persistance = GameStatePersistance()
        controller = Controller(persistance)
        init_state = controller.start_game_session('player-1')
        game_id = init_state.game_id
        player_1 = init_state.active_player
        player_2 = controller.join_to_game_game_session(
            'player-2', game_id).active_player

        controller.start_game(game_id)
        game_state_dto = controller.make_move(
            game_id, player_1.player_id, 2, 2)
        field = game_state_dto.field

        self.assertEqual(Sign.X, field[2][2])
        self.assertTrue(player_2.is_active)
        self.assertFalse(player_1.is_active)

        game_state_dto = controller.make_move(
            game_id, player_2.player_id, 1, 1)
        field = game_state_dto.field
        self.assertEqual(Sign.O, field[1][1])
        self.assertFalse(player_2.is_active)
        self.assertTrue(player_1.is_active)

    def test_get_status(self):
        persistance = GameStatePersistance()
        controller = Controller(persistance)
        init_state = controller.start_game_session('player-1')
        game_id = init_state.game_id
        player_1 = init_state.active_player
        player_2 = controller.join_to_game_game_session(
            'player-2', game_id).active_player

        controller.start_game(game_id)
        controller.make_move(game_id, player_1.player_id, 0, 0)
        controller.make_move(game_id, player_2.player_id, 1, 1)
        controller.make_move(game_id, player_1.player_id, 0, 1)
        controller.make_move(game_id, player_2.player_id, 0, 2)
        controller.make_move(game_id, player_1.player_id, 1, 0)
        controller.make_move(game_id, player_2.player_id, 2, 0)
        game_status_dto = controller.get_status(game_id)
        field = game_status_dto.field
        active_palyer = game_status_dto.active_player  # X
        winner = game_status_dto.winner
        self.assertIsNotNone(winner)
        winner_player = winner.player
        sign = winner.sign
        self.assertEqual([[Sign.X, Sign.X, Sign.O],
                          [Sign.X, Sign.O, None],
                          [Sign.O, None, None]], field)
        self.assertIsNotNone(winner_player)
        self.assertIsNotNone(sign)
        self.assertTrue(active_palyer.is_active)
        self.assertEqual(Sign.X, active_palyer.sign)
        self.assertEqual('player-1', active_palyer.player_name)
        self.assertEqual('player-2', winner_player.player_name)
        self.assertEqual(Sign.O, winner_player.sign)
