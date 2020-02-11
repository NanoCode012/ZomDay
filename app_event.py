from flask import jsonify
from random import randint

def event_handler(action, cntrl):
    #may have error when user enters this state without name check
    res = cntrl.get_player_data()

    day = res["day"]
    resources = convert_resources_to_dict(res["resources"].split(","))#see doc for order/item 
    options = res["options"].split(",")
    status = convert_status_to_dict(res["status"].split(","))
    news = res["news"]

    if (day > 0):
        if (action in options):
            if (action == "Check supplies"):
                msg = "Opening supply box"
            elif (action == "Act"):
                msg = "Showing possible actions"
            elif (action == "Next Day"):
                msg = "Next day.."
                next_day(cntrl, day, status)
            elif (action == "Exit" or action == "-" or action == " "):
                msg = "Game over"
            elif (action == "Eat"):
                if (resources["food"] > 0):
                    msg = "Eating.."
                    resources["food"] -= 1
                    status["energy"] = min(status["energy"]+20, 100)
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
            elif (action == "Add Geek as contact"):
                energy_needed = 10
                if (status["energy"] >= energy_needed):
                    msg = "You added Geek"
                    options[7] = "Back"
                    status["energy"] = max(status["energy"]-energy_needed, 0)
                    cntrl.update_player_options(config_options_for_db(options))
                    cntrl.update_player_status(convert_dict_to_status_db(status))
                else:
                    msg = "Not enough energy"
                next_day(cntrl, day, status)  
            elif (action == "Send supplies to Geek"):
                energy_needed = 30
                if (status["energy"] >= energy_needed):
                    msg = "You sent supplies to Geek"
                    options[7] = "Back"
                    status["energy"] = max(status["energy"]-energy_needed, 0)
                    cntrl.update_player_options(config_options_for_db(options))
                    cntrl.update_player_status(convert_dict_to_status_db(status))
                else:
                    msg = "Not enough energy"
                next_day(cntrl, day, status)     
            elif (action == "Look for supplies"):
                r = randint(0, 100)
                if (0<= r < 30):
                    msg = "Found food!"
                    food_found = randint(1,3)
                    news = add_news(news, "You found " + str(food_found) + " food")
                    resources["food"] += food_found
                    cntrl.update_player_resources(resources)
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

def event_handler_v2(cntrl):
    res = cntrl.get_player_data()

    day = res["day"]
    options = res["options"].split(",")
    news = res["news"]
    events = [int(v) for v in res["events"].split(",")]

    if (day > 0):
        r = randint(0, 100)
        if (events[0] == 0):
            # if ((day == 2 and (0 <= r < 30)) or (day == 3 and (0 <= r < 60)) or (day == 4)):
            if (day >= 2):
                events[0] = 1
                
                events[1] = day
                options[7] = "Add Geek as contact"
                news = "A self-proclaimed geek came to visit and left a message containing his contact. Check it out at Act."
                cntrl.update_player_events(convert_list_to_events_db(events))
                cntrl.update_player_options(config_options_for_db(options))
                cntrl.update_player_news("A self-proclaimed geek came to visit and left a message containing his contact. Check it out at Act.")
                
        elif (events[0] == 1):
            # if ((events[1] - day == 1 and (0 <= r < 30)) or (events[1] - day == 2 and (0 <= r < 60)) or (events[1] - day == 3)):
            if (day >= 4):
                events[0] = 2
                
                events[1] = day
                options[7] = "Send supplies to Geek"
                cntrl.update_player_events(convert_list_to_events_db(events))
                cntrl.update_player_options(config_options_for_db(options))
                cntrl.update_player_news("You got a message from Geek. He lives nearby. He is asking for some supplies. Check it out at Act.")
    return jsonify({"message": news})


def add_news(current_news, new_news):
    return new_news + "\\n" + current_news

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

def convert_list_to_events_db(e):
    return ",".join([str(v) for v in e])

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
