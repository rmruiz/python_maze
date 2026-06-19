# Python Maze

A small Python maze generator and solver with graphical visualization using `easygraphics`.

## Project overview

This project creates random mazes using several generation algorithms and solves them using breadth-first search. It includes a simple graphical view to draw walls, visited cells, and the solution path.

## Features

- Maze generation algorithms:
  - Depth-first search (`dfs`)
  - Prim's algorithm (`prim`)
  - Kruskal's algorithm (`kruskal`)
  - Wilson's algorithm (`wilson`)
- Breadth-first search solver for shortest path finding
- Grid-based maze representation with separate wall and cell state storage
- Easy color-based rendering of maze cells and start/end positions

## Requirements

- Python 3.11
- `easygraphics`

Install dependencies with:

```bash
pip install -r requirements.txt
```

## Usage

Run the application with:

```bash
python run.py
```

The program generates a maze, draws it, then solves it and displays the solution.

### Configuration

Edit `run.py` to change:

- `MAZE_ALGORITHM` to one of `dfs`, `prim`, `kruskal`, `wilson`
- `CANVAS` size for rendering
- `maze_size` in `mainloop()` for maze dimensions
- `DEBUG`, `STEPBYSTEP`, and `STEPBYSTEP2` flags for debugging and step-by-step rendering

## Project structure

- `run.py` - application entry point and high-level control flow
- `maze.py` - `Maze` class and maze generation logic
- `maze_solver.py` - `MazeSolver` class and pathfinding logic
- `maze_view.py` - rendering logic using `easygraphics`
- `grid.py` - reusable boolean grid storage class
- `vector.py` - immutable 2D vector helper class
- `requirements.txt` - project dependencies
- `config.txt` - setup notes for local Python environment and dependencies

## Design notes

- The maze is represented as a grid of cells with separate south and east wall grids.
- The solver traverses the maze graph using open passages between cells.
- The renderer draws walls and optionally highlights the path, start, and end positions.

## Extending the project

Possible improvements:

- add additional solver algorithms such as A* or DFS
- add unit tests for generation and solving
- support command-line arguments for maze size and algorithm selection
- improve the UI to animate generation and solution steps

## License

This project is released under the MIT License. Feel free to reuse and modify it.
