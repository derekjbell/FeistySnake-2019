from astar import AStar
from helper import Helper

class State_Defend():

    # width = data.get("width")
    # height = data.get("height")
    # food = data.get("food").get("data") #Array
    # snakes = data.get("snakes").get("data") #Array
    # you = data.get("you")
    # myHealth = you.get("health")
    # myLength = you.get("body").get("length")
    # mySnake = you.get("body").get("data")
    # myID = you.get("id")

    def __init__(self):
        self.name = "defend state"

    def get_move(self, grid_data, data):
        self.height = data.get("height")
        self.width = data.get("width")
        self.pathfinder = AStar(grid_data[0], self.width, self.height)
        self.grid_data = grid_data
        self.data = data
        self.head_x = data.get("you").get("body").get("data")[0].get("x")
        self.head_y = data.get("you").get("body").get("data")[0].get("y")

        move = move_to_food()

        #NOTE FIND TAIL MODE
        if len(mySnake) > 3 and myHealth > 75 or move == None: #85
            gonnaGrow = False
            if myHealth == 100:
                gonnaGrow = True
            move = chase_tail(gonnaGrow)

        if move:
            return move
        else:
            neighbours = Helper.get_neighbors((head_x, head_y), grid_data[0], height, width)
            if neighbours:
                return Helper.get_move_letter((head_x, head_y), neighbours[0])
            else:
                return 'left'


    def move_to_food(self):
        food_list = self.grid_data[1]
        current_minimum = float('inf')
        current_path = None
        for food in food_list:
            path = self.pathfinder.compute_path((self.head_x, self.head_y), tuple(food))
            if path:
                path = list(path)
                if len(path) < current_minimum:
                    current_minimum = len(path)
                    current_path = path
        if current_path:
            return Helper.get_move_letter((self.head_x, self.head_y), list(current_path)[1])
        return None

    def chase_tail(self, isGonnaGrow):
        my_tail = (self.data.get("you").get("body").get("data")[-1].get("x"), self.data.get("you").get("body").get("data")[-1].get("y"))
        self.grid_data[0][my_tail[1]][my_tail[0]] = 1
        path = self.pathfinder.compute_path((self.head_x, self.head_y), my_tail)
        self.grid_data[0][my_tail[1]][my_tail[0]] = 0
        if path:
            if not isGonnaGrow:
                return get_move_letter((head_x, head_y), list(path)[1])
            else:
                neighbours = Helper.get_neighbors(my_tail, grid_options[0], self.height, self.width)
                for neighbour in neighbours:
                    path = self.pathfinder.compute_path((self.head_x, self.head_y), neighbour)
                    if path:
                        return Helper.get_move_letter((self.head_x, self.head_y), list(path)[1])
        return None
