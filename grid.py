class Grid:
    def __init__(self, size, value=False):
        self.size = size
        self.data = [[value for _ in range(size.x)] for _ in range(size.y)]

    def width(self):
        return self.size.x

    def height(self):
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
