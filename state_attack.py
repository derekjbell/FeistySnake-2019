from helper import Helper
from astar import AStar
import math


class State_Attack():

    def __init__(self):
        self.name = "attack state"

    def get_move(self, grid_data, data):
        snakes = data.get("snakes")
        head = data.get("you").get("data")[0]
        a_star = AStar(head, grid_data, data.get("height"), data.get("width"))
        # find closest snake
        target_snake_id = self.path_to_head(a_star, snakes, head)
        target_snake
        # Find target snake data
        for snake in snakes:
            if snake.get("id") == target_snake_id:
                target_snake = snake.get("data")

        target_position = self.get_target_position(target_snake)
        return move_to_food(self, a_star, [target_position], head)

    def get_target_position(self, snake):
        delta_x = snake[0].get("x") - snake[1].get("x")
        delts_y = snake[0].get("y") - snake[1].get("y")
        target_x = 2*delta_x + snake[0].get("x")
        target_y = 2*delta_y + snake[0].get("y")
        return (target_x, target_y)

    def path_to_head(self, a_star_object, snakes, head):
        current_minimum = float('inf')
        current_path = None
        current_id = None
        for snake in snakes:
            path = a_star_object.astar(snake.get("data")[0], tuple(head))
            if path:
                path = list(path)
                if len(path) < current_minimum:
                    current_minimum = len(path)
                    current_path = path
                    current_id = snake.get("id")

        return current_id

    def move_to_food(self, a_star_object, food_list, head):
        current_minimum = float('inf')
        current_path = None
        for food in food_list:
            path = a_star_object.astar(head, tuple(food))
            if path:
                path = list(path)
                if len(path) < current_minimum:
                    current_minimum = len(path)
                    current_path = path
        if current_path:
            return get_move_letter(head, list(current_path)[1])
        return None
