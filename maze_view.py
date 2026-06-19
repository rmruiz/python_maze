from __future__ import annotations

from typing import Optional

from easygraphics import draw_circle, set_fill_color, Color, draw_polygon, draw_poly_line, set_color
from math import floor

from vector import Vector

class MazeView:
    def __init__(
        self,
        maze: Maze,
        canvas_size: Vector,
        margin: int = 5,
        show_visited: bool = False,
        start: Optional[Vector] = None,
        end: Optional[Vector] = None,
    ) -> None:
        self.maze = maze
        self.canvas_size = canvas_size
        self.margin = margin
        self.show_visited = show_visited
        self.start = start
        self.end = end

    @property
    def cell_width(self) -> int:
        return floor(self.canvas_size.x / self.maze.size.x)

    @property
    def cell_height(self) -> int:
        return floor(self.canvas_size.y / self.maze.size.y)

    def draw_cell(self, pos: Vector) -> None:
        x0 = pos.x * self.cell_width + self.margin
        x1 = (pos.x + 1) * self.cell_width + self.margin
        y0 = pos.y * self.cell_height + self.margin
        y1 = (pos.y + 1) * self.cell_height + self.margin

        if self.maze.cell_has_south_wall(pos):
            set_color(Color.DARK_BLUE)
            draw_poly_line(x0, y1, x1, y1)

        if self.maze.cell_has_east_wall(pos):
            set_color(Color.DARK_BLUE)
            draw_poly_line(x1, y1, x1, y0)

    def draw_visited_cell(self, pos: Vector) -> None:
        if not self.show_visited or not self.maze.visited[pos] or self.maze.solution[pos]:
            return

        fill_color = self._color_or_default("LIGHT_GRAY", Color.WHITE)
        set_fill_color(fill_color)
        set_color(fill_color)

        x0 = pos.x * self.cell_width + self.margin
        x1 = (pos.x + 1) * self.cell_width + self.margin
        y0 = pos.y * self.cell_height + self.margin
        y1 = (pos.y + 1) * self.cell_height + self.margin
        draw_polygon(x0, y0, x0, y1, x1, y1, x1, y0)

    def draw_ball(self, pos: Vector) -> None:
        x0 = int(pos.x * self.cell_width + self.margin + self.cell_width / 2)
        y0 = int(pos.y * self.cell_height + self.margin + self.cell_height / 2)
        radius = int(min(self.cell_width, self.cell_height) / 3)
        set_color(Color.RED)
        set_fill_color(Color.RED)
        draw_circle(x0, y0, radius)

    def draw_result(self, pos: Vector) -> None:
        fill_color = self._color_or_default("LIGHT_RED", Color.RED)
        set_fill_color(fill_color)
        set_color(Color.RED)

        x0 = int(pos.x * self.cell_width + self.margin + 2)
        y0 = int(pos.y * self.cell_height + self.margin + 2)
        x1 = int(x0 + self.cell_width - 4)
        y1 = int(y0 + self.cell_height - 4)
        draw_polygon(x0, y0, x0, y1, x1, y1, x1, y0)
        draw_poly_line(x0, y0, x1, y0, x1, y1, x0, y1, x0, y0)

    def draw_start_end(self) -> None:
        start_pos = self.start or Vector(0, 0)
        end_pos = self.end or Vector(self.maze.size.x - 1, self.maze.size.y - 1)
        self._draw_highlight(start_pos, self._color_or_default("GREEN", Color.BLACK))
        self._draw_highlight(end_pos, self._color_or_default("BLUE", Color.BLACK))

    def _draw_highlight(self, pos: Vector, color: Color) -> None:
        x0 = int(pos.x * self.cell_width + self.margin + self.cell_width / 2)
        y0 = int(pos.y * self.cell_height + self.margin + self.cell_height / 2)
        radius = int(min(self.cell_width, self.cell_height) / 4)
        set_color(color)
        set_fill_color(color)
        draw_circle(x0, y0, radius)

    def _color_or_default(self, name: str, default: Color) -> Color:
        return getattr(Color, name, default)

    def draw_border(self) -> None:
        set_color(Color.BLACK)
        set_fill_color(Color.WHITE)
        x0 = self.margin
        x1 = self.maze.size.x * self.cell_width + self.margin
        y0 = self.margin
        y1 = self.maze.size.y * self.cell_height + self.margin
        draw_polygon(x0, y0, x0, y1, x1, y1, x1, y0)

    def draw(self) -> None:
        self.draw_border()
        for pos in self.maze.all_positions():
            self.draw_visited_cell(pos)
            self.draw_cell(pos)
            if self.maze.solution[pos]:
                self.draw_result(pos)
        self.draw_start_end()
