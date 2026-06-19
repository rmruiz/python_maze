from dataclasses import dataclass

@dataclass(frozen=True)
class Vector:
    x: int = 0
    y: int = 0

    def __str__(self):
        return f"[{self.x}, {self.y}]"

    def is_equal_to(self, pos):
        return pos is not None and self == pos

    def north(self):
        return Vector(self.x, self.y - 1)

    def south(self):
        return Vector(self.x, self.y + 1)

    def east(self):
        return Vector(self.x + 1, self.y)

    def west(self):
        return Vector(self.x - 1, self.y)

    def in_list(self, sequence):
        return self in sequence
          