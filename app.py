#!/usr/bin/env python

from flask import Flask, request, jsonify
import time

from setup import Setup
from helper import Helper

from state_attack import State_Attack
from state_defend import State_Defend
from state_grow import State_Grow


app = Flask(__name__) #App is now an instance of Flask.

#NOTE Routing information

@app.route("/start", methods=["POST"])
def start():
    print("-----START GAME-----")
    return jsonify( color = "#FF69B4", name = "FeistySnake", headType = "shades", tailType = "freckled")

@app.route("/move", methods=["POST"])
def move():
    tic = time.time()
    data = request.get_json()

    #NOTE grid_data[0] = move_grid // grid_data[1] = food_grid
    setup_process = Setup()
    helper = Helper()
    grid_data = setup_process.grid_setup(data)

    # Game States
    defend = State_Defend()
    attack = State_Attack()
    grow = State_Grow()

    # Assign the global helper methods to each state
    defend.helper = helper
    attack.helper = helper
    grow.helper = helper

    #helper.print_board(grid_data[0])

    max_snake = helper.get_max_snake_length(data)

    closest_food_distance = helper.get_closest_food_dist(grid_data[1], data)

    board_width = data.get("board").get("width")

    if len(data.get("you").get("body")) > max_snake + 1:
        # Assign the attack state when we are 2 bigger than any other snake
        state = attack
    elif closest_food_distance < board_width / 1.5:
        # Assign the grow state if a piece of food is within boardlen/1.5
        # or if there are more than 5 pieces of food on the board
        state = grow
    else:
        state = defend

    #NOTE Get the next move based on the pellet
    next_move = state.get_move(grid_data, data)
    toc = time.time()

    print("Move for round: {}".format(data.get("turn")))
    print("Time used: {}ms".format((toc - tic)*1000))
    print("State: {}".format(state.name))
    #helper.print_board(grid_data[0])
    #NOTE Return the move in the JSON object wrapper
    return jsonify( move = next_move )

@app.route("/end", methods=["POST"])
def end():
    print("-----END GAME-----")
    return '', 200

@app.route("/ping", methods=["POST"])
def ping():
    return '', 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False, use_reloader=True)
