class Vector:
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y

    def __str__(self):
        return "[" + str(self.x) + ", " + str(self.y) + "]"

    def is_equal_to(self, pos):
        if pos == None:
            return False
        if self.x == pos.x and self.y == pos.y:
            return True
        else:
            return False

    def north(self):
        return Vector(self.x, self.y - 1)

    def south(self):
        return Vector(self.x, self.y + 1)

    def east(self):
        return Vector(self.x + 1, self.y)

    def west(self):
        return Vector(self.x - 1, self.y)

    def in_list(self, list):
        for v in list:
            if self.is_equal_to(v): return True
        return False
          