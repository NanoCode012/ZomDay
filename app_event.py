from flask import jsonify

def event_handler(action, cntrl):
    #may have error when user enters this state without name check
    res = cntrl.get_player_data()

    day = res["day"]
    resources = convert_resources_to_dict(res["resources"].split(","))#see doc for order/item 
    options = res["options"].split(",")
    status = convert_status_to_dict(res["status"].split(","))

    if (day > 0):
        if (action in options):
            if (action == "Check supplies"):
                msg = "Opening supply box"
            elif (action == "Act"):
                msg = "Showing possible actions"
            elif (action == "Next Day"):
                msg = "Next day.."
                next_day(cntrl, day, status)

            elif (action == "Exit"):
                msg = "Game over"
            elif (action == "Eat"):
                if (resources["food"] > 0):
                    msg = "Eating.."
                    resources["food"] -= 1
                    status["hp"] = min(status["hp"]+20, 100)
                    cntrl.update_player_resources(convert_dict_to_resources_db(resources))
                    cntrl.update_player_status(convert_dict_to_status_db(status))
                else:
                    msg = "Not enough food"
            elif (action == "Drink"):
                if (resources["water"] > 0):
                    msg = "Drinking.."
                    resources["water"] -= 1
                    status["thirst"] = min(status["thirst"]+20, 100)
                    cntrl.update_player_resources(convert_dict_to_resources_db(resources))
                    cntrl.update_player_status(convert_dict_to_status_db(status))
                else:
                    msg = "Not enough water"
            elif (action == "Back"):
                msg = "Back options"
            elif (action == "Talk to neighbour"):
                energy_needed = 10
                if (status["energy"] >= energy_needed):
                    msg = "Neighbour: Hi"
                    status["energy"] = max(status["energy"]-energy_needed, 0)
                    cntrl.update_player_status(convert_dict_to_status_db(status))
                    cntrl.update_player_news("Static: You talked to someone!")
                else:
                    msg = "Not enough energy"
                next_day(cntrl, day, status)    
            elif (action == "Look for food"):
                from random import randint
                
                r = randint(0, 100)
                if (0<= r < 30):
                    msg = "Found food!"
                elif (30 <= r < 60):
                    msg = "You died!"
                    status["hp"] = 0
                    options = ["Exit"]
                    cntrl.update_player_status(convert_dict_to_status_db(status))
                    cntrl.update_player_options(config_options_for_db(options))
                else:
                    msg = "You found nothing"
                next_day(cntrl, day, status) 
        else:
            return jsonify({"message" : "invalid action"})
        
        return jsonify({"message" : msg})
    else:
        return jsonify({"message":"game not started"})

def next_day(cntrl, day, status):
    day += 1
    cntrl.update_player_day(day)

    status["hp"] = max(status["hp"]-10, 0)
    status["thirst"] = max(status["thirst"]-10, 0)
    status["energy"] = min(status["energy"]+10, 100)
    cntrl.update_player_status(convert_dict_to_status_db(status))

def convert_resources_to_dict(res):
    from app import get_items

    d = {}
    items = get_items()
    for i in range(len(items)):
        d[items[i]] = int(res[i])
    return d

def convert_dict_to_resources_db(res):
    from app import get_items
    items = get_items()
    s = str(res[items[0]])
    for i in range(1, len(items)):
        s += "," + str(res[items[i]])
    return s

def convert_status_to_dict(st):
    d = {}
    d["hp"] = int(st[0])
    d["energy"] = int(st[1])
    d["thirst"] = int(st[2])
    return d

def convert_dict_to_status_db(st):
    return str(st["hp"]) + "," + str(st["energy"]) + "," + str(st["thirst"])

def pad_options(options, length=10):
    if (len(options) == length): return options
    
    for i in range(len(options), length):
        options.append("")
    return options

def config_options_for_db(options):
    return ",".join(pad_options(options))

def config_options_for_js(options):
    options = pad_options(options)
    d = {}
    for i in range(1, len(options)+1):
        d[str(i)] = options[i]
    return d
