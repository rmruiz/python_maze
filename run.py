from easygraphics import pause, easy_run, close_graph, set_caption, RenderMode, set_color, clear_device, is_run, init_graph, delay_fps, set_render_mode
from math import floor
import time

from map import Map
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
    view = MazeView(maze)

    pos_i = Vector(0, 0)
    stack = [pos_i]
    maze.visitado.set(pos_i, True)

    while is_run():
        if len(stack) == 0:
            clear_device()
            view.draw()
            pause()
            break

        while len(stack) > 0:
            pos_i = stack.pop()
            if maze.has_any_neighbor(pos_i):
                stack.append(pos_i)
                pos_n = maze.next_neighbor(pos_i)
                maze.remove_wall_between(pos_i, pos_n)
                maze.visitado.set(pos_n, True)
                stack.append(pos_n)

            if STEPBYSTEP:
                delay_fps(1000)
                clear_device()
                view.draw()

    debug("Solving maze")
    start_node = Vector(0, 0)
    end_node = Vector(maze_size.x - 1, maze_size.y - 1)
    stack_search(start_node, end_node, maze, view)

    view.draw()
    pause()

def stack_search(start, end, maze, view=None):
    stack = []
    dead_end = []
    stack.append(start)

    found = False
    maze.solucion.set(start, True)
    
    while not found:
        if STEPBYSTEP2 and view is not None:
            view.draw()
            delay_fps(1000)
        current = stack.pop()
        maze.solucion.set(current, False)

        if current.is_equal_to(end):
            stack.append(current)
            maze.solucion.set(current, True)
            found = True
        else:
            debug("pushing current " + str(current))
            stack.append(current)
            maze.solucion.set(current, True)
            can_move = False
            if maze.can_move_north(current) and not current.north().in_list(stack) and not current.north().in_list(dead_end):
                debug("pushing current N " + str(current.north()))
                stack.append(current.north())
                can_move = True
            if maze.can_move_south(current) and not current.south().in_list(stack) and not current.south().in_list(dead_end):
                debug("pushing current S " + str(current.south()))
                stack.append(current.south())
                can_move = True
            if maze.can_move_east(current) and not current.east().in_list(stack) and not current.east().in_list(dead_end):
                debug("pushing current E " + str(current.east()))
                stack.append(current.east())
                can_move = True
            if maze.can_move_west(current) and not current.west().in_list(stack) and not current.west().in_list(dead_end):
                debug("pushing current W " + str(current.west()))
                stack.append(current.west())
                can_move = True
            if not can_move:
                de = stack.pop()
                dead_end.append(de)
                maze.solucion.set(de, False)
                debug("Dead End: " + str(de))
    return

def main():
    init_graph(max_width + 2*MARGIN, max_height + 2*MARGIN)
    set_render_mode(RenderMode.RENDER_MANUAL)
    set_caption("Maze builder")
    mainloop()
    pause()
    close_graph()

if __name__ == "__main__":
    easy_run(main)

