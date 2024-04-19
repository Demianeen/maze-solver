from typing import List, Tuple
from cell import Cell
import random
import time


class Maze:
    def __init__(
        self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win=None, seed=None
    ):
        self.__x1 = x1
        self.__y1 = y1
        self.__num_rows = num_rows
        self.__num_columns = num_cols
        self.__cell_size_x = cell_size_x
        self.__cell_size_y = cell_size_y
        self.__win = win
        if seed is not None:
            self.__seed = seed
        else:
            self.__seed = random.random()
        random.seed(self.__seed)

        self.__create_cells()
        self.__break_entrance_and_exit()
        self.__break_walls_r(0, 0)
        self.__reset_cells_visited()

    def __create_cells(self):
        self.__cell_matrix: List[List[Cell]] = []
        for col_num in range(self.__num_columns):
            self.__cell_matrix.append([])
            for row_num in range(self.__num_rows):
                new_cell = Cell(self.__win)
                self.__cell_matrix[col_num].append(new_cell)
                self.__draw_cell(col_num, row_num)

    def __draw_cell(self, column: int, row: int):
        cell: Cell = self.__cell_matrix[column][row]
        x1 = self.__x1 + row * self.__cell_size_x
        y1 = self.__y1 + column * self.__cell_size_y
        x2 = x1 + self.__cell_size_x
        y2 = y1 + self.__cell_size_y
        cell.draw(x1, y1, x2, y2)
        self.__animate()

    def __animate(self):
        if self.__win is None:
            return
        self.__win.redraw()
        time.sleep(0.05)

    def __break_entrance_and_exit(self):
        self.__cell_matrix[0][0].has_top_wall = False
        self.__draw_cell(0, 0)
        self.__cell_matrix[-1][-1].has_bottom_wall = False
        self.__draw_cell(self.__num_columns - 1, self.__num_rows - 1)

    def __get_not_visited_moves(self, column: int, row: int):
        possible_moves: List[Tuple[int, int]] = []

        if column > 0:
            possible_moves.append((column - 1, row))
        if column < self.__num_columns - 1:
            possible_moves.append((column + 1, row))

        if row > 0:
            possible_moves.append((column, row - 1))
        if row < self.__num_rows - 1:
            possible_moves.append((column, row + 1))

        not_visited_moves = list(
            filter(
                lambda m: not self.__cell_matrix[m[0]][m[1]].visited,
                possible_moves,
            )
        )

        return not_visited_moves

    def __break_walls_between(
        self, column: int, row: int, next_column: int, next_row: int
    ):
        if next_column == column + 1:
            self.__cell_matrix[column][row].has_bottom_wall = False
            self.__cell_matrix[column + 1][row].has_top_wall = False
        if next_column == column - 1:
            self.__cell_matrix[column][row].has_top_wall = False
            self.__cell_matrix[column - 1][row].has_bottom_wall = False

        if next_row == row + 1:
            self.__cell_matrix[column][row].has_right_wall = False
            self.__cell_matrix[column][row + 1].has_left_wall = False
        if next_row == row - 1:
            self.__cell_matrix[column][row].has_left_wall = False
            self.__cell_matrix[column][row - 1].has_right_wall = False

    def __break_walls_r(self, column: int, row: int):
        self.__cell_matrix[column][row].visited = True
        while True:
            not_visited_moves = self.__get_not_visited_moves(column, row)
            if len(not_visited_moves) == 0:
                self.__draw_cell(column, row)
                return
            move = random.choice(not_visited_moves)
            self.__cell_matrix[move[0]][move[1]].visited = True
            self.__break_walls_between(column, row, *move)

            self.__break_walls_r(*move)

    def __reset_cells_visited(self):
        for column in range(self.__num_columns):
            for row in range(self.__num_rows):
                self.__cell_matrix[column][row].visited = False

    def __is_there_blocking_wall(
        self, column: int, row: int, next_column: int, next_row: int
    ):
        if next_column == column + 1:
            return (
                self.__cell_matrix[column][row].has_bottom_wall
                or self.__cell_matrix[next_column][row].has_top_wall
            )
        if next_column == column - 1:
            return (
                self.__cell_matrix[column][row].has_top_wall
                or self.__cell_matrix[next_column][row].has_bottom_wall
            )
        if next_row == row + 1:
            return (
                self.__cell_matrix[column][row].has_right_wall
                or self.__cell_matrix[column][next_row].has_left_wall
            )
        if next_row == row - 1:
            return (
                self.__cell_matrix[column][row].has_left_wall
                or self.__cell_matrix[column][next_row].has_right_wall
            )

        return False

    def __solve_r(self, column: int, row: int):
        self.__animate()
        current_cell: Cell = self.__cell_matrix[column][row]
        current_cell.visited = True
        if column == self.__num_columns - 1 and row == self.__num_rows - 1:
            return True

        not_visited_moves = self.__get_not_visited_moves(column, row)
        possible_moves = list(
            filter(
                lambda m: not self.__is_there_blocking_wall(column, row, *m),
                not_visited_moves,
            )
        )
        for move in possible_moves:
            next_cell = self.__cell_matrix[move[0]][move[1]]
            current_cell.draw_move(next_cell)
            is_found = self.__solve_r(*move)
            if is_found:
                return True
            current_cell.draw_move(next_cell, undo=True)

        return False

    def solve(self):
        return self.__solve_r(0, 0)
