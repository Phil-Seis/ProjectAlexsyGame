# File: test_tetris.py

import unittest
import pygame
from grid import Grid
from pieces import IPiece, JPiece, LPiece, OPiece, SPiece, TPiece, ZPiece
from tetris_logic import TetrisLogic
from color import Color


class TestGrid(unittest.TestCase):
    def setUp(self):
        self.grid = Grid(screen_offset=0)

    def test_border_collision_inside(self):
        self.assertTrue(self.grid.border_collision(5, 5))

    def test_border_collision_outside(self):
        self.assertFalse(self.grid.border_collision(10, 20))
        self.assertFalse(self.grid.border_collision(-1, -1))

    def test_empty_space(self):
        self.assertTrue(self.grid.empty_space(5, 5))
        self.grid.grid[5][5] = 1
        self.assertFalse(self.grid.empty_space(5, 5))

    def test_complete_line(self):
        for x in range(self.grid.total_x):
            self.grid.grid[x][0] = 1
        self.assertTrue(self.grid.complete_line(0))

    def test_delete_row(self):
        for x in range(self.grid.total_x):
            self.grid.grid[x][0] = 1
        self.grid.delete_row(0)
        self.assertTrue(
            all(self.grid.grid[x][0] == 0 for x in range(self.grid.total_x)))

    def test_clear_rows(self):
        for x in range(self.grid.total_x):
            self.grid.grid[x][0] = 1

        cleared = self.grid.clear_rows()
        self.assertEqual(cleared, 1)

    def test_reset(self):
        self.grid.grid[5][5] = 1
        self.grid.reset()
        self.assertTrue(all(all(cell == 0 for cell in row)
                        for row in self.grid.grid))


class TestPiece(unittest.TestCase):
    def test_initial_position(self):
        piece = IPiece()
        positions = piece.get_position()
        self.assertTrue(all(0 <= x < 10 and 0 <= y < 20 for x, y in positions))

    def test_rotation(self):
        piece = LPiece()
        initial_rotation = piece.get_rotation()
        piece.right_rotate()
        self.assertNotEqual(initial_rotation, piece.get_rotation())
        piece.left_rotate()
        self.assertEqual(initial_rotation, piece.get_rotation())

    def test_move(self):
        piece = JPiece()
        original_position = piece.get_position()
        piece.move(1, 1)
        new_position = piece.get_position()
        self.assertNotEqual(original_position, new_position)


class TestTetrisLogic(unittest.TestCase):
    def setUp(self):
        pygame.init()
        pygame.mixer.init()
        self.logic = TetrisLogic()

    def tearDown(self):
        pygame.quit()

    def test_initial_game_state(self):
        self.assertFalse(self.logic.game_over)
        self.assertEqual(self.logic.current_score, 0)

    def test_piece_movement(self):
        initial_position = self.logic.current_piece.get_position()
        self.logic.move_left()
        new_position = self.logic.current_piece.get_position()
        self.assertNotEqual(initial_position, new_position)

    def test_row_clear_score(self):
        for x in range(10):
            self.logic.grid.grid[x][19] = 1
        self.logic.lock()
        self.assertGreater(self.logic.current_score, 0)

    def test_game_over(self):
        for x in range(9):
            for y in range(2):
                self.logic.grid.grid[x][y] = 1
        self.logic.current_piece.move(0, -1)
        self.logic.lock()
        self.assertTrue(self.logic.game_over)


class TestColor(unittest.TestCase):
    def test_get_color(self):
        colors = Color.get_color()
        self.assertIsInstance(colors, list)
        self.assertGreater(len(colors), 0)
        self.assertIsInstance(colors[0], tuple)


if __name__ == '__main__':
    # Create a test suite and add tests
    suite = unittest.TestLoader().loadTestsFromModule(__import__('test_tetris'))

    # Run tests with verbosity
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
