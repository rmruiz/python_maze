class Vector:
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y

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

#def north(xy): return [xy[0], xy[1]-1]
#def south(xy): return [xy[0], xy[1]+1]
#def east(xy): return [xy[0]+1, xy[1]]
#def west(xy): return [xy[0]-1, xy[1]]            