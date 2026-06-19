import logging
from typing import Callable, List, Optional

from grid import Grid
from random import choice, shuffle
from vector import Vector

logger = logging.getLogger(__name__)

class Maze:
    def __init__(self, size: Vector, canvas_size: Vector, debug: bool = True) -> None:
        self.size: Vector = size
        self.canvas_size: Vector = canvas_size
        self.south_walls: Grid = Grid(size, True)
        self.east_walls: Grid = Grid(size, True)
        self.visited: Grid = Grid(size, False)
        self.solution: Grid = Grid(size, False)
        self.debug_enabled: bool = debug

    def generate(
        self,
        start_position: Optional[Vector] = None,
        algorithm: str = "dfs",
        step_callback: Optional[Callable[[], None]] = None,
    ) -> None:
        if start_position is None:
            start_position = Vector(0, 0)

        self.south_walls = Grid(self.size, True)
        self.east_walls = Grid(self.size, True)
        self.visited = Grid(self.size, False)
        self.solution = Grid(self.size, False)

        self.debug(f"generating maze with algorithm={algorithm}")

        if algorithm == "dfs":
            self._generate_dfs(start_position, step_callback)
        elif algorithm == "prim":
            self._generate_prim(start_position, step_callback)
        elif algorithm == "kruskal":
            self._generate_kruskal(step_callback)
        elif algorithm == "wilson":
            self._generate_wilson(start_position, step_callback)
        else:
            raise ValueError(f"Unsupported maze generation algorithm: {algorithm}")

    def in_bounds(self, pos: Vector) -> bool:
        return self.visited.in_bounds(pos)

    def all_positions(self) -> list[Vector]:
        return [Vector(x, y) for y in range(self.size.y) for x in range(self.size.x)]

    def cell_has_south_wall(self, pos: Vector) -> bool:
        return self.south_walls[pos]

    def cell_has_east_wall(self, pos: Vector) -> bool:
        return self.east_walls[pos]

    def debug(self, string: str) -> None:
        if self.debug_enabled:
            logger.debug(string)
    
    def next_neighbor(self, pos: Vector) -> Optional[Vector]:
        neighbors = [
            pos.east(),
            pos.west(),
            pos.north(),
            pos.south(),
        ]
        candidates = [neighbor for neighbor in neighbors if self.in_bounds(neighbor) and not self.visited[neighbor]]

        if not candidates:
            return None

        self._shuffle_neighbors(candidates)
        selected = candidates[0]
        self.debug("neighbor selected: " + str(selected))
        return selected

    def _shuffle_neighbors(self, neighbors: list[Vector]) -> None:
        shuffle(neighbors)

    def _adjacent_cells(self, pos: Vector) -> list[Vector]:
        return [
            neighbor
            for neighbor in [pos.north(), pos.south(), pos.east(), pos.west()]
            if self.in_bounds(neighbor)
        ]

    def _unvisited_adjacent(self, pos: Vector) -> list[Vector]:
        return [neighbor for neighbor in self._adjacent_cells(pos) if not self.visited[neighbor]]

    def _generate_dfs(
        self,
        start_position: Vector,
        step_callback: Optional[Callable[[], None]] = None,
    ) -> None:
        stack: list[Vector] = [start_position]
        self.visited[start_position] = True

        while stack:
            current_position = stack.pop()
            if self.has_any_neighbor(current_position):
                stack.append(current_position)
                next_position = self.next_neighbor(current_position)
                self.remove_wall_between(current_position, next_position)
                self.visited[next_position] = True
                stack.append(next_position)

            if step_callback is not None:
                step_callback()

    def _generate_prim(
        self,
        start_position: Vector,
        step_callback: Optional[Callable[[], None]] = None,
    ) -> None:
        frontier: list[tuple[Vector, Vector]] = []
        self.visited[start_position] = True
        self._add_frontier_edges(start_position, frontier)

        while frontier:
            current, neighbor = choice(frontier)
            frontier.remove((current, neighbor))
            if self.visited[neighbor]:
                continue

            self.remove_wall_between(current, neighbor)
            self.visited[neighbor] = True
            self._add_frontier_edges(neighbor, frontier)

            if step_callback is not None:
                step_callback()

    def _add_frontier_edges(self, cell: Vector, frontier: list[tuple[Vector, Vector]]) -> None:
        for neighbor in self._adjacent_cells(cell):
            if not self.visited[neighbor]:
                frontier.append((cell, neighbor))

    def _generate_kruskal(self, step_callback: Optional[Callable[[], None]] = None) -> None:
        parents = {pos: pos for pos in self.all_positions()}

        def find(pos: Vector) -> Vector:
            while parents[pos] != pos:
                pos = parents[pos]
            return pos

        def union(a: Vector, b: Vector) -> None:
            parents[find(a)] = find(b)

        edges: list[tuple[Vector, Vector]] = []
        for pos in self.all_positions():
            for neighbor in [pos.east(), pos.south()]:
                if self.in_bounds(neighbor):
                    edges.append((pos, neighbor))

        shuffle(edges)

        for pos, neighbor in edges:
            if find(pos) != find(neighbor):
                union(pos, neighbor)
                self.remove_wall_between(pos, neighbor)
                self.visited[pos] = True
                self.visited[neighbor] = True

                if step_callback is not None:
                    step_callback()

    def _generate_wilson(
        self,
        start_position: Vector,
        step_callback: Optional[Callable[[], None]] = None,
    ) -> None:
        tree: set[Vector] = {start_position}
        self.visited[start_position] = True
        remaining = [pos for pos in self.all_positions() if pos not in tree]

        while remaining:
            current = choice(remaining)
            path: list[Vector] = [current]
            path_index = {current: 0}

            while path[-1] not in tree:
                next_cell = choice(self._adjacent_cells(path[-1]))
                if next_cell in path_index:
                    cut = path_index[next_cell]
                    path = path[: cut + 1]
                    path_index = {cell: idx for idx, cell in enumerate(path)}
                else:
                    path.append(next_cell)
                    path_index[next_cell] = len(path) - 1

            for first, second in zip(path, path[1:]):
                self.remove_wall_between(first, second)
                self.visited[first] = True
                self.visited[second] = True

            tree.update(path)
            remaining = [pos for pos in remaining if pos not in tree]

            if step_callback is not None:
                step_callback()

    def cell_has_east_neighbor(self, cell: Vector) -> bool:
        return self.in_bounds(cell.east()) and not self.visited[cell.east()]

    def cell_has_west_neighbor(self, cell: Vector) -> bool:
        return self.in_bounds(cell.west()) and not self.visited[cell.west()]

    def cell_has_north_neighbor(self, cell: Vector) -> bool:
        return self.in_bounds(cell.north()) and not self.visited[cell.north()]

    def cell_has_south_neighbor(self, cell: Vector) -> bool:
        return self.in_bounds(cell.south()) and not self.visited[cell.south()]

    def remove_wall_between(self, from_pos: Vector, to_pos: Vector) -> None:
        if   to_pos == from_pos.north(): self.destroy_north_wall(from_pos)
        elif to_pos == from_pos.south(): self.destroy_south_wall(from_pos)
        elif to_pos == from_pos.east():  self.destroy_east_wall(from_pos)
        elif to_pos == from_pos.west():  self.destroy_west_wall(from_pos)
        else: raise RuntimeError("ERROR: No match to remove wall!")

    def destroy_south_wall(self, pos: Vector) -> None:
        self.debug("destroying south wall " + str(pos))
        self.south_walls[pos] = False
        
    def destroy_east_wall(self, pos: Vector) -> None:
        self.debug("destroying east wall " + str(pos))
        self.east_walls[pos] = False

    def destroy_north_wall(self, pos: Vector) -> None:
        self.debug("destroying north wall " + str(pos))
        self.destroy_south_wall(pos.north())

    def destroy_west_wall(self, pos: Vector) -> None:
        self.debug("destroying west wall " + str(pos))
        self.destroy_east_wall(pos.west())

    def has_any_neighbor(self, pos: Vector) -> bool:
        if self.cell_has_east_neighbor(pos): return True
        if self.cell_has_west_neighbor(pos): return True
        if self.cell_has_north_neighbor(pos): return True
        if self.cell_has_south_neighbor(pos): return True
        self.debug("no neighbor found for " + str(pos))
        return False

    def can_move_east(self, pos: Vector) -> bool:
        if pos.x == self.size.x - 1: return False
        return not self.east_walls[pos]

    def can_move_south(self, pos: Vector) -> bool:
        if pos.y == self.size.y - 1: return False
        return not self.south_walls[pos]

    def can_move_north(self, pos: Vector) -> bool:
        if pos.y == 0: return False
        return self.can_move_south(pos.north())
        
    def can_move_west(self, pos: Vector) -> bool:
        if pos.x == 0: return False
        return self.can_move_east(pos.west())
    