from astar import AStar
import helper

class State_Defend():

    def __init__(self):
        self.name = "defend state"
        self.helper = None

    def get_move(self, grid_data, data):
        self.height = data.get("board").get("height")
        self.width = data.get("board").get("width")
        self.head_x = data.get("you").get("body")[0].get("x")
        self.head_y = data.get("you").get("body")[0].get("y")
        self.my_snake_health = data.get("you").get("health")
        self.my_snake_length = len(data.get("you").get("body"))
        self.pathfinder = AStar((self.head_x, self.head_y), grid_data[0], self.width, self.height)
        self.grid_data = grid_data
        self.data = data

        move = self.move_to_food()

        #NOTE FIND TAIL MODE
        if self.my_snake_length > 3 and self.my_snake_health > 65 or move == None:
            move = self.chase_tail(self.my_snake_health == 100)

        if move:
            return move
        else:
            backup_moves = self.helper.get_backup_move((self.head_x, self.head_y), self.grid_data[0], self.height, self.width)
            if backup_moves:
                return self.helper.get_move_letter((self.head_x, self.head_y), backup_moves[0])
            else:
                return 'up'


    def move_to_food(self):
        food_list = self.grid_data[1]
        current_minimum = float('inf')
        current_path = None
        for food in food_list:
            path = self.pathfinder.compute_path(tuple(food))
            if path:
                path = list(path)
                if len(path) < current_minimum:
                    current_minimum = len(path)
                    current_path = path
        if current_path and self.helper.is_good_move(current_path[1], self.grid_data[0], self.my_snake_length):
            return self.helper.get_move_letter((self.head_x, self.head_y), list(current_path)[1])

    def chase_tail(self, snake_growing):
        my_tail = (self.data.get("you").get("body")[-1].get("x"), self.data.get("you").get("body")[-1].get("y"))
        self.grid_data[0][my_tail[1]][my_tail[0]] = 1
        path = self.pathfinder.compute_path(my_tail)
        self.grid_data[0][my_tail[1]][my_tail[0]] = -1

        if path:
            danger_tail_move = (path[1] == (self.data.get("you").get("body")[-1].get("x"), self.data.get("you").get("body")[-1].get("y")) and self.tail_is_in_danger())
            if not danger_tail_move:
                if not snake_growing:
                    return self.helper.get_move_letter((self.head_x, self.head_y), list(path)[1])
                else:
                    neighbours = self.helper.get_neighbors(my_tail, self.grid_data[0], self.height, self.width)
                    for neighbour in neighbours:
                        path = self.pathfinder.compute_path(neighbour)
                        if path:
                            return self.helper.get_move_letter((self.head_x, self.head_y), list(path)[1])

    def tail_is_in_danger(self):
        my_tail = (self.data.get("you").get("body")[-1].get("x"), self.data.get("you").get("body")[-1].get("y"))
        for snake in self.data.get("board").get("snakes"):
            (x, y) = (snake.get("body")[0].get("x"), snake.get("body")[0].get("y"))
            moves = [(nx, ny) for nx, ny in[(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)] if 0 <= nx < self.width and 0 <= ny < self.height]
            if my_tail in moves:
                return False
        return True
