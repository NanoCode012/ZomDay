#!/usr/bin/python
#-*-coding: utf-8 -*-
from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
# from flask_sqlalchemy import SQLAlchemy
import json
# import numpy as np

app = Flask(__name__)

app.config["MYSQL_USER"] = "sql12321899"
app.config["MYSQL_PASSWORD"] = "rS2Gp9tXEn"
app.config["MYSQL_HOST"] = "sql12.freemysqlhosting.net"
app.config["MYSQL_DB"] = "sql12321899"
app.config["MYSQL_CURSORCLASS"]  = "DictCursor"
mysql = MySQL(app)

####################### new ########################

#default global variables
# name = ""
# game_start = False
# current_level = -1
# food = -1
# options = ["", ""]

class Controller():
    def __init__(self, player_name):
        self.cur = mysql.connection.cursor()
        self.player_name = player_name

    def create_table():
        self.cur.execute('''CREATE TABLE `tbl_players` (
                        `id` int(11) NOT NULL AUTO_INCREMENT,
                        `name` varchar(200) NOT NULL,
                        `game_start` tinyint(1) NOT NULL,
                        `current_level` int(11) NOT NULL,
                        `food` int(11) NOT NULL,
                        `options` varchar(200) NOT NULL
                        ) ENGINE=InnoDB DEFAULT CHARSET=latin1;''')
    def add_player(self):
        self.cur.execute('''INSERT INTO `tbl_players` (`id`, `name`, `game_start`, `current_level`, `food`, `options`) VALUES (NULL, "''' + self.player_name + '''", '1', '0', '2', 'Stay,Look,Exit')''')
        mysql.connection.commit()
    def delete_player(self):
        self.cur.execute('''DELETE FROM `tbl_players` WHERE `name` = "''' + self.player_name + '''"''')
        mysql.connection.commit()
    def get_player_data(self):
        self.cur.execute('''SELECT * FROM `tbl_players` WHERE `name` = "''' + self.player_name + '''"''')
        return self.cur.fetchall()
    def update_player_data(self, new_level, food, options, game_start = 1):
        self.cur.execute('''UPDATE `tbl_players` SET `game_start`=''' + str(game_start) + 
                        ''',`current_level`=''' + str(new_level) + 
                        ''',`food`=''' + str(food) + 
                        ''',`options`="''' + options + 
                        '''" WHERE `name` = "''' + self.player_name + '''"''')
        mysql.connection.commit()


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
        cntrl = Controller(name)
        cntrl.add_player()

    return jsonify({"message" : name + ", you are at home. You have food for only 2 days. You have two choice. 'Stay' inside or 'Look' outside?"})

@app.route("/play", methods=["GET"])
def play():
    try:
        name = request.args["name"].strip()
        cntrl = Controller(name)
        res = cntrl.get_player_data()[0]
        game_start = bool(res["game_start"])
        current_level = int(res["current_level"])
        food = int(res["food"])
        options = res["options"].split(",")

        if (game_start and current_level >= 0):
            action = request.args["action"].strip()
            if (current_level == 0):
                if (action == "Stay"):
                    current_level = 1
                    food -= 1
                    msg =  "You have " + str(food) + " food left. Do you want to 'Stay' inside or 'Look' outside?"
                elif (action == "Look"):
                    current_level = 2
                    food += 1
                    msg = "You found food! You have " + str(food) + " food left. Do you want to 'Stay' inside or 'Look' outside?"
                elif (action == "Exit"):
                    options = ["Exit", "", ""]
                    msg =  "Game over"
                else:
                    raise Exception("Unexpected State")
            elif (current_level == 1):
                if (action == "Stay"):
                    current_level = 3
                    food -= 1
                    options = ["Exit", "", ""]
                    msg =  "Hurray! The government stopped the crisis! You won"
                elif (action == "Look"):
                    current_level = 4
                    options = ["Exit", "", ""]
                    msg = "You died!"
                elif (action == "Exit"):
                    options = ["Exit", "", ""]
                    msg = "Game over"
                else:
                    raise Exception("Unexpected State")
            elif (current_level == 2):
                if (action == "Stay"):
                    current_level = 3
                    food -= 1
                    options = ["Exit", "", ""]
                    msg = "Hurray! The government stopped the crisis! You won"
                elif (action == "Look"):
                    current_level = 4
                    options = ["Exit", "", ""]
                    msg = "You died!"
                elif (action == "Exit"):
                    options = ["Exit", "", ""]
                    msg = "Game over"
                else:
                    raise Exception("Unexpected State")
            else:
                raise Exception("Unexpected State")
            cntrl.update_player_data(current_level, food, ",".join(options))
            return jsonify({"message" : msg})
        else:
            return jsonify({"message":"game not started"})
    except:
        options = ["Exit", "", ""]
        cntrl.update_player_data(current_level, food, options)
        return jsonify({"message" : "Sorry, invalid action"})

    return jsonify({"message":"unexpected state"})

@app.route("/reset", methods=["GET"])
def reset():
    game_reset()
    return jsonify({"message" : "Game reset"})

@app.route("/options", methods=["GET"])
def options():
    try:
        name = request.args["name"]
        res = Controller(name).get_player_data()[0]
        options = res["options"].split(",")
    except:
        return jsonify({'message' : 'error'})
    return jsonify({"option1" : options[0],
                    "option2" : options[1],
                    "option3" : options[2]
                    })

@app.route("/delete", methods=["GET"])
def delete():
    try:
        name = request.args["name"]
        Controller(name).delete_player()
    except:
        return jsonify({'message' : 'error'})
    return jsonify({"message" : "success"})

@app.route("/playerdata", methods=["GET"])
def playerdata():
    try:
        name = request.args["name"]
        msg = Controller(name).get_player_data()
    except:
        return jsonify({'message' : 'error'})
    return jsonify({"message" : msg})

def game_reset():
    game_start = False
    current_level = -1
    food = 2
    options = ["", ""]

if __name__ == '__main__':
    app.run(debug=True)
