import unittest
from sudoku_solver import SudokuSolverApp
import tkinter as tk
import numpy as np

class TestSudokuSolverApp(unittest.TestCase):

    def setUp(self):
        self.root = tk.Tk()
        self.app = SudokuSolverApp(self.root)
        self.board = [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ]

    def tearDown(self):
        self.root.destroy()

    def test_is_safe(self):
        self.assertTrue(self.app.is_safe(self.board, 0, 2, 1))
        self.assertFalse(self.app.is_safe(self.board, 0, 2, 3))
        self.assertFalse(self.app.is_safe(self.board, 4, 4, 8))
        self.assertTrue(self.app.is_safe(self.board, 4, 4, 5))

    def test_update_board(self):
        self.app.update_board(self.board)
        for i in range(9):
            for j in range(9):
                if self.board[i][j] != 0:
                    self.assertEqual(self.app.entries[i][j].get(), str(self.board[i][j]))
                else:
                    self.assertEqual(self.app.entries[i][j].get(), '')

    def test_find_empty(self):
        self.assertEqual(self.app.find_empty(self.board), (0, 2))
        self.board[0][2] = 1
        self.assertEqual(self.app.find_empty(self.board), (0, 3))

    def test_solve_sudoku(self):
        board = np.array([
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ])
        self.assertTrue(self.app.solve_sudoku(board))
        self.assertTrue(self.app.is_valid_board(board))

if __name__ == "__main__":
    unittest.main()