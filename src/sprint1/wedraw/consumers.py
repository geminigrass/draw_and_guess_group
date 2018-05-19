from django.http import HttpResponse
from channels.handler import AsgiHandler
from channels.sessions import channel_session
from channels import Group
from urlparse import urlparse
from channels import Channel
import ast
import json
# In consumers.py

def ws_add(message):
    # Accept the connection
    message.reply_channel.send({"accept": True})
    # Add to the chat group
    Group("chat").add(message.reply_channel)

@channel_session
def ws_message(message):
    # ASGI WebSocket packet-received and send-packet message types
    # both have a "text" key for their textual data.
    payload = json.loads(message['text'])
    dictpayload = ast.literal_eval(payload)
    print("dictpayload")
    print(dictpayload)
    Channel("chat.receive").send(dictpayload)



def ws_disconnect(message):
    Group("chat").discard(message.reply_channel)



def we_draw(message):
    print("here==!!!!!!")
    print("here==!!!!!!")
    print("here==!!!!!!")
    print("here==!!!!!!")
    # array = message.content['text']
    print(message.content)
    # array = message.content
   
    # print (type(array) == type({}) )
    # arrayjson = json.loads(array)
    arrayjson = message.content
    print(arrayjson)
    print("arrayjson")
    x = arrayjson['x']
    y = arrayjson["y"]
    startX = arrayjson["startX"]
    startY = arrayjson["startY"]
    drawstyle = arrayjson["drawstyle"]
    curColor = arrayjson["curColor"]
    curRadius = arrayjson["curRadius"]
    Group("chat").send({
        "text": json.dumps({
            "draw": "candraw",
            "x": x,
            "y": y,
            "startX":startX,
            "startY":startY,
            "drawstyle":drawstyle,
            "curColor":curColor,
            "curRadius":curRadius,
        }),
    })