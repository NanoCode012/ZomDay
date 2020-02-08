#!/usr/bin/python
#-*-coding: utf-8 -*-
from flask import Flask, jsonify, request
# from flask_sqlalchemy import SQLAlchemy
import json
# import numpy as np


app = Flask(__name__)
#app.config("SQLALCHEMY_DATABASE_URI") = r"mysql://id10391787_acclog:7%4dx7SC%to$@localhost/id10391787_accountlogin"
#db = SQLAcademy(app)

####################### new ########################

#default global variables
name = ""
game_start = False
current_level - -1
food = -1


@app.route('/')
def index():
    return jsonify({'message' : 'hello world, good to know you'})

@app.route('/callback', methods=['GET'])
def callback():
    try:
        name = request.args["username"]
    except:
        return jsonify({'message' : 'error'})
    print("No error")
    return jsonify({'message' : msg })

@app.route("/start", methods=["GET"])
def start():
    try:
        name = request.args["name"].strip()
    except:
        return jsonify({"message" : "Sorry, invalid name"})
    finally:
        game_start = true
        current_level = 0
    return jsonify({"message" : "You are at home. You have food for only 2 days. You have two choice. 'Stay' inside or 'Look' outside?",
                    "option1" : "Stay",
                    "option2" : "Look"
                    })

@app.route("/play", methods=["GET"])
def play():
    try:
        if (game_start == True and current_level >= 0):
            action = request.args["action"].strip()
            if (current_level == 0):
                if (action == "Stay"):
                    current_level = 1
                    food -= 1
                    return jsonify({"message" : "You have " + food + " food left. Do you want to 'Stay' inside or 'Look' outside?",
                                    "option1" : "Stay",
                                    "option2" : "Look"
                                    })
                elif (action == "Look"):
                    current_level = 2
                    food += 1
                    return jsonify({"message" : "You found food! You have " + food + " food left. Do you want to 'Stay' inside or 'Look' outside?",
                                    "option1" : "Stay",
                                    "option2" : "Look"
                                    })
                elif (action == "Exit"):
                    return jsonify({"message" : "Game over"})
                else:
                    return Exception()
            elif (current_level == 1):
                if (action == "Stay"):
                    current_level = 3
                    food -= 1
                    return jsonify({"message" : "Hurray! The government stopped the crisis! You won",
                                    "option1" : "Exit",
                                    "option2" : "Exit"
                                    })
                elif (action == "Look"):
                    current_level = 4
                    return jsonify({"message" : "You died!",
                                    "option1" : "Exit",
                                    "option2" : "Exit"
                                    })
                elif (action == "Exit"):
                    return jsonify({"message" : "Game over"})
                else:
                    return Exception()
            elif (current_level == 2):
                if (action == "Stay"):
                    current_level = 3
                    food -= 1
                    return jsonify({"message" : "Hurray! The government stopped the crisis! You won",
                                    "option1" : "Exit",
                                    "option2" : "Exit"
                                    })
                elif (action == "Look"):
                    current_level = 4
                    return jsonify({"message" : "You died!",
                                    "option1" : "Exit",
                                    "option2" : "Exit"
                                    })
                elif (action == "Exit"):
                    return jsonify({"message" : "Game over"})
                else:
                    return Exception()
            else:
                return Exception()
    except:
        return jsonify({"message" : "Sorry, invalid action"})

@app.route("/reset", methods=["GET"])
def reset():
    game_reset()
    return jsonify({"message" : "Game reset"})

def game_reset():
    game_start = False
    current_level = -1
    food = 2

if __name__ == '__main__':
    app.run(debug=True)
