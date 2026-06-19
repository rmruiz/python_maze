from easygraphics import draw_circle, set_fill_color, Color, draw_polygon, draw_poly_line, set_color
from math import floor

from vector import Vector

MARGIN = 5
max_width = 640
max_height = 480

class MazeView:
    def __init__(self, maze):
        self.maze = maze

    def draw_cell(self, pos):
        cell_height = floor(max_height / self.maze.size.y)
        cell_width = floor(max_width / self.maze.size.x)
        x0 = pos.x * cell_width + MARGIN
        x1 = (pos.x + 1) * cell_width + MARGIN
        y0 = pos.y * cell_height + MARGIN
        y1 = (pos.y + 1) * cell_height + MARGIN

        if self.maze.cell_has_south_wall(pos):
            set_color(Color.DARK_BLUE)
            draw_poly_line(x0, y1, x1, y1)
        else:
            set_color(Color.WHITE)
            draw_poly_line(x0, y1, x1, y1)

        if self.maze.cell_has_east_wall(pos):
            set_color(Color.DARK_BLUE)
            draw_poly_line(x1, y1, x1, y0)
        else:
            set_color(Color.WHITE)
            draw_poly_line(x1, y1, x1, y0)

    def draw_ball(self, pos):
        x0 = int(pos.x * self.maze.cell_width() + MARGIN + self.maze.cell_width() / 2)
        y0 = int(pos.y * self.maze.cell_height() + MARGIN + self.maze.cell_height() / 2)
        radius = int(min(self.maze.cell_width(), self.maze.cell_height()) / 3)
        set_color(Color.RED)
        set_fill_color(Color.RED)
        draw_circle(x0, y0, radius)

    def draw_result(self, pos):
        set_color(Color.RED)
        set_fill_color(Color.RED)
        margin = 2
        x0 = int(pos.x * self.maze.cell_width() + MARGIN + margin)
        y0 = int(pos.y * self.maze.cell_height() + MARGIN + margin)
        x1 = int(x0 + self.maze.cell_width() - 2 * margin)
        y1 = int(y0 + self.maze.cell_height() - 2 * margin)
        draw_polygon(x0, y0, x0, y1, x1, y1, x1, y0)

    def draw_border(self):
        set_color(Color.BLACK)
        set_fill_color(Color.WHITE)
        cell_height = floor(max_height / self.maze.size.y)
        cell_width = floor(max_width / self.maze.size.x)
        x0 = MARGIN
        x1 = self.maze.size.x * cell_width + MARGIN
        y0 = MARGIN
        y1 = self.maze.size.y * cell_height + MARGIN
        draw_polygon(x0, y0, x0, y1, x1, y1, x1, y0)

    def draw(self):
        self.draw_border()
        for x in range(self.maze.size.x):
            for y in range(self.maze.size.y):
                pos = Vector(x, y)
                self.draw_cell(pos)
                if self.maze.solucion.get(pos):
                    self.draw_ball(pos)
