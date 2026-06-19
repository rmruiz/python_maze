from easygraphics import pause, easy_run, close_graph, set_caption, RenderMode, clear_device, is_run, init_graph, delay_fps, set_render_mode
from math import floor
import time

from map import Map
from maze_solver import MazeSolver
from maze_view import MazeView
from vector import Vector

DEBUG = False
STEPBYSTEP = False
STEPBYSTEP2 = False
MARGIN = 5

CANVAS = Vector(640, 480)
max_width = 640
max_height = 480

def debug(string):
    if DEBUG: print(string)

def mainloop():
    maze_size = Vector(15, 15)
    maze = Map(maze_size, CANVAS)
    view = MazeView(maze, CANVAS, margin=MARGIN)

    start_position = Vector(0, 0)
    stack = [start_position]
    maze.visited[start_position] = True

    while is_run() and stack:
        current_position = stack.pop()
        if maze.has_any_neighbor(current_position):
            stack.append(current_position)
            next_position = maze.next_neighbor(current_position)
            maze.remove_wall_between(current_position, next_position)
            maze.visited[next_position] = True
            stack.append(next_position)

        if STEPBYSTEP:
            delay_fps(1000)
            clear_device()
            view.draw()

    clear_device()
    view.draw()
    pause()

    debug("Solving maze")
    start_node = Vector(0, 0)
    end_node = Vector(maze_size.x - 1, maze_size.y - 1)
    solver = MazeSolver(maze)
    solver.solve(start_node, end_node)

    view.draw()
    pause()


def main():
    init_graph(max_width + 2*MARGIN, max_height + 2*MARGIN)
    set_render_mode(RenderMode.RENDER_MANUAL)
    set_caption("Maze builder")
    mainloop()
    pause()
    close_graph()

if __name__ == "__main__":
    easy_run(main)

