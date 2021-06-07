from grid import Grid
from random import randint
from math import floor

class Map:
    def __init__(self, size, canvas_size):
        self.size = size
        self.canvas_size = canvas_size
        self.south_walls = Grid(size, True)
        self.east_walls = Grid(size, True)
        self.visitado = Grid(size, False)
        self.solucion = Grid(size, False)
        self.DEBUG = True

    def cell_has_south_wall(self, pos):
        return self.south_walls.get(pos)

    def cell_has_east_wall(self, pos):
        return self.east_walls.get(pos)

    def debug(self, string):
        if self.DEBUG: print(string)
    
    def next_neighbor(self, pos):
        neighbors = []
        if self.cell_has_east_neighbor(pos): neighbors.append(pos.east())
        if self.cell_has_west_neighbor(pos): neighbors.append(pos.west())
        if self.cell_has_north_neighbor(pos): neighbors.append(pos.north())
        if self.cell_has_south_neighbor(pos): neighbors.append(pos.south())
        
        next = randint(0, len(neighbors) - 1) 
        self.debug("neighbor selected: " + str(neighbors[next]))
        return neighbors[next]

    def cell_has_east_neighbor(self, cell):
        if cell.x == self.size.x - 1: 
            return False
        return not self.visitado.get(cell.east())

    def cell_has_west_neighbor(self, cell):
        if cell.x == 0:
            return False
        return not self.visitado.get(cell.west())

    def cell_has_north_neighbor(self, cell):
        if cell.y == 0: 
            return False
        return not self.visitado.get(cell.north())

    def cell_has_south_neighbor(self, cell):
        if cell.y == self.size.y - 1: 
            return False
        return not self.visitado.get(cell.south())

    def remove_wall_between(self, pos_i, pos_f):
        if   pos_f.is_equal_to(pos_i.north()): self.destroy_north_wall(pos_i)
        elif pos_f.is_equal_to(pos_i.south()): self.destroy_south_wall(pos_i)
        elif pos_f.is_equal_to(pos_i.east()):  self.destroy_east_wall(pos_i)
        elif pos_f.is_equal_to(pos_i.west()):  self.destroy_west_wall(pos_i)
        else: raise("ERROR: No match to remove wall!")
        return

    def destroy_south_wall(self, pos):
        self.debug("destroying south wall " + str(pos))
        self.south_walls.set(pos, False)
        
    def destroy_east_wall(self, pos):
        self.debug("destroying east wall " + str(pos))
        self.east_walls.set(pos, False)

    def destroy_north_wall(self, pos):
        self.debug("destroying north wall " + str(pos))
        self.destroy_south_wall(pos.north())

    def destroy_west_wall(self, pos):
        self.debug("destroying west wall " + str(pos))
        self.destroy_east_wall(pos.west())

    def has_any_neighbor(self, pos):
        if self.cell_has_east_neighbor(pos): return True
        if self.cell_has_west_neighbor(pos): return True
        if self.cell_has_north_neighbor(pos): return True
        if self.cell_has_south_neighbor(pos): return True
        self.debug("no neighbor found for " + str(pos))
        return False

    def can_move_east(self, pos):
        if pos.x == self.size.x - 1: return False 
        return not self.east_walls.get(pos)

    def can_move_south(self, pos):
        if pos.y == self.size.y - 1: return False 
        return not self.south_walls.get(pos)

    def can_move_north(self, pos):
        if pos.y == 0: return False
        return self.can_move_south(pos.north())
        
    def can_move_west(self, pos):
        if pos.x == 0: return False
        return self.can_move_east(pos.west())

    def cell_width(self):
        return floor(self.canvas_size.x/self.size.x)
    
    def cell_height(self):
        return floor(self.canvas_size.y/self.size.y)
    