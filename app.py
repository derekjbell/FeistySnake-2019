#!/usr/bin/env python
# Battlesnake 2018 Competition AI
# Jan 2019

import os, random, math, game_logic
from flask import Flask, request, jsonify
from datetime import datetime
from timeit import default_timer as timer

app = Flask(__name__) #App is now an instance of Flask.

#NOTE Routing information

@app.route("/start", methods=["POST"])
def start():
    global height
    global width
    global game_id

    return jsonify( color = "#E0FFFF", secondary_color = "#000000", name = "FeistySnake", taunt = "Mess with Snekko, better run like hecko", head_type = "shades", tail_type = "freckled", head_url = "https://todaysmusings.files.wordpress.com/2008/05/raccoon.jpg?w=229&h=300")

@app.route("/move", methods=["POST"])
def move():
    debug = True # Prints off debugging information to the Heroku logger

    data = request.get_json()

    width = data.get("width")
    height = data.get("height")
    food = data.get("food").get("data") #Array
    snakes = data.get("snakes").get("data") #Array
    you = data.get("you")
    myHealth = you.get("health")
    myLength = you.get("body").get("length")
    mySnake = you.get("body").get("data")


    if debug:
        start = timer() #NOTE THIS IS OUR TIMER START POINT
        print('')
        print("Health:{}".format(myHealth))
        print('')
        print("Game height:{}, Game width:{}".format(height,width))
        print('')
        print('turn = {}'.format(data.get("turn")))


    #NOTE grid_options[0] = general_grid // grid_options[1] = food_grid
    grid_options = game_logic.grid_setup(food, width, height, snakes, mySnake, you.get("id"))

    #NOTE Now, set our coordinates!
    mySnakeX = mySnake[0].get("x")
    mySnakeY = mySnake[0].get("y")

    #NOTE Search for the coordinates of the closest food pellet
    target_food = game_logic.get_closest_food(grid_options[1], mySnakeX, mySnakeY)

    #NOTE Get the next move based on the pellet
    next_move = game_logic.get_move(grid_options, target_food, mySnakeX, mySnakeY, height, width, mySnake, myHealth)

    if debug:
        #NOTE This is the end reference point of the timer. Just to get a good idea of what the runtime of the program is in total
        end = timer()
        print('')
        print("RUNTIME: {0}ms. MAX 200ms, currently using {1}%".format(((end - start) * 1000),(((end - start) * 1000) / 2)))

    #NOTE Return the move in the JSON object wrapper
    return jsonify(
    move = next_move #NOTE This is what controls where the snake goes!
    )

@app.route("/end", methods=["POST"])
def end():
    return '', 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, use_reloader=True)
