<<<<<<< HEAD
import geop.distance as ps
import pandas as pd
import gspread

from oauth2client.service_account import ServicAccountCredentials
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json',scope)
client = gspread.authorize(creds)
sheet = client.open("Data name").sheet1
data = sheet.get_all_records()
listdata = pd.DataFrame(data)
print(listdata)
=======
#!/usr/bin/python
#-*-coding: utf-8 -*-
##from __future__ import absolute_import
###
from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
import json
import numpy as np


#import pymongo
#from pymongo import MongoClient
#from flask_restful import Resource, Api, reqparse

# from linebot.models import (
#     MessageEvent, TextMessage, TextSendMessage,TemplateSendMessage,ImageSendMessage, StickerSendMessage, AudioSendMessage
# )
# from linebot.models.template import *
# from linebot import (
#     LineBotApi, WebhookHandler
# )

app = Flask(__name__)
#app.config("SQLALCHEMY_DATABASE_URI") = r"mysql://id10391787_acclog:7%4dx7SC%to$@localhost/id10391787_accountlogin"
#db = SQLAcademy(app)

# lineaccesstoken = 'tIusZcDlB46unf8x8Lr2WkL197uMfnW7UJ85O021hxTVJ1p8/IRzGUDrew7vS7H4589SiLf6wlALp+JMm93AGUv6X0D739fynRQoPMtcFSie+MlcWOgexoVuhuhglLwgVxl/um3ewL3vlaXKPQQDYQdB04t89/1O/w1cDnyilFU='
# line_bot_api = LineBotApi(lineaccesstoken)

####################### new ########################
@app.route('/', methods=['GET'])
def index():
    return jsonify({'message' : 'hello world'})


@app.route('/callback', methods=['GET'])
def callback():
    try:
        json_line = request.args["name"]
    except:
        return jsonify({'message' : 'error'})
    print("No error")
    return jsonify({'message' : json_line })

    # json_line = json.dumps(json_line)
    # decoded = json.loads(json_line)


    # no_event = len(decoded['events'])
    # for i in range(no_event):
    #     event = decoded['events'][i]
    #     #try:
    #     event_handle(event)
    #     #except:
    #     #    pass
    return '',200


def event_handle(event):
    return ""


if __name__ == '__main__':
    app.run(debug=True)
>>>>>>> b168b3b847cb83ce33feaf43d1402f782e85b1c1
