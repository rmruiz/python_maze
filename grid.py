from copy import deepcopy
from typing import Any

from vector import Vector

class Grid:
    def __init__(self, size: Vector, value: bool = False) -> None:
        self.size: Vector = size
        self.data: list[list[Any]] = self._create_grid(value)

    def _create_grid(self, value: bool) -> list[list[Any]]:
        return [[deepcopy(value) for _ in range(self.size.x)] for _ in range(self.size.y)]

    @property
    def width(self) -> int:
        return self.size.x

    @property
    def height(self) -> int:
        return self.size.y

    def _pos_to_coords(self, pos):
        if hasattr(pos, "x") and hasattr(pos, "y"):
            return pos.x, pos.y
        return pos

    def in_bounds(self, pos):
        x, y = self._pos_to_coords(pos)
        return 0 <= x < self.size.x and 0 <= y < self.size.y

    def __getitem__(self, pos):
        x, y = self._pos_to_coords(pos)
        return self.data[y][x]

    def __setitem__(self, pos, value):
        x, y = self._pos_to_coords(pos)
        self.data[y][x] = value

    def set(self, pos, value):
        self[pos] = value

    def get(self, pos):
        return self[pos]
