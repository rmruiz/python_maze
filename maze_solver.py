from collections import deque

from vector import Vector

class MazeSolver:
    def __init__(self, maze):
        self.maze = maze

    def solve(self, start: Vector, end: Vector, method: str = "bfs"):
        self._clear_solution()
        if method == "bfs":
            return self._solve_bfs(start, end)
        raise ValueError(f"Unsupported solver method: {method}")

    def _clear_solution(self):
        for y in range(self.maze.size.y):
            for x in range(self.maze.size.x):
                self.maze.solucion[Vector(x, y)] = False

    def _solve_bfs(self, start: Vector, end: Vector):
        queue = deque([start])
        parents = {start: None}
        visited = {start}

        while queue:
            current = queue.popleft()
            if current == end:
                return self._reconstruct_path(parents, end)

            for neighbor in self._neighbors(current):
                if neighbor in visited:
                    continue
                visited.add(neighbor)
                parents[neighbor] = current
                queue.append(neighbor)

        return []

    def _neighbors(self, pos: Vector):
        neighbors = []
        if self.maze.can_move_north(pos):
            neighbors.append(pos.north())
        if self.maze.can_move_south(pos):
            neighbors.append(pos.south())
        if self.maze.can_move_east(pos):
            neighbors.append(pos.east())
        if self.maze.can_move_west(pos):
            neighbors.append(pos.west())
        return neighbors

    def _reconstruct_path(self, parents, end: Vector):
        path = []
        current = end
        while current is not None:
            path.append(current)
            current = parents[current]
        path.reverse()

        for pos in path:
            self.maze.solucion[pos] = True

        return path
