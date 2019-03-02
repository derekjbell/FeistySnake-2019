import helper
class Setup():
    def __init__(self):
        self.name = "Setup Functions"
        self.helper = helper.Helper()

    #NOTE performs grid setup for each move
    def grid_setup(self, data):
        # Squares with 1 are open, squares with 0 are no-go, squares with -1 are danger

        # Get the information held in the data object
        food = data.get("board").get("food")
        width = data.get("board").get("width")
        height = data.get("board").get("height")
        snakes = data.get("board").get("snakes")
        my_snake_id = data.get("you").get("id")
        my_snake_length = len(data.get("you").get("body"))
        my_snake_head = (data.get("you").get("body")[0].get("x"), data.get("you").get("body")[0].get("y"))

        # Holds information about the map and where the snake can move
        move_grid = []
        for y in range(0, height):
            new_row = []
            for x in range(0, width):
                new_row.append(1)
            move_grid.append(new_row)

        # Creates a list of all food locations on the grid

        unsorted_food_list = []
        for pellet in food:
            tuple_pellet = (pellet.get("x"), pellet.get("y"))
            new_entry = [tuple_pellet, self.helper.get_crows_dist(tuple_pellet, my_snake_head)]
            unsorted_food_list.append(new_entry)
        unsorted_food_list.sort(key=lambda x: x[1])
        food_grid = [x for [x, y] in unsorted_food_list]
        food_grid=food_grid[0:5]

        # food_grid = []
        # for point in food:
        #     food_grid.append([point.get("x"), point.get("y")])

        #Snake locations:
        for snake in snakes:
            body = snake.get("body")
            snake_id = snake.get("id")

            # Sets up the "danger zone" around a snake's head
            if snake_id != my_snake_id: #and len(body) >= my_snake_length or (len(body) == my_snake_length - 1 and snake.get("health") == 100):
                # If snake is an enedata.get("you").get("body").get("data")[0].get("x")my, create a "Danger Zone" around the
                # snake's head
                head = body[0]
                head_x = head.get("x")
                head_y = head.get("y")

                top = head_y - 1
                bottom = head_y + 1
                left = head_x - 1
                right = head_x + 1

                # Sets up "Danger Squares" around foe snake heads
                if top >= 0 and move_grid[top][head_x] != 0:
                    move_grid[top][head_x] = -1
                if bottom < height and move_grid[bottom][head_x] != 0:
                    move_grid[bottom][head_x] = -1
                if left >= 0 and move_grid[head_y][left] != 0:
                    move_grid[head_y][left] = -1
                if right < width and move_grid[head_y][right] != 0:
                    move_grid[head_y][right] = -1

            # Changes every point of a snake to a 0 on the board aka a wall.
            for point in body:
                move_grid[point.get("y")][point.get("x")] = 0

            # Set the tail of a snake to a location that you can move to IF NECESSARY!
            if snake.get("health") < 100:
                move_grid[body[-1].get("y")][body[-1].get("x")] = -1

        grid_data = []
        grid_data.append(move_grid)
        grid_data.append(food_grid)

        return grid_data
