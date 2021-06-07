from easygraphics import draw_circle, pause, easy_run, close_graph, set_fill_color, set_caption, Color, RenderMode, draw_polygon, draw_poly_line, set_color, clear_device, is_run, init_graph, delay_fps, set_render_mode
from random import randint
from math import floor
from time import sleep

from grid import Grid
from vector import Vector

VISITED = 4
SOUTH = 2
EAST = 1

DEBUG = False
STEPBYSTEP = False
STEPBYSTEP2 = True
MARGIN = 5

max_width = 640
max_height = 480

def make_full_grid(width, height):
    return [[7 for i in range(width)] for j in range(height)]

def debug(string):
    if DEBUG: print(string)

def get_grid(x,y):
    return grid[y][x]

def set_grid(x, y, value):
    grid[y][x] = value
    return

def cell_was_visited(pos):
    return False if get_grid(pos.x, pos.y) >= VISITED else True

def visit(pos):
    if get_grid(pos.x, pos.y) >= VISITED:
        debug("marcando como visitado [" + str(pos.x) + ", " + str(pos.y) + "]")
        set_grid(pos.x, pos.y, get_grid(pos.x, pos.y) - VISITED)
    return

def cell_has_south_wall(i, j):
    if j == len(grid) - 1: return False 
    tmp = get_grid(i, j)
    tmp = tmp - VISITED if tmp >= VISITED else tmp
    return True if tmp >= SOUTH else False

def cell_has_east_wall(i, j):
    if i == len(grid[0]) - 1: return False 
    tmp = get_grid(i, j)
    tmp = tmp - VISITED if tmp >= VISITED else tmp
    tmp = tmp - SOUTH if tmp >= SOUTH else tmp
    return True if tmp >= EAST else False

def cell_has_east_neighbor(cell):
    if cell.x == len(grid[0]) - 1: 
        return False
    return not cell_was_visited(cell.east())

def cell_has_west_neighbor(cell):
    if cell.x == 0:
        return False
    return not cell_was_visited(cell.west())

def cell_has_north_neighbor(cell):
    if cell.y == 0: 
        return False
    return not cell_was_visited(cell.north())

def cell_has_south_neighbor(cell):
    if cell.y == len(grid) - 1: 
        return False
    return not cell_was_visited(cell.south())

def north(xy): return [xy[0], xy[1]-1]
def south(xy): return [xy[0], xy[1]+1]
def east(xy): return [xy[0]+1, xy[1]]
def west(xy): return [xy[0]-1, xy[1]]

def remove_wall_between(xi,yi, xf,yf):
    xyi=[xi,yi]
    pos_i = Vector(xi, yi)
    xyf=[xf,yf]
    if(  xf == north(xyi)[0] and yf == north(xyi)[1]): destroy_north_wall(pos_i)
    elif(xf == south(xyi)[0] and yf == south(xyi)[1]): destroy_south_wall(pos_i)
    elif(xf == east(xyi)[0]  and yf == east(xyi)[1]):  destroy_east_wall(pos_i)
    elif(xf == west(xyi)[0]  and yf == west(xyi)[1]):  destroy_west_wall(pos_i)
    else: raise("no match to remove wall!")
    return

def destroy_south_wall(pos):
    tmp = get_grid(pos.x, pos.y)
    tmp = tmp - VISITED if tmp >= VISITED else tmp
    if tmp >= SOUTH:
        debug("destroying south wall [" + str(pos.x) + ", " + str(pos.y) + "]")
        set_grid(pos.x, pos.y, get_grid(pos.x, pos.y) - SOUTH)

def destroy_east_wall(pos):
    tmp = get_grid(pos.x, pos.y)
    tmp = tmp - VISITED if tmp >= VISITED else tmp
    tmp = tmp - SOUTH if tmp >= SOUTH else tmp
    if tmp >= EAST:
        debug("destroying east wall [" + str(pos.x) + ", " + str(pos.y) + "]")
        set_grid(pos.x, pos.y, get_grid(pos.x, pos.y) - EAST)

def destroy_north_wall(pos):
    debug("destroying north wall [" + str(pos.x) + ", " + str(pos.y) + "]")
    destroy_south_wall(pos.north())

def destroy_west_wall(pos):
    debug("destroying west wall [" + str(pos.x) + ", " + str(pos.y) + "]")
    destroy_east_wall(pos.west())

def draw_cell(i, j):
    cell_height = floor(max_height/len(grid))
    cell_width = floor(max_width/len(grid[0]))
    x0 = i * cell_width + MARGIN
    x1 = (i+1) * cell_width + MARGIN
    y0 = j * cell_height + MARGIN
    y1 = (j+1) * cell_height + MARGIN
    
    if cell_has_south_wall(i, j): 
        set_color(Color.DARK_BLUE)
        draw_poly_line(  x0,y1,  x1,y1  )
    else: 
        set_color(Color.WHITE)
        draw_poly_line(  x0,y1,  x1,y1  )
    if cell_has_east_wall(i, j):
        set_color(Color.DARK_BLUE)
        draw_poly_line(  x1,y1,  x1,y0  )
    else: 
        set_color(Color.WHITE)
        draw_poly_line(  x1,y1,  x1,y0  )
    #if cell_was_visited(i, j):
    #    set_color(Color.RED)
    #    draw_poly_line(  x0,y0,  x1,y1  )
    #    draw_poly_line(  x0,y1,  x1,y0  )


def draw_ball(i, j):
    cell_height = floor(max_height/len(grid))
    cell_width = floor(max_width/len(grid[0]))
    x0 = i * cell_width + MARGIN + cell_width/2
    y0 = j * cell_height + MARGIN + cell_height/2
    set_color(Color.RED)
    set_fill_color(Color.RED)
    draw_circle(x0, y0, min(cell_width, cell_height)/4 - 2 )

def draw():
    draw_border()
    x_range = range(len(grid[0]))
    y_range = range(len(grid))

    for i in x_range:
        for j in y_range:
            pos = Vector(i, j)
            draw_cell(i, j)
            if solucion.get(pos): 
                draw_ball(i, j)
    return

def draw_border():
    set_color(Color.BLACK)
    set_fill_color(Color.WHITE)
    cell_height = floor(max_height/len(grid))
    cell_width = floor(max_width/len(grid[0]))
    x0 = 0 + MARGIN
    x1 = len(grid[0]) * cell_width + MARGIN
    y0 = 0 + MARGIN
    y1 = len(grid) * cell_height + MARGIN
    draw_polygon( x0,y0, x0,y1, x1,y1, x1,y0) 

def has_any_neighbor(pos):
    if cell_has_east_neighbor(pos): return True
    if cell_has_west_neighbor(pos): return True
    if cell_has_north_neighbor(pos): return True
    if cell_has_south_neighbor(pos): return True
    debug("no neighbor found for [" + str(pos.x) + ", " + str(pos.y) + "]")
    return False

def next_neighbor(x, y):
    neighbors = []
    xy=[x,y]
    cell = Vector(x, y)
    if cell_has_east_neighbor(cell): neighbors.append(east(xy))
    if cell_has_west_neighbor(cell): neighbors.append(west(xy))
    if cell_has_north_neighbor(cell): neighbors.append(north(xy))
    if cell_has_south_neighbor(cell): neighbors.append(south(xy))
    
    next = randint(0, len(neighbors)-1) 
    debug("neighbor selected: " + str(neighbors[next]))
    return neighbors[next]

grid = []
solucion = None
def mainloop():
    global grid, solucion
    maze_size = Vector(15, 12)
    width = maze_size.x
    height = maze_size.y
    
    grid = make_full_grid(width, height)
    solucion = Grid(maze_size, False)

    xi = randint(0, len(grid)-1)
    yi = len(grid) - 1
    stack = []
    stack.append([xi, yi])
    pos_i = Vector(xi, yi)
    visit(pos_i)
    while is_run():
        if(len(stack) == 0): 
            clear_device()
            draw()
            pause()
            break
        while(len(stack)>0):
            #sleep(1)
            xi, yi = stack.pop()
            pos_i = Vector(xi, yi)
            if(has_any_neighbor(pos_i)):
                stack.append([xi, yi])
                xn, yn = next_neighbor(xi, yi)
                remove_wall_between(xi,yi,xn,yn)
                pos_n = Vector(xn, yn)
                visit(pos_n)
                stack.append([xn, yn])

            if(STEPBYSTEP):
                delay_fps(1000)            
                clear_device()
                draw()

    debug("Solving maze")
    start_node = Vector(0, 0)
    end_node = Vector(maze_size.x - 1, maze_size.y - 1)
    stack_search(start_node, end_node)
        
    draw()
    pause()

def stack_search(start, end):
    start_node = [start.x, start.y]
    end_node = [end.x, end.y]
    stack = []
    dead_end = []
    stack.append(start_node)

    found = False
    solucion.set(start, True)
    
    while(not found):
        if(STEPBYSTEP2):
            draw()
            delay_fps(1000) 
        current=stack.pop()
        curr = Vector(current[0], current[1])
        solucion.set(curr, False)
        if curr.is_equal_to(Vector(end_node[0],end_node[1])):
            stack.append(current)
            solucion.set(curr, True)
            found = True
        else:
            debug("pushing current " + str(current))
            stack.append(current)
            solucion.set(curr, True)
            can_move = False
            if can_move_north(curr) and north(current) not in stack and north(current) not in dead_end:    
                debug("pushing current N" + str(north(current)))
                stack.append(north(current))
                can_move = True
            if can_move_south(curr) and south(current) not in stack and south(current) not in dead_end:
                debug("pushing current S" + str(south(current)))
                stack.append(south(current))
                can_move = True
            if can_move_east(curr) and east(current) not in stack and east(current) not in dead_end:
                debug("pushing current E" + str(east(current)))
                stack.append(east(current))
                can_move = True
            if can_move_west(curr) and west(current) not in stack and west(current) not in dead_end:
                debug("pushing current W"+ str(west(current)))
                stack.append(west(current))
                can_move = True
            if not can_move:
                de = stack.pop()
                dead_end.append(de)
                solucion.set(Vector(de[0], de[1]), False)
                debug("Dead End " + str(de))
                
    return

def deep_search(sub_tree, end_node):
    draw()
    if(STEPBYSTEP2):
        delay_fps(1000) 
    debug("deep_search over ["+str(sub_tree.data[0])+","+str(sub_tree.data[1])+"]")
    if sub_tree.data[0] == end_node[0] and sub_tree.data[1] == end_node[1]:
        print("Found!")
        return True
    for child in sub_tree.children:
        child_pos = Vector(child.data[0], child.data[1])
        solucion.set(child_pos, True)
        if not deep_search(child, end_node): 
            debug("removing ["+str(sub_tree.data[0])+","+str(sub_tree.data[1])+"]")
            solucion.set(child_pos, False)
        else:
            return True
    return False

def can_move_east(pos):
    if pos.x == len(grid[0]) - 1: return False 
    tmp = get_grid(pos.x, pos.y)
    tmp = tmp - VISITED if tmp >= VISITED else tmp
    tmp = tmp - SOUTH if tmp >= SOUTH else tmp
    return False if tmp >= EAST else True

def can_move_south(pos):
    if pos.y == len(grid) - 1: return False 
    tmp = get_grid(pos.x, pos.y)
    tmp = tmp - VISITED if tmp >= VISITED else tmp
    return False if tmp >= SOUTH else True

def can_move_north(pos):
    if pos.y == 0: return False
    return can_move_south(pos.north())
    
def can_move_west(pos):
    if pos.x == 0: return False
    return can_move_east(pos.west())

def main():
    init_graph(max_width + 2*MARGIN, max_height + 2*MARGIN)
    set_render_mode(RenderMode.RENDER_MANUAL)
    set_caption("Maze builder")
    mainloop()
    close_graph()

easy_run(main)

