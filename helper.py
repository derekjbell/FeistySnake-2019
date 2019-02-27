import math
import floodfill

class Helper():

    def __init__(self):
        self.name = "helper methods"

    #NOTE returns a position tuple of closest food pellet
    def get_closest_food(self, food_list, date):
        head_x = data.get("you").get("body").get("data")[0].get("x")
        head_y = data.get("you").get("body").get("data")[0].get("y")

        current_minimum = math.inf
        for pellet in food_list:
            pellet_distance = get_crows_dist((head_x, head_y),pellet)
            if pellet_distance < current_minimum:
                current_minimum = pellet_distance
                target_position = pellet
        return tuple(target_position)

    def get_crows_dist(self, start, end):
        (x1, y1) = start
        (x2, y2) = end
        return abs(math.hypot(x2 - x1, y2 - y1))

    def get_move_letter(self, start, end):
        current_x = start[0]
        current_y = start[1]
        next_x = end[0]
        next_y = end[1]
        delta_x = next_x - current_x
        delta_y = next_y - current_y
        if delta_x > 0:
            return 'right'
        elif delta_y > 0:
            return 'down'
        elif delta_x < 0:
            return 'left'
        elif delta_y < 0:
            return 'up'

    def get_neighbors(self, node, lines, height, width):
        (x, y) = node #changed from x, y
        # return[(nx, ny) for nx, ny in[(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)] if 0 <= nx < width and 0 <= ny < height and lines[ny][nx] == 1]
        potential_moves = [(nx, ny) for nx, ny in[(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)] if 0 <= nx < width and 0 <= ny < height and lines[ny][nx] == 1]
        print("Potential moves:")
        print(potential_moves)
        if len(potential_moves) > 0:
            return self.sort_options_fill(potential_moves, lines)
        else:
            return None

    def get_last_resort(self, node, lines, height, width):
        (x, y) = node #changed from x, y
        # return[(nx, ny) for nx, ny in[(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)] if 0 <= nx < width and 0 <= ny < height and lines[ny][nx] == 1]
        potential_moves = [(nx, ny) for nx, ny in[(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)] if 0 <= nx < width and 0 <= ny < height and lines[ny][nx] != 0]
        print("Potential last resort moves:")
        print(potential_moves)
        if len(potential_moves) > 0:
            return self.sort_options_fill(potential_moves, lines)
        else:
            return None

    def sort_options_fill(self, list, map):
        filler = floodfill.FloodFill([map,[]])
        list_with_area = []
        for entry in list:
            new_entry = [entry, filler.calculate_one(entry)]
            list_with_area.append(new_entry)
        list_with_area.sort(key=lambda x: x[1])
        return_list = [x for [x, y] in list_with_area]
        return_list.reverse()
        return return_list

    def get_max_snake_length(self, data):
        my_snake_id = data.get("you").get("id")
        snakes = data.get("board").get("snakes")

        current_max = 0

        for snake in snakes:
            if snake.get("id") != my_snake_id:
                if len(snake.get("body")) > current_max:
                    current_max = len(snake.get("body"))

        return current_max

    def is_good_move(self, location, map, my_snake_length):
        filler = floodfill.FloodFill([map,[]])
        available_space = filler.calculate_one(location)
        if available_space <= my_snake_length:
            print("Bad move:{} spaces available".format(available_space))
            return False
        else:
            print("Good move:{} spaces available".format(available_space))
            return True

    def print_board(self, grid):
        for row in grid:
            for column in row:
                print(column,end='')
                print(" ",end='')
            print("")

if __name__ == "__main__":
    helper = Helper()
    grid = [[1,0,1,1,0,1,1,1],
            [1,0,1,1,0,1,1,1],
            [1,0,1,0,0,1,1,1],
            [1,0,1,0,1,1,0,1],
            [1,0,1,0,1,1,0,0]]
    op1 = (0, 0)
    op2 = (2, 0)
    op3 = (6, 0)
    new_list = [op1, op2, op3]
    print(helper.sort_options_fill(new_list, grid))
