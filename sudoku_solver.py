import tkinter as tk
import numpy as np
import time

class SudokuSolverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver")
        self.canvas = tk.Canvas(self.root, width=450, height=450)
        self.canvas.grid(row=0, column=0, columnspan=9, rowspan=9)
        self.entries = [[None for _ in range(9)] for _ in range(9)]
        self.initial_board = np.zeros((9, 9), dtype=int)  # Empty board
        self.create_board()
        self.create_solve_button()
        self.create_reset_button()
        self.create_timer_label()
        self.create_status_label()

    def create_board(self):
        for i in range(9):
            for j in range(9):
                x, y = j * 50, i * 50
                entry = tk.Entry(self.root, width=2, font=('Arial', 18, 'bold'), justify='center')
                entry.place(x=x+5, y=y+5, width=45, height=45)
                self.entries[i][j] = entry

        for i in range(10):
            width = 3 if i % 3 == 0 else 1
            self.canvas.create_line(0, i * 50, 450, i * 50, width=width)
            self.canvas.create_line(i * 50, 0, i * 50, 450, width=width)

    def create_solve_button(self):
        solve_button = tk.Button(self.root, text="Solve", font=('Arial', 18, 'bold'), command=self.solve)
        solve_button.grid(row=9, column=4, pady=10)

    def create_reset_button(self):
        reset_button = tk.Button(self.root, text="Reset", font=('Arial', 18, 'bold'), command=self.reset)
        reset_button.grid(row=9, column=5, pady=10)

    def create_timer_label(self):
        self.timer_label = tk.Label(self.root, text="Time: 0.00s", font=('Arial', 18, 'bold'))
        self.timer_label.grid(row=10, column=4, pady=10)

    def create_status_label(self):
        self.status_label = tk.Label(self.root, text="Status: Ready", font=('Arial', 18, 'bold'))
        self.status_label.grid(row=11, column=4, pady=10)

    def solve(self):
        self.disable_entries()
        self.status_label.config(text="Status: Solving...")
        self.root.update_idletasks()  # Update the GUI to reflect the status change
        initial_board = self.get_board()
        print("Initial board:")
        print(initial_board)
        if self.is_valid_board(initial_board):
            start_time = time.time()
            solved_board = initial_board.copy()
            if self.solve_sudoku(solved_board):
                end_time = time.time()
                elapsed_time = end_time - start_time
                self.timer_label.config(text=f"Time: {elapsed_time:.2f}s")
                print("Solved board:")
                print(solved_board)
                self.update_board(initial_board, solved_board)
                self.status_label.config(text="Status: Solved")
            else:
                print("No solution found.")
                self.status_label.config(text="Status: No solution found")

    def reset(self):
        self.status_label.config(text="Status: Ready")
        self.timer_label.config(text="Time: 0.00s")
        for i in range(9):
            for j in range(9):
                self.entries[i][j].config(state='normal')
                self.entries[i][j].delete(0, tk.END)
                self.entries[i][j].config(fg='black')

    def disable_entries(self):
        for row in self.entries:
            for entry in row:
                entry.config(state='disabled')

    def enable_entries(self):
        for row in self.entries:
            for entry in row:
                entry.config(state='normal')

    def get_board(self):
        board = np.zeros((9, 9), dtype=int)
        for i in range(9):
            for j in range(9):
                value = self.entries[i][j].get()
                if value.isdigit():
                    board[i][j] = int(value)
        return board

    def is_valid_board(self, board):
        # Add validation logic if needed
        return True

    def solve_sudoku(self, board):
        empty = self.find_empty(board)
        if not empty:
            return True  # Puzzle solved
        row, col = empty
        print(f"Trying to solve cell ({row}, {col})")

        for num in range(1, 10):
            if self.is_safe(board, row, col, num):
                board[row][col] = num
                print(f"Placed {num} at ({row}, {col})")
                if self.solve_sudoku(board):
                    return True
                board[row][col] = 0
                print(f"Backtracked at ({row}, {col})")

        return False  # Trigger backtracking

    def find_empty(self, board):
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    print(f"Found empty cell at ({i}, {j})")
                    return (i, j)
        return None

    def is_safe(self, board, row, col, num):
        for i in range(9):
            if board[row][i] == num or board[i][col] == num:
                return False
        box_row, box_col = row // 3 * 3, col // 3 * 3
        for i in range(3):
            for j in range(3):
                if board[box_row + i][box_col + j] == num:
                    return False
        return True

    def update_board(self, initial_board, solved_board):
        for i in range(9):
            for j in range(9):
                if initial_board[i][j] == 0:
                    self.entries[i][j].config(state='normal')
                    self.entries[i][j].delete(0, tk.END)
                    self.entries[i][j].insert(0, str(solved_board[i][j]))
                    self.entries[i][j].config(state='disabled', fg='blue')

if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuSolverApp(root)
    root.mainloop()