from easygraphics import draw_circle, set_fill_color, Color, draw_polygon, draw_poly_line, set_color
from math import floor

from vector import Vector

class MazeView:
    def __init__(self, maze, canvas_size, margin=5):
        self.maze = maze
        self.canvas_size = canvas_size
        self.margin = margin
        self.cell_width = floor(canvas_size.x / maze.size.x)
        self.cell_height = floor(canvas_size.y / maze.size.y)

    def draw_cell(self, pos):
        x0 = pos.x * self.cell_width + self.margin
        x1 = (pos.x + 1) * self.cell_width + self.margin
        y0 = pos.y * self.cell_height + self.margin
        y1 = (pos.y + 1) * self.cell_height + self.margin

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
        x0 = int(pos.x * self.cell_width + self.margin + self.cell_width / 2)
        y0 = int(pos.y * self.cell_height + self.margin + self.cell_height / 2)
        radius = int(min(self.cell_width, self.cell_height) / 3)
        set_color(Color.RED)
        set_fill_color(Color.RED)
        draw_circle(x0, y0, radius)

    def draw_result(self, pos):
        set_color(Color.RED)
        set_fill_color(Color.RED)
        margin = 2
        x0 = int(pos.x * self.cell_width + self.margin + margin)
        y0 = int(pos.y * self.cell_height + self.margin + margin)
        x1 = int(x0 + self.cell_width - 2 * margin)
        y1 = int(y0 + self.cell_height - 2 * margin)
        draw_polygon(x0, y0, x0, y1, x1, y1, x1, y0)

    def draw_border(self):
        set_color(Color.BLACK)
        set_fill_color(Color.WHITE)
        x0 = self.margin
        x1 = self.maze.size.x * self.cell_width + self.margin
        y0 = self.margin
        y1 = self.maze.size.y * self.cell_height + self.margin
        draw_polygon(x0, y0, x0, y1, x1, y1, x1, y0)

    def draw(self):
        self.draw_border()
        for pos in self.maze.all_positions():
            self.draw_cell(pos)
            if self.maze.solution[pos]:
                self.draw_result(pos)
