#!/usr/bin/env python

import os, random, math
from flask import Flask, request, jsonify
from datetime import datetime
from timeit import default_timer as timer

from setup import Setup
from helper import Helper

from state_attack import State_Attack
from state_defend import State_Defend
from state_grow import State_Grow


app = Flask(__name__) #App is now an instance of Flask.

#NOTE Routing information

@app.route("/start", methods=["POST"])
def start():
    return jsonify( color = "#800000", secondary_color = "#000000", name = "FeistySnake", taunt = "Mess with Snekko, better run like hecko", head_type = "shades", tail_type = "freckled", head_url = "https://todaysmusings.files.wordpress.com/2008/05/raccoon.jpg?w=229&h=300")

@app.route("/move", methods=["POST"])
def move():
    start = timer()
    data = request.get_json()

    #NOTE grid_data[0] = move_grid // grid_data[1] = food_grid
    setup_process = Setup()
    helper = Helper()
    grid_data = setup_process.grid_setup(data) #(food, width, height, snakes, myID)

    # Game States
    defend = State_Defend()
    attack = State_Attack()
    grow = State_Grow()

    max_snake = helper.get_max_snake_length(data)

    if(len(data.get("you").get("body")) > max_snake):
        state = attack #TODO determine when to change states
    else:
        state = grow

    #NOTE Get the next move based on the pellet
    next_move = state.get_move(grid_data, data)
    end = timer()
    time = (end - start)
    print("Currently using {}".format(time))
    #NOTE Return the move in the JSON object wrapper
    return jsonify( move = next_move )

@app.route("/end", methods=["POST"])
def end():
    return '', 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, use_reloader=True)
