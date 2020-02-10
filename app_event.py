from flask import jsonify

def event_handler(res, action, cntrl):
    game_start = bool(res["game_start"])
    current_level = int(res["current_level"])
    food = int(res["food"])
    options = res["options"].split(",")

    if (game_start and current_level >= 0):
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
                options = ["Exit"]
                msg =  "Game over"
            else:
                raise Exception("Unexpected State")
        elif (current_level == 1):
            if (action == "Stay"):
                current_level = 3
                food -= 1
                options = ["Exit"]
                msg =  "Hurray! The government stopped the crisis! You won"
            elif (action == "Look"):
                current_level = 4
                options = ["Exit"]
                msg = "You died!"
            elif (action == "Exit"):
                options = ["Exit"]
                msg = "Game over"
            else:
                raise Exception("Unexpected State")
        elif (current_level == 2):
            if (action == "Stay"):
                current_level = 3
                food -= 1
                options = ["Exit"]
                msg = "Hurray! The government stopped the crisis! You won"
            elif (action == "Look"):
                current_level = 4
                options = ["Exit"]
                msg = "You died!"
            elif (action == "Exit"):
                options = ["Exit"]
                msg = "Game over"
            else:
                raise Exception("Unexpected State")
        else:
            raise Exception("Unexpected State")
        cntrl.update_player_data(current_level, food, config_options_for_db(options))
        return jsonify({"message" : msg})
    else:
        return jsonify({"message":"game not started"})

def pad_options(options, length=3):
    if (len(options) == length): return options
    
    for i in range(len(options), length):
        options.append("")
    return options

def config_options_for_db(options):
    return ",".join(pad_options(options))
