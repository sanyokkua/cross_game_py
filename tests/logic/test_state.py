import unittest

from crossgame.exceptions.game_exceptions import (CellIsAlreadyBusyException,
                                                  IncorrectFieldSizeException)
from crossgame.logic.game_enums import GameStatus, Sign
from crossgame.logic.state import GameState


class StateTestSuite(unittest.TestCase):
    def test_initialized_game(self):
        state = GameState()
        self.assertIsNotNone(state)
        self.assertIsNotNone(state.field)
        self.assertEqual(3, len(state.field))
        for row in state.field:
            self.assertEqual(3, len(row))
        for row in state.field:
            for cell in row:
                self.assertIsNone(cell)

    def test_custom_initialized_game(self):
        state = GameState(5, 5)
        for row in state.field:
            self.assertEqual(5, len(row))
        for row in state.field:
            for cell in row:
                self.assertIsNone(cell)

    def test_exception_with_incorrect_init(self):
        self.assertRaises(IncorrectFieldSizeException, GameState, 4, 4)
        self.assertRaises(IncorrectFieldSizeException, GameState, 2, 3)
        self.assertRaises(IncorrectFieldSizeException, GameState, 3, 2)
        self.assertRaises(IncorrectFieldSizeException, GameState, 0, 0)
        self.assertRaises(IncorrectFieldSizeException, GameState, -3, -3)

    def test_getting_game_state(self):
        state = GameState()
        self.assertIsNotNone(state.field)
        self.assertIsNotNone(state.get_game_state())
        self.assertEqual(3, len(state.get_game_state()))

    def test_make_move(self):
        state = GameState()
        state.make_move(0, 0, Sign.X)
        self.assertEqual(Sign.X, state.get_game_state()[0][0])
        state.make_move(1, 0, Sign.O)
        self.assertEqual(Sign.O, state.get_game_state()[1][0])
        state.make_move(2, 0, Sign.X)
        self.assertEqual(Sign.X, state.get_game_state()[2][0])
        state.make_move(0, 1, Sign.O)
        self.assertEqual(Sign.O, state.get_game_state()[0][1])
        state.make_move(2, 2, Sign.X)
        self.assertEqual(Sign.X, state.get_game_state()[2][2])
        self.assertRaises(CellIsAlreadyBusyException,
                          state.make_move, 0, 0, Sign.O)
        self.assertRaises(CellIsAlreadyBusyException,
                          state.make_move, 1, 0, Sign.X)
        self.assertRaises(CellIsAlreadyBusyException,
                          state.make_move, 2, 0, Sign.X)
        self.assertRaises(CellIsAlreadyBusyException,
                          state.make_move, 2, 2, Sign.O)

    def test_is_cell_empty(self):
        state = GameState()
        state.make_move(0, 0, Sign.X)
        state.make_move(2, 2, Sign.O)
        self.assertTrue(state.is_cell_empty(0, 1))
        self.assertTrue(state.is_cell_empty(2, 1))
        self.assertFalse(state.is_cell_empty(0, 0))
        self.assertFalse(state.is_cell_empty(2, 2))

    def test_game_is_finished_with_winner(self):
        is_finished_1 = [[Sign.O, Sign.O, Sign.O],
                         [None, None, None],
                         [None, None, None]]
        is_finished_2 = [[None, None, None],
                         [Sign.O, Sign.O, Sign.O],
                         [None, None, None]]
        is_finished_3 = [[None, None, None],
                         [None, None, None],
                         [Sign.O, Sign.O, Sign.O]]
        is_finished_4 = [[None, Sign.O, None],
                         [None, Sign.O, None],
                         [None, Sign.O, None]]
        is_finished_5 = [[Sign.O, None, None],
                         [None, Sign.O, None],
                         [None, None, Sign.O]]
        is_finished_6 = [[None, None, Sign.O],
                         [None, Sign.O, None],
                         [Sign.O, None, None]]
        is_finished_7 = [[Sign.O, None, None],
                         [Sign.O, None, None],
                         [Sign.O, None, None]]
        is_finished_8 = [[None, None, Sign.O],
                         [None, None, Sign.O],
                         [None, None, Sign.O]]
        game_state = GameState()
        for row in [is_finished_1, is_finished_2, is_finished_3,
                    is_finished_4, is_finished_5, is_finished_6,
                    is_finished_7, is_finished_8]:
            game_state.field = row
            stat = game_state.game_is_finished()
            self.assertEqual(GameStatus.FINISHED, stat.status)
            self.assertEqual(Sign.O, stat.sign)

    def test_game_is_finished_draw(self):
        is_finished_draw = [[Sign.O, Sign.X, Sign.X],
                            [Sign.X, Sign.O, Sign.O],
                            [Sign.O, Sign.X, Sign.X]]
        is_finished_draw_2 = [[Sign.O, Sign.X, Sign.X],
                              [Sign.X, Sign.O, Sign.O],
                              [Sign.X, Sign.O, Sign.X]]
        game_state = GameState(3, 3)
        for row in [is_finished_draw, is_finished_draw_2]:
            game_state.field = row
            stat = game_state.game_is_finished()
            self.assertEqual(GameStatus.DRAW, stat.status)
            self.assertIsNone(stat.sign)

    def test_game_is_finished_custom_field_5to5(self):
        custom_field_1 = [[Sign.O, None, None, None, None],
                          [None, Sign.O, None, None, None],
                          [None, None, Sign.O, None, None],
                          [None, None, None, Sign.O, None],
                          [None, None, None, None, Sign.O]]
        custom_field_2 = [[None, None, None, None, Sign.O],
                          [None, None, None, Sign.O, None],
                          [None, None, Sign.O, None, None],
                          [None, Sign.O, None, None, None],
                          [Sign.O, None, None, None, None]]
        game_state = GameState(5, 5)
        for row in [custom_field_1, custom_field_2]:
            game_state.field = row
            stat = game_state.game_is_finished()
            self.assertEqual(GameStatus.FINISHED, stat.status)
            self.assertEqual(Sign.O, stat.sign)

    def test_game_is_not_finished(self):
        is_not_finished_1 = [[None, None, None],
                             [None, None, None],
                             [None, None, None]]
        game_state = GameState()
        for row in [is_not_finished_1]:
            game_state.field = row
            res = game_state.game_is_finished().status
            self.assertEqual(GameStatus.IN_PROGRESS, res)

    def test_check_line(self):
        res, sign = GameState.check_line([None, None, None])
        self.assertFalse(res)
        self.assertIsNone(sign)

        res, sign = GameState.check_line([Sign.O, None, None])
        self.assertFalse(res)
        self.assertEqual(Sign.O, sign)

        res, sign = GameState.check_line([Sign.O, None, Sign.O])
        self.assertFalse(res)
        self.assertEqual(Sign.O, sign)

        res, sign = GameState.check_line([None, Sign.O, Sign.O])
        self.assertFalse(res)
        self.assertIsNone(sign)

        res, sign = GameState.check_line([Sign.X, Sign.X, Sign.X])
        self.assertTrue(res)
        self.assertEqual(Sign.X, sign)

    def test_make_pritty_array_str(self):
        test_arr = [[Sign.O, Sign.X, Sign.X],
                    [Sign.X, Sign.O, Sign.O],
                    [Sign.O, Sign.X, Sign.X]]
        self.assertEqual('Sign.O\tSign.X\tSign.X\t\nSign.X\tSign.O\tSign.O\t\nSign.O\tSign.X\tSign.X\t\n',
                         GameState.make_pritty_array_str(test_arr))
