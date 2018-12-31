#!/usr/bin/env python
# Battlesnake 2018 Competition AI
# Jan 2019

import os, random, math, game_logic
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
    global height
    global width
    global game_id
    global defend = State_Defend
    global attack = State_Attack
    global grow = State_Grow
    global state = defend

    return jsonify( color = "#E0FFFF", secondary_color = "#000000", name = "FeistySnake", taunt = "Mess with Snekko, better run like hecko", head_type = "shades", tail_type = "freckled", head_url = "https://todaysmusings.files.wordpress.com/2008/05/raccoon.jpg?w=229&h=300")

@app.route("/move", methods=["POST"])
def move():
    data = request.get_json()

    # width = data.get("width")
    # height = data.get("height")
    # food = data.get("food").get("data") #Array
    # snakes = data.get("snakes").get("data") #Array
    # you = data.get("you")
    # myHealth = you.get("health")
    # myLength = you.get("body").get("length")
    # mySnake = you.get("body").get("data")
    # myID = you.get("id")

    #NOTE grid_options[0] = move_grid // grid_options[1] = food_grid
    grid_options = Setup.grid_setup(data) #(food, width, height, snakes, myID)

    #NOTE Our snake's coordinates
    # mySnakeX = mySnake[0].get("x")
    # mySnakeY = mySnake[0].get("y")

    #NOTE Get coordinates of the closest food pellet
    target_food = Helper.get_closest_food(grid_options[1], data)

    #NOTE Get the next move based on the pellet
    next_move = game_logic.get_move(grid_options, target_food, data)

    #NOTE Return the move in the JSON object wrapper
    return jsonify( move = next_move )

@app.route("/end", methods=["POST"])
def end():
    return '', 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, use_reloader=True)
