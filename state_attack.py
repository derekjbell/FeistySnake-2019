from helper import Helper
from astar import AStar
import math


class State_Attack():

    def __init__(self):
        self.name = "attack state"
        self.helper = Helper()

    def get_move(self, grid_data, data):
        self.height = data.get("height")
        self.width = data.get("width")
        self.head_x = data.get("you").get("body").get("data")[0].get("x")
        self.head_y = data.get("you").get("body").get("data")[0].get("y")
        self.my_snake_health = data.get("you").get("health")
        self.my_snake_length = data.get("you").get("length")
        self.pathfinder = AStar((self.head_x, self.head_y), grid_data[0], self.width, self.height)
        self.grid_data = grid_data
        self.data = data

        snakes = data.get("snakes").get("data")
        head = (self.head_x, self.head_y)
        # find closest snake
        target_snake_id = self.path_to_head(snakes, head)

        if target_snake_id:
            target_snake = None
            # Find target snake data
            for snake in snakes:
                if snake.get("id") == target_snake_id:
                    target_snake = snake.get("body").get("data")

                    target_position = self.get_target_position(target_snake)
                    return self.move_to_food([target_position], head)
        else:
            move = self.move_to_food()

            #NOTE FIND TAIL MODE
            if self.my_snake_length > 3 and self.my_snake_health > 65 or move == None:
                move = self.chase_tail(self.my_snake_health == 100)

            if move:
                return move
            else:
                neighbours = self.helper.get_neighbors((self.head_x, self.head_y), self.grid_data[0], self.height, self.width)
                if neighbours:
                    return self.helper.get_move_letter((self.head_x, self.head_y), neighbours[0])
                else:
                    # All spots around the head are full, or are next to an opponents head
                    neighbours = self.helper.get_last_resort((self.head_x, self.head_y), self.grid_data[0], self.height, self.width)
                    if neighbours:
                        return self.helper.get_move_letter((self.head_x, self.head_y), neighbours[0])
                    else:
                        # Snake will almost certainly die
                        return 'up'

    def get_target_position(self, target_snake):
        delta_x = target_snake[0].get("x") - target_snake[1].get("x")
        delta_y = target_snake[0].get("y") - target_snake[1].get("y")
        target_x = 2*delta_x + target_snake[0].get("x")
        target_y = 2*delta_y + target_snake[0].get("y")
        return (target_x, target_y)

    def path_to_head(self, snakes, head):
        current_minimum = float('inf')
        current_path = None
        current_id = None
        for snake in snakes:
            if snake.get("id") == self.data.get("you").get("id"):
                continue
            enemy_head_x = snake.get("body").get("data")[0].get("x")
            enemy_head_y = snake.get("body").get("data")[0].get("y")
            dist = self.helper.get_crows_dist((self.head_x, self.head_y), (enemy_head_x, enemy_head_y))
            if dist < current_minimum:
                current_minimum = dist
                current_id = snake.get("id")
        return current_id

    def move_to_food(self, food_list, head):
        current_minimum = float('inf')
        current_path = None
        for food in food_list:
            path = self.pathfinder.compute_path(tuple(food))
            if path:
                path = list(path)
                if len(path) < current_minimum:
                    current_minimum = len(path)
                    current_path = path
        if current_path and len(current_path) > 1:
            #TODO figure out how to stop two competing SNAKES from trying to take the same square
            return self.helper.get_move_letter(head, list(current_path)[1])
        else:
            neighbours = self.helper.get_last_resort((self.head_x, self.head_y), self.grid_data[0], self.height, self.width)
            if neighbours:
                return self.helper.get_move_letter((self.head_x, self.head_y), neighbours[0])
            else:
                # Snake will almost certainly die
                return 'up'
        return None
