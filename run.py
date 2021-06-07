from easygraphics import draw_circle, pause, easy_run, close_graph, set_fill_color, set_caption, Color, RenderMode, draw_polygon, draw_poly_line, set_color, clear_device, is_run, init_graph, delay_fps, set_render_mode
from math import floor

from map import Map
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

def draw_cell(pos):
    cell_height = floor(max_height/maze.size.y)
    cell_width = floor(max_width/maze.size.x)
    x0 = pos.x * cell_width + MARGIN
    x1 = (pos.x+1) * cell_width + MARGIN
    y0 = pos.y * cell_height + MARGIN
    y1 = (pos.y+1) * cell_height + MARGIN
    
    if maze.cell_has_south_wall(pos): 
        set_color(Color.DARK_BLUE)
        draw_poly_line(  x0,y1,  x1,y1  )
    else: 
        set_color(Color.WHITE)
        draw_poly_line(  x0,y1,  x1,y1  )
    if maze.cell_has_east_wall(pos):
        set_color(Color.DARK_BLUE)
        draw_poly_line(  x1,y1,  x1,y0  )
    else: 
        set_color(Color.WHITE)
        draw_poly_line(  x1,y1,  x1,y0  )

def draw_ball(pos):
    x0 = pos.x * maze.cell_width() + MARGIN + maze.cell_width()/2
    y0 = pos.y * maze.cell_height() + MARGIN + maze.cell_height()/2
    set_color(Color.RED)
    set_fill_color(Color.RED)
    draw_circle(x0, y0, min(maze.cell_width(), maze.cell_height())/3 )

def draw_result(pos):
    set_color(Color.RED)
    set_fill_color(Color.RED)
    margin = 2
    x0 = pos.x * maze.cell_width() + MARGIN + margin
    y0 = pos.y * maze.cell_height() + MARGIN + margin
    x1 = x0 + maze.cell_width() - 2*margin
    y1 = y0 + maze.cell_height() - 2*margin
    draw_polygon( x0,y0, x0,y1, x1,y1, x1,y0 )

def draw():
    draw_border()
    
    for x in range(maze.size.x):
        for y in range(maze.size.y):
            pos = Vector(x, y)
            draw_cell(pos)
            if maze.solucion.get(pos): 
                draw_ball(pos)
    return

def draw_border():
    set_color(Color.BLACK)
    set_fill_color(Color.WHITE)
    cell_height = floor(max_height/maze.size.y)
    cell_width = floor(max_width/maze.size.x)
    x0 = 0 + MARGIN
    x1 = maze.size.x * cell_width + MARGIN
    y0 = 0 + MARGIN
    y1 = maze.size.y * cell_height + MARGIN
    draw_polygon( x0,y0, x0,y1, x1,y1, x1,y0) 

maze = None

def mainloop():
    global maze
    maze_size = Vector(15, 15)  
    maze = Map(maze_size, CANVAS)
    
    pos_i = Vector(0, 0)
    stack = []
    stack.append(pos_i)
    maze.visitado.set(pos_i, True)
    while is_run():
        if(len(stack) == 0): 
            clear_device()
            draw()
            pause()
            break
        while(len(stack)>0):
            #sleep(1)
            pos_i = stack.pop()
            if(maze.has_any_neighbor(pos_i)):
                stack.append(pos_i)
                pos_n = maze.next_neighbor(pos_i)
                maze.remove_wall_between(pos_i, pos_n)
                maze.visitado.set(pos_n, True)
                stack.append(pos_n)

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
    stack = []
    dead_end = []
    stack.append(start)

    found = False
    maze.solucion.set(start, True)
    
    while(not found):
        if(STEPBYSTEP2):
            draw()
            delay_fps(1000) 
        current=stack.pop()
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
    close_graph()

easy_run(main)

