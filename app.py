#!/usr/bin/python
#-*-coding: utf-8 -*-
from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
# from flask_sqlalchemy import SQLAlchemy
import json
# import numpy as np

from app_flex import fxmessage
from app_event import event_handler, event_handler_v2, next_events_handler

app = Flask(__name__)

app.config["MYSQL_USER"] = "sql12321899"
app.config["MYSQL_PASSWORD"] = "rS2Gp9tXEn"
app.config["MYSQL_HOST"] = "sql12.freemysqlhosting.net"
app.config["MYSQL_DB"] = "sql12321899"
app.config["MYSQL_CURSORCLASS"]  = "DictCursor"
mysql = MySQL(app)

####################### new ########################

class Controller():
    def __init__(self, player_name):
        self.cur = mysql.connection.cursor()
        self.player_name = player_name

    def create_table(self):
        self.cur.execute('''CREATE TABLE `tbl_players` (
                        `id` int(11) NOT NULL AUTO_INCREMENT,
                        `name` varchar(200) NOT NULL UNIQUE,
                        `status` varchar(200) NOT NULL,
                        `day` int(11) NOT NULL,
                        `resources` varchar(200) NOT NULL,
                        `options` varchar(200) NOT NULL,
                        `news` varchar(200) NOT NULL,
                        `events` varchar(200) NOT NULL
                        ) ENGINE=InnoDB DEFAULT CHARSET=latin1;''')
    def add_player(self):
        self.cur.execute('''INSERT INTO `tbl_players` (`id`, `name`, `status`, `day`, `resources`, `options`, `news`, `events`) VALUES (NULL, "''' + self.player_name + '''", '100,100,100', 1,'3,3,0,0,0,0,0,0,0,0', 'Check supplies,Act,Next Day,Exit,Eat,Drink,Back,Back,Look for supplies,Back', '', '0,0')''')
        mysql.connection.commit()
    def delete_player(self):
        self.cur.execute('''DELETE FROM `tbl_players` WHERE `name` = "''' + self.player_name + '''"''')
        mysql.connection.commit()
    def get_player_data(self):
        self.cur.execute('''SELECT * FROM `tbl_players` WHERE `name` = "''' + self.player_name + '''"''')
        return self.cur.fetchall()[0]
    # def update_player_data(self, status, day, resources, options):
    #     self.cur.execute('''UPDATE `tbl_players` SET `game_start`=''' + str(game_start) + 
    #                     ''',`current_level`=''' + str(new_level) + 
    #                     ''',`resources`=''' + ",".join(resources) + 
    #                     ''',`options`="''' + options + 
    #                     '''" WHERE `name` = "''' + self.player_name + '''"''')
        # mysql.connection.commit()
    def update_player_resources(self, resources):
        self.cur.execute('''UPDATE `tbl_players` SET `resources`="''' + resources + 
                        '''" WHERE `name` = "''' + self.player_name + '''"''')
        mysql.connection.commit()
    def update_player_status(self, status):
        self.cur.execute('''UPDATE `tbl_players` SET `status`="''' + status + 
                        '''" WHERE `name` = "''' + self.player_name + '''"''')
        mysql.connection.commit()
    def update_player_day(self, day):
        self.cur.execute('''UPDATE `tbl_players` SET `day`=''' + str(day) + 
                        ''' WHERE `name` = "''' + self.player_name + '''"''')
        mysql.connection.commit()
    def update_player_events(self, events):
        self.cur.execute('''UPDATE `tbl_players` SET `events`="''' + events + 
                        '''" WHERE `name` = "''' + self.player_name + '''"''')
        mysql.connection.commit()
    def update_player_news(self, news, clear=False):
        if (not clear):
            res = self.get_player_data()
            if (res["news"] != ""):
                news = res["news"] + "\\n" + news


        self.cur.execute('''UPDATE `tbl_players` SET `news`="''' + news + 
                        '''" WHERE `name` = "''' + self.player_name + '''"''')
        mysql.connection.commit()
    def update_player_options(self, options):
        self.cur.execute('''UPDATE `tbl_players` SET `options`="''' + options + 
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
    return jsonify({'message' : name })

@app.route("/start", methods=["GET"])
def start():
    try:
        name = request.args["name"].strip()
        Controller(name).add_player()
    except:
        return jsonify({"message" : "Loading previous save"})

    return jsonify({"message" : name + ", you are at home. Apocalypse happened. You must survive!"})

@app.route("/play", methods=["GET"])
def play():
    try:
        name = request.args["name"].strip()
        action = request.args["action"].strip()

        cntrl = Controller(name)

        return event_handler(action, cntrl)
    except:
        return jsonify({"message" : "Sorry, please try again"})

@app.route("/events", methods=["GET"])
def events():
    try:
        name = request.args["name"].strip()

        cntrl = Controller(name)

        return event_handler_v2(cntrl)
    except:
        return jsonify({"message" : "Sorry, please try again"})

@app.route("/next_day", methods=["GET"])
def next_day():
    try:
        name = request.args["name"].strip()

        cntrl = Controller(name)
        res = cntrl.get_player_data()
        from app_event import next_day, convert_status_to_dict
        next_day(cntrl, res["day"], convert_status_to_dict(res["status"].split(",")))
        return jsonify({"message":"success"})
    except:
        return jsonify({"message" : "Sorry, please try again"})

@app.route("/eat", methods=["GET"])
def eat():
    try:
        name = request.args["name"].strip()

        cntrl = Controller(name)
        from app_event import convert_resources_to_dict
        food = convert_resources_to_dict(cntrl.get_player_data()["resources"].split(","))["food"]

        if (food >= 1):
            food -= 1
            msg = "Food - 1"
        else:
            msg = "Not enough food"

        return jsonify({"message" : msg})
    except:
        return jsonify({"message" : "Sorry, please try again"})

@app.route("/drink", methods=["GET"])
def drink():
    try:
        name = request.args["name"].strip()

        cntrl = Controller(name)
        from app_event import convert_resources_to_dict
        water = convert_resources_to_dict(cntrl.get_player_data()["resources"].split(","))["water"]

        if (water >= 1):
            water -= 1
            msg = "Water - 1"
        else:
            msg = "Not enough food"

        return jsonify({"message" : msg})
    except:
        return jsonify({"message" : "Sorry, please try again"})

@app.route("/next_events", methods=["GET"])
def next_events():
    try:
        name = request.args["name"].strip()

        cntrl = Controller(name)

        return next_events_handler(cntrl)
    except:
        return jsonify({"message" : "Sorry, please try again"})

@app.route("/news", methods=["GET"])
def news():
    try:
        name = request.args["name"].strip()

        cntrl = Controller(name)

        res = cntrl.get_player_data()
        news = res["news"]
        if (news == ""): news = "No extra news for today."
        cntrl.update_player_news("", True)
        
        header_news = "It's Day " + str(res["day"])

        return jsonify({"header": header_news, "message": news})
    except:
        return jsonify({"message" : "Sorry, please try again"})

@app.route("/status", methods=["GET"])
def status():
    try:
        name = request.args["name"].strip()

        cntrl = Controller(name)

        from app_event import convert_status_to_dict
        status = convert_status_to_dict(cntrl.get_player_data()["status"].split(","))

        msg = "HP:"+str(status["hp"])+"\\n"+"Energy:"+str(status["energy"])+"\\nThirst:"+str(status["thirst"])
        return jsonify({"message": msg})
    except:
        return jsonify({"message" : "Sorry, please try again"})

@app.route("/newsandstatus", methods=["GET"])
def newsandstatus():
    try:
        name = request.args["name"].strip()

        cntrl = Controller(name)

        event_handler_v2(cntrl)

        res = cntrl.get_player_data()
        from app_event import convert_status_to_dict
        status = convert_status_to_dict(res["status"].split(","))

        status_message = "HP:"+str(status["hp"])+"\\n"+"Energy:"+str(status["energy"])+"\\nThirst:"+str(status["thirst"])

        news_body = res["news"]
        if (news_body == ""): news_body = "No extra news for today."
        cntrl.update_player_news("", True)
        
        news_header = "It's Day " + str(res["day"])

        return jsonify({"news_header": news_header, "news_body": news_body, "status_message": status_message})
    except:
        return jsonify({"message" : "Sorry, please try again"})

@app.route("/resources", methods=["GET"])
def resources():
    try:
        name = request.args["name"].strip()

        cntrl = Controller(name)

        from app_event import convert_resources_to_dict
        resources = convert_resources_to_dict(cntrl.get_player_data()["resources"].split(","))

        food = resources["food"]
        water = resources["water"]
        return jsonify({"food": food, "water": water})
    except:
        return jsonify({"message" : "Sorry, please try again"})

# @app.route("/reset", methods=["GET"])
# def reset():
#     game_reset()
#     return jsonify({"message" : "Game reset"})

@app.route("/options", methods=["GET"])
def options():
    try:
        name = request.args["name"]
        res = Controller(name).get_player_data()
        options = res["options"].split(",")
    except:
        return jsonify({'message' : 'error'})
    return jsonify({"option1" : options[0],
                    "option2" : options[1],
                    "option3" : options[2],
                    "option4" : options[3]
                    })

@app.route("/options0", methods=["GET"])
def options0():
    try:
        name = request.args["name"]
        res = Controller(name).get_player_data()
        options = res["options"].split(",")
    except:
        return jsonify({'message' : 'error'})
    return jsonify({"option1" : options[4],
                    "option2" : options[5],
                    "option3" : options[6]
                    })

@app.route("/options1", methods=["GET"])
def options1():
    try:
        name = request.args["name"]
        res = Controller(name).get_player_data()
        options = res["options"].split(",")
    except:
        return jsonify({'message' : 'error'})
    return jsonify({"option1" : options[7],
                    "option2" : options[8],
                    "option3" : options[9]
                    })

@app.route("/itemlist", methods=["GET"])
def itemlist():
    items = get_items()
    di = {}
    for i in range(len(items)):
        di["item" + str(i+1)] = items[i]
    return jsonify(di)

@app.route("/takeitem", methods=["GET"])
def takeitem():
    try:
        name = request.args["name"]
        item = request.args["item"]
        cntrl = Controller(name)
        res = cntrl.get_player_data()
        from app_event import convert_dict_to_resources_db, convert_resources_to_dict

        resources = convert_resources_to_dict(res["resources"].split(","))
        if (item in resources):
            resources[item] += 1
            cntrl.update_player_resources(convert_dict_to_resources_db(resources))
            return jsonify({"message":"picked up item"})
        else:
            raise Exception("Wrong item")
    except:
        return jsonify({'message' : 'error'})

@app.route("/ret", methods=["GET"])
def ret():
    return jsonify({"message":"1", "message2":"DL_goout"})

# @app.route("/delete", methods=["GET"])
# def delete():
#     try:
#         name = request.args["name"]
#         Controller(name).delete_player()
#     except:
#         return jsonify({'message' : 'error'})
#     return jsonify({"message" : "success"})

@app.route("/playerdata", methods=["GET"])
def playerdata():
    try:
        name = request.args["name"]
        msg = Controller(name).get_player_data()
    except:
        return jsonify({'message' : 'error'})
    return jsonify(msg)

@app.route("/fxmessage", methods=["GET"])
def fxmessagehandler():
    return fxmessage()

def get_items():
    return ["food", "water", "weapon1", "weapon2", "comm device", "surv tool 1", "surv tool 2", "surv tool 3", "surv tool 4", "surv tool 5"]

def get_status():
    return ["hp", "energy", "thirst"]

if __name__ == '__main__':
    app.run(debug=True)
