class Grid:
    def __init__(self, size, value = False):
        self.size = size
        self.data = [[value for i in range(size.x)] for j in range(size.y)]

    def width(self):
        return self.size.x

    def height(self):
        return self.size.y

    def set(self, pos, value):
        self.data[pos.y][pos.x] = value
        return

    def get(self, pos):
        return self.data[pos.y][pos.x]