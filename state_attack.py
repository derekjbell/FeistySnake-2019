import helper
from astar import AStar
import math


class State_Attack():

    def __init__(self):
        self.name = "attack state"
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

        snakes = data.get("board").get("snakes")
        head = (self.head_x, self.head_y)

        # find closest snake ID
        target_snake_id = self.find_closest_snake_head(snakes)

        # Guard to make sure our snake doesn't just starve
        if self.my_snake_health < 40:
            return self.default_behaviour()

        if target_snake_id:
            return self.attack_snake_head(snakes, target_snake_id)
        else:
            return self.default_behaviour()

    def find_closest_snake_head(self, snakes):
        current_minimum = float('inf')
        current_path = None
        current_id = None
        for snake in snakes:
            if snake.get("id") == self.data.get("you").get("id"):
                continue
            enemy_head_x = snake.get("body")[0].get("x")
            enemy_head_y = snake.get("body")[0].get("y")
            dist = self.helper.get_crows_dist((self.head_x, self.head_y), (enemy_head_x, enemy_head_y))
            if dist < current_minimum:
                current_minimum = dist
                current_id = snake.get("id")
        return current_id

    def attack_snake_head(self, snakes, target_id):
        target_snake = None
        # Find target snake data
        for snake in snakes:
            if snake.get("id") == target_id:
                target_snake = snake.get("body")

                target_position = self.get_danger_squares(target_snake)
                if target_position:
                    #If there is some point in the snakes' danger zone, go to it
                    target_y = target_position[1]
                    target_x = target_position[0]

                    old_val = self.grid_data[0][target_y][target_x]

                    self.grid_data[0][target_y][target_x] = 1;
                    target_move = self.move_to_food([target_position])

                    self.grid_data[0][target_y][target_x] = old_val;

                    return target_move
                else:
                    return self.default_behaviour()

    # Return the first entry of possible danger squares around a snakes' head
    def get_danger_squares(self, target_snake):
        available_moves = []
        head_x = target_snake[0].get("x")
        head_y = target_snake[0].get("y")

        top = head_y - 1
        bottom = head_y + 1
        left = head_x - 1
        right = head_x + 1

        if top >= 0 and self.grid_data[0][top][head_x] != 0:
            available_moves.append((head_x, top))
        if bottom < self.height and self.grid_data[0][bottom][head_x] != 0:
            available_moves.append((head_x, bottom))
        if left >= 0 and self.grid_data[0][head_y][left] != 0:
            available_moves.append((left, head_y))
        if right < self.width and self.grid_data[0][head_y][right] != 0:
            available_moves.append((right, head_y))
        if len(available_moves) > 0:
            return available_moves[0]
        else:
            return None

    # This needs to get changed to a uniquely named method, and altered to do less...
    def move_to_food(self, food_list):
        current_minimum = float('inf')
        current_path = None
        for food in food_list:
            path = self.pathfinder.compute_path(tuple(food))
            if path:
                path = list(path)
                if len(path) < current_minimum:
                    current_minimum = len(path)
                    current_path = path
        if current_path and self.helper.is_good_move(list(current_path)[1], self.grid_data[0], self.my_snake_length):
            #TODO figure out how to stop two competing SNAKES from trying to take the same square
            return self.helper.get_move_letter((self.head_x, self.head_y), list(current_path)[1])
        else:
            backup_moves = self.helper.get_backup_move((self.head_x, self.head_y), self.grid_data[0], self.height, self.width)
            if backup_moves:
                return self.helper.get_move_letter((self.head_x, self.head_y), backup_moves[0])
            else:
                return 'up'

    def default_behaviour(self):
        move = self.move_to_food(self.grid_data[1])
        #NOTE FIND TAIL MODE
        if move:
            return move
            # There should ALWAYS be a move since move_to_food has all the guards
        else:
            backup_moves = self.helper.get_backup_move((self.head_x, self.head_y), self.grid_data[0], self.height, self.width)
            if backup_moves:
                return self.helper.get_move_letter((self.head_x, self.head_y), backup_moves[0])
            else:
                return 'up'
