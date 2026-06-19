from __future__ import annotations

from dataclasses import dataclass

@dataclass(frozen=True)
class Vector:
    x: int = 0
    y: int = 0

    def __repr__(self) -> str:
        return f"Vector(x={self.x}, y={self.y})"

    def __str__(self) -> str:
        return f"[{self.x}, {self.y}]"

    def north(self) -> Vector:
        return Vector(self.x, self.y - 1)

    def south(self) -> Vector:
        return Vector(self.x, self.y + 1)

    def east(self) -> Vector:
        return Vector(self.x + 1, self.y)

    def west(self) -> Vector:
        return Vector(self.x - 1, self.y)

    def __add__(self, other: Vector) -> Vector:
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Vector) -> Vector:
        return Vector(self.x - other.x, self.y - other.y)
          