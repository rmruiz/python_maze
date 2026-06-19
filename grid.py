class Grid:
    def __init__(self, size, value=False):
        self.size = size
        self.data = [[value for _ in range(size.x)] for _ in range(size.y)]

    def width(self):
        return self.size.x

    def height(self):
        return self.size.y

    def __getitem__(self, pos):
        if hasattr(pos, "x") and hasattr(pos, "y"):
            return self.data[pos.y][pos.x]
        x, y = pos
        return self.data[y][x]

    def __setitem__(self, pos, value):
        if hasattr(pos, "x") and hasattr(pos, "y"):
            self.data[pos.y][pos.x] = value
        else:
            x, y = pos
            self.data[y][x] = value

    def set(self, pos, value):
        self[pos] = value

    def get(self, pos):
        return self[pos]
