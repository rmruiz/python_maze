from __future__ import annotations

from typing import Tuple, Union

from vector import Vector

class Grid:
    def __init__(self, size: Vector, value: bool = False) -> None:
        self.size: Vector = size
        self.data: list[list[bool]] = self._create_grid(value)

    def _create_grid(self, value: bool) -> list[list[bool]]:
        return [[value for _ in range(self.size.x)] for _ in range(self.size.y)]

    @property
    def width(self) -> int:
        return self.size.x

    @property
    def height(self) -> int:
        return self.size.y

    def _pos_to_coords(self, pos: Union[Vector, Tuple[int, int]]) -> Tuple[int, int]:
        if isinstance(pos, Vector):
            return pos.x, pos.y
        return pos

    def in_bounds(self, pos: Union[Vector, Tuple[int, int]]) -> bool:
        x, y = self._pos_to_coords(pos)
        return 0 <= x < self.size.x and 0 <= y < self.size.y

    def __getitem__(self, pos: Union[Vector, Tuple[int, int]]) -> bool:
        x, y = self._pos_to_coords(pos)
        return self.data[y][x]

    def __setitem__(self, pos: Union[Vector, Tuple[int, int]], value: bool) -> None:
        x, y = self._pos_to_coords(pos)
        self.data[y][x] = value

    def set(self, pos: Union[Vector, Tuple[int, int]], value: bool) -> None:
        self[pos] = value

    def get(self, pos: Union[Vector, Tuple[int, int]]) -> bool:
        return self[pos]
