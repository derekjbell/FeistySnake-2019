class State_Attack():

    def __init__(self):
        self.name = "attack state"

    def get_move(self, grid_options, data):
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
