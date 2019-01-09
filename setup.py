class Setup():
    def __init__(self):
        self.name = "Setup Functions"

    #NOTE performs grid setup for each move
    def grid_setup(self, data):

        # Get the information held in the data object
        food = data.get("board").get("food")
        width = data.get("board").get("width")
        height = data.get("board").get("height")
        snakes = data.get("board").get("snakes")
        my_snake_id = data.get("you").get("id")

        # Holds information about the map and where the snake can move
        move_grid = []
        for y in range(0, height):
            new_row = []
            for x in range(0, width):
                new_row.append(1)
            move_grid.append(new_row)

        # Creates a list of all food locations on the grid
        food_grid = []
        for point in food:
            food_grid.append([point.get("x"), point.get("y")])

        #Snake locations:
        for snake in snakes:
            body = snake.get("body")
            snake_id = snake.get("id")
            if snake_id != my_snake_id:
                # If snake is an enedata.get("you").get("body").get("data")[0].get("x")my, create a "Danger Zone" around the
                # snake's head
                head = body[0]
                head_x = head.get("x")
                head_y = head.get("y")

                top = head_y - 1
                bottom = head_y + 1
                left = head_x - 1
                right = head_x + 1

                if top > 0:
                    move_grid[top][head_x] = -1
                if bottom < height:
                    move_grid[bottom][head_x] = -1
                if left > 0:
                    move_grid[head_y][left] = -1
                if right < width:
                    move_grid[head_y][right] = -1

            for point in body:
                move_grid[point.get("y")][point.get("x")] = 0

        grid_data = []
        grid_data.append(move_grid)
        grid_data.append(food_grid)

        return grid_data
