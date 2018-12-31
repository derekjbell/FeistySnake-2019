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
    print("Starting start method")
    data = request.get_json()

    global height
    height = data.get("height")
    global width
    width = data.get("weight")
    global game_id
    game_id = data.get("game_id")

    # Game States
    global defend
    defend = State_Defend()
    global attack
    attack = State_Attack()
    global grow
    grow = State_Grow()

    # Current State
    global state
    state = defend

    return jsonify( color = "#E0FFFF", secondary_color = "#000000", name = "FeistySnake", taunt = "Mess with Snekko, better run like hecko", head_type = "shades", tail_type = "freckled", head_url = "https://todaysmusings.files.wordpress.com/2008/05/raccoon.jpg?w=229&h=300")

@app.route("/move", methods=["POST"])
def move():
    data = request.get_json()

    #NOTE grid_data[0] = move_grid // grid_data[1] = food_grid
    grid_data = Setup().grid_setup(data) #(food, width, height, snakes, myID)

    #NOTE Get the next move based on the pellet
    next_move = state.get_move(grid_data, data)

    #NOTE Return the move in the JSON object wrapper
    return jsonify( move = next_move )

@app.route("/end", methods=["POST"])
def end():
    return '', 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, use_reloader=True)
