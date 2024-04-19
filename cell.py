from graphics import Line, Point


class Cell:
    def __init__(self, win=None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.__x1 = None
        self.__x2 = None
        self.__y1 = None
        self.__y2 = None
        self.__win = win
        self.visited = False

    def draw(self, x1, y1, x2, y2):
        self.__x1 = x1
        self.__x2 = x2
        self.__y1 = y1
        self.__y2 = y2
        if self.__win is None:
            return

        line = Line(Point(x1, y1), Point(x1, y2))
        if self.has_left_wall:
            self.__win.draw_line(line)
        else:
            # otherwise the wall will remain drawn even if we don't draw it again
            self.__win.draw_line(line, "white")

        line = Line(Point(x1, y1), Point(x2, y1))
        if self.has_top_wall:
            self.__win.draw_line(line)
        else:
            self.__win.draw_line(line, "white")

        line = Line(Point(x2, y1), Point(x2, y2))
        if self.has_right_wall:
            self.__win.draw_line(line)
        else:
            self.__win.draw_line(line, "white")

        line = Line(Point(x1, y2), Point(x2, y2))
        if self.has_bottom_wall:
            self.__win.draw_line(line)
        else:
            self.__win.draw_line(line, "white")

    def draw_move(self, other_cell: "Cell", undo=False):
        if (
            self.__x1 is None
            or self.__x2 is None
            or self.__y1 is None
            or self.__y2 is None
            or other_cell.__x1 is None
            or other_cell.__x2 is None
            or other_cell.__y1 is None
            or other_cell.__y2 is None
        ):
            raise Exception("You need to draw the cell first")

        if self.__win is None:
            return

        center_x = (self.__x1 + self.__x2) / 2
        center_y = (self.__y1 + self.__y2) / 2
        current_cell_center = Point(center_x, center_y)

        other_center_x = (other_cell.__x1 + other_cell.__x2) / 2
        other_center_y = (other_cell.__y1 + other_cell.__y2) / 2
        other_cell_center = Point(other_center_x, other_center_y)

        move_line = Line(current_cell_center, other_cell_center)
        color = "black"
        if undo:
            color = "gray"
        self.__win.draw_line(move_line, color)
