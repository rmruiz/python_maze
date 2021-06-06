from easygraphics import draw_circle, pause, easy_run, close_graph, set_fill_color, set_caption, Color, RenderMode, draw_polygon, draw_poly_line, set_color, clear_device, is_run, init_graph, delay_fps, set_render_mode
from random import randint
from math import floor
from time import sleep

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

def make_solucion(width, height):
    return [[False for i in range(width)] for j in range(height)]

def debug(string):
    if DEBUG: print(string)

def get_grid(x,y):
    return grid[y][x]

def set_grid(x, y, value):
    grid[y][x] = value
    return

def cell_was_visited(i, j):
    return False if get_grid(i, j) >= VISITED else True

def visit(i, j):
    if get_grid(i, j) >= VISITED:
        debug("marcando como visitado i:" + str(i) + " j:" + str(j))
        set_grid(i, j, get_grid(i, j) - VISITED)
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

def cell_has_east_neighbor(i, j):
    if i == len(grid[0]) - 1: 
        return False
    return not cell_was_visited(i+1, j)

def cell_has_west_neighbor(i, j):
    if i == 0:
        return False
    return not cell_was_visited(i-1, j)

def cell_has_north_neighbor(i, j):
    if j == 0: 
        return False
    return not cell_was_visited(i, j-1)

def cell_has_south_neighbor(i, j):
    if j == len(grid) - 1: 
        return False
    return not cell_was_visited(i, j+1)

def north(xy): return [xy[0], xy[1]-1]
def south(xy): return [xy[0], xy[1]+1]
def east(xy): return [xy[0]+1, xy[1]]
def west(xy): return [xy[0]-1, xy[1]]

def remove_wall_between(xi,yi, xf,yf):
    xyi=[xi,yi]
    xyf=[xf,yf]
    if(  xf == north(xyi)[0] and yf == north(xyi)[1]): destroy_north_wall(xi,yi)
    elif(xf == south(xyi)[0] and yf == south(xyi)[1]): destroy_south_wall(xi,yi)
    elif(xf == east(xyi)[0]  and yf == east(xyi)[1]):  destroy_east_wall(xi,yi)
    elif(xf == west(xyi)[0]  and yf == west(xyi)[1]):  destroy_west_wall(xi,yi)
    else: raise("no match to remove wall!")
    return

def destroy_south_wall(i, j):
    tmp = get_grid(i, j)
    tmp = tmp - VISITED if tmp >= VISITED else tmp
    if tmp >= SOUTH:
        debug("destroying south wall i:" + str(i) + " j:" + str(j))
        set_grid(i, j, get_grid(i, j) - SOUTH)

def destroy_east_wall(i, j):
    tmp = get_grid(i, j)
    tmp = tmp - VISITED if tmp >= VISITED else tmp
    tmp = tmp - SOUTH if tmp >= SOUTH else tmp
    if tmp >= EAST:
        debug("destroying east wall i:" + str(i) + " j:" + str(j))
        set_grid(i, j, get_grid(i, j) - EAST)

def destroy_north_wall(i, j):
    #debug("destroying north wall i:" + str(i) + " j:" + str(j))
    destroy_south_wall(i, j-1)

def destroy_west_wall(i, j):
    #debug("destroying west wall i:" + str(i) + " j:" + str(j))
    destroy_east_wall(i-1, j)

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
          draw_cell(i, j)
          if get_solucion(i, j): 
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

def has_any_neighbor(x, y):
    if cell_has_east_neighbor(x, y): return True
    if cell_has_west_neighbor(x, y): return True
    if cell_has_north_neighbor(x, y): return True
    if cell_has_south_neighbor(x, y): return True
    #debug("no neighbor found for x:" + str(x) + " y:" + str(y))
    return False

def next_neighbor(x, y):
    neighbors = []
    xy=[x,y]
    if cell_has_east_neighbor(x, y): neighbors.append(east(xy))
    if cell_has_west_neighbor(x, y): neighbors.append(west(xy))
    if cell_has_north_neighbor(x, y): neighbors.append(north(xy))
    if cell_has_south_neighbor(x, y): neighbors.append(south(xy))
    
    next = randint(0, len(neighbors)-1) 
    debug("neighbor selectd: " + str(neighbors[next]))
    return neighbors[next]

grid = []
solucion = []
def mainloop():
    global grid, solucion
    width = 64
    height = 48
    
    grid = make_full_grid(width, height)
    solucion = make_solucion(width, height)

    xi = randint(0, len(grid)-1)
    yi = len(grid) - 1
    stack = []
    stack.append([xi, yi])
    visit(xi, yi)
    while is_run():
        if(len(stack) == 0): 
            clear_device()
            draw()
            pause()
            break
        while(len(stack)>0):
            #sleep(1)
            xi, yi = stack.pop()
            if(has_any_neighbor(xi, yi)):
                stack.append([xi, yi])
                xn, yn = next_neighbor(xi, yi)
                remove_wall_between(xi,yi,xn,yn)
                visit(xn, yn)
                stack.append([xn, yn])

            if(STEPBYSTEP):
                delay_fps(1000)            
                clear_device()
                draw()

    debug("Solving maze")
    start_node = [0, 0]
    end_node = [width-1,height-1]
    #tree = build_tree_from(start_node, None)
    #set_solucion(tree.data, tree.data, True)
    #deep_search(tree, end_node)
    stack_search(start_node, end_node)
        
    draw()
    pause()

def stack_search(start_node, end_node):
    stack = []
    dead_end = []
    stack.append(start_node)

    found = False
    set_solucion(start_node, True)
    
    while(not found):
        if(STEPBYSTEP2):
            draw()
            delay_fps(1000) 
        current=stack.pop()
        set_solucion(current, False)
        if same(current, end_node):
            stack.append(current)
            set_solucion(current, True)
            found = True
        else:
            debug("pushing current " + str(current))
            stack.append(current)
            set_solucion(current, True)
            can_move = False
            if can_move_north(current[0], current[1]) and north(current) not in stack and north(current) not in dead_end:    
                debug("pushing current N" + str(north(current)))
                stack.append(north(current))
                can_move = True
            if can_move_south(current[0], current[1]) and south(current) not in stack and south(current) not in dead_end:
                debug("pushing current S" + str(south(current)))
                stack.append(south(current))
                can_move = True
            if can_move_east(current[0], current[1]) and east(current) not in stack and east(current) not in dead_end:
                debug("pushing current E" + str(east(current)))
                stack.append(east(current))
                can_move = True
            if can_move_west(current[0], current[1]) and west(current) not in stack and west(current) not in dead_end:
                debug("pushing current W"+ str(west(current)))
                stack.append(west(current))
                can_move = True
            if not can_move:
                de = stack.pop()
                dead_end.append(de)
                set_solucion(de, False)
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
        set_solucion(child.data[0], child.data[1], True)
        if not deep_search(child, end_node): 
            debug("removing ["+str(sub_tree.data[0])+","+str(sub_tree.data[1])+"]")
            set_solucion(child.data[0], child.data[1], False)
        else:
            return True
    return False

def get_solucion(x, y):
    return solucion[y][x]

def set_solucion(xy, value):
    solucion[xy[1]][xy[0]] = value
    return

class Node:
    def __init__(self, data = None):
        self.children = []
        self.data = data

def same(ij, xy):
    if xy == None: return False
    if ij[0] != xy[0]: return False
    if ij[1] != xy[1]: return False
    return True

def build_tree_from(xy, last_visited):
    node = Node()
    node.data = xy
    node.children = []
    if can_move_north(xy[0], xy[1]):
        if not same(north(xy[0], xy[1]), last_visited): 
            debug("going north:")
            debug(north(xy[0], xy[1]))
            node.children.append(build_tree_from(north(xy[0], xy[1]), xy))
    if can_move_south(xy[0], xy[1]):
        if not same(south(xy[0], xy[1]), last_visited): 
            debug("going south:")
            debug(south(xy[0], xy[1]))
            node.children.append(build_tree_from(south(xy[0], xy[1]), xy))
    if can_move_east(xy[0], xy[1]):
        if not same(east(xy[0], xy[1]), last_visited): 
            debug("going east:")
            debug(east(xy[0], xy[1]))
            node.children.append(build_tree_from(east(xy[0], xy[1]), xy))
    if can_move_west(xy[0], xy[1]):
        if not same(west(xy[0], xy[1]), last_visited): 
            debug("going west:")
            debug(west(xy[0], xy[1]))
            node.children.append(build_tree_from(west(xy[0], xy[1]), xy))
    return node

def can_move_east(i, j):
    if i == len(grid[0]) - 1: return False 
    tmp = get_grid(i, j)
    tmp = tmp - VISITED if tmp >= VISITED else tmp
    tmp = tmp - SOUTH if tmp >= SOUTH else tmp
    return False if tmp >= EAST else True

def can_move_south(i, j):
    if j == len(grid) - 1: return False 
    tmp = get_grid(i, j)
    tmp = tmp - VISITED if tmp >= VISITED else tmp
    return False if tmp >= SOUTH else True

def can_move_north(i, j):
    if j == 0: return False
    return can_move_south(i, j-1)
    
def can_move_west(i, j):
    if i == 0: return False
    return can_move_east(i-1, j)

def main():
    init_graph(max_width + 2*MARGIN, max_height + 2*MARGIN)
    set_render_mode(RenderMode.RENDER_MANUAL)
    set_caption("Maze builder")
    mainloop()
    close_graph()

easy_run(main)

