import math, sys, random
import astar

def get_neighbors(node, lines, height, width):
    (x, y) = node #changed from x, y
    return[(nx, ny) for nx, ny in[(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)] if 0 <= nx < width and 0 <= ny < height and lines[ny][nx] == 1]


def move_to_food(a_star_object, food_list, head_x, head_y):
    current_minimum = float('inf')
    current_path = None
    for food in food_list:
        path = a_star_object.astar((head_x, head_y), tuple(food))
        if path:
            path = list(path)
            if len(path) < current_minimum:
                current_minimum = len(path)
                current_path = path
    if current_path:
        return get_move_letter((head_x, head_y), list(current_path)[1])
    return None

def chase_tail(a_star_object, grid_options, mySnake, head_x, head_y, isGonnaGrow, height, width):
    myTail = (mySnake[-1].get("x"), mySnake[-1].get("y"))
    grid_options[0][myTail[1]][myTail[0]] = 1
    path = a_star_object.astar((head_x, head_y), myTail)
    grid_options[0][myTail[1]][myTail[0]] = 0
    if path:
        if not isGonnaGrow:
            return get_move_letter((head_x, head_y), list(path)[1])
        else:
            neighbours = get_neighbors(myTail, grid_options[0], height, width)
            for neighbour in neighbours:
                path = a_star_object.astar((head_x, head_y), neighbour)
                if path:
                    return get_move_letter((head_x, head_y), list(path)[1])


    return None

def get_move(grid_options, target, head_x, head_y, height, width, mySnake, myHealth):
    a_star_object = astar.AStarAlgorithm(grid_options[0], width, height)

    myLength = len(mySnake)
    move = move_to_food(a_star_object, grid_options[1], head_x, head_y)

    #NOTE FIND TAIL MODE
    if myLength > 3 and myHealth > 75 or move == None: #85
        gonnaGrow = False
        if myHealth == 100:
            gonnaGrow = True
        move = chase_tail(a_star_object, grid_options, mySnake, head_x, head_y, gonnaGrow, height, width)


    if move:
        return move
    else:
        neighbours = get_neighbors((head_x, head_y), grid_options[0], height, width)
        if neighbours:
            return get_move_letter((head_x, head_y), neighbours[0])
        else:
            return 'left'
