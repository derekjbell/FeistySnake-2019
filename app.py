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
    return jsonify( color = "#FF69B4", secondary_color = "#000000", name = "FeistySnake", taunt = "Mess with Snekko, better run like hecko", head_type = "shades", tail_type = "freckled", head_url = "https://todaysmusings.files.wordpress.com/2008/05/raccoon.jpg?w=229&h=300")

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

    defend.helper = helper
    attack.helper = helper
    grow.helper = helper

    max_snake = helper.get_max_snake_length(data)
    closest_food_distance = helper.get_closest_food_dist(grid_data[1], data)
    board_width = data.get("board").get("width")

    if(len(data.get("you").get("body")) > max_snake):
        state = attack #TODO determine when to change states
    elif closest_food_distance < board_width / 2 or len(data.get("board").get("food")) > 5:
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
    app.run(host='0.0.0.0', debug=True, use_reloader=True)
