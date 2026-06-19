import logging

from easygraphics import pause, easy_run, close_graph, set_caption, RenderMode, clear_device, is_run, init_graph, delay_fps, set_render_mode

from maze import Maze
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

logger = logging.getLogger(__name__)

def debug(string: str) -> None:
    logger.debug(string)

def mainloop() -> None:
    maze_size = Vector(15, 15)
    maze = Maze(maze_size, CANVAS, debug=DEBUG)
    view = MazeView(maze, CANVAS, margin=MARGIN)

    def step():
        delay_fps(1000)
        clear_device()
        view.draw()

    if STEPBYSTEP:
        maze.generate(Vector(0, 0), step_callback=step)
    else:
        maze.generate(Vector(0, 0))

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


def main() -> None:
    logging.basicConfig(level=logging.DEBUG if DEBUG else logging.INFO)
    init_graph(max_width + 2*MARGIN, max_height + 2*MARGIN)
    set_render_mode(RenderMode.RENDER_MANUAL)
    set_caption("Maze builder")
    mainloop()
    pause()
    close_graph()

if __name__ == "__main__":
    easy_run(main)

