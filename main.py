from graphics import Line, Point, Window
from cell import Cell
from maze import Maze


def main():
    win = Window(800, 600)
    maze = Maze(65, 65, 12, 12, 50, 50, win, 12)
    maze.solve()
    win.wait_for_close()


main()
