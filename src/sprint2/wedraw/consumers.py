from django.http import HttpResponse
from channels.handler import AsgiHandler
from channels.sessions import channel_session
from channels import Group
from channels import Channel
import ast
import json
from channels.auth import channel_session_user_from_http, channel_session_user
from .models import Room
# In consumers.py

@channel_session_user_from_http
def ws_add(message):

    info = message.content['path'].strip("/").split("/")
    if len(info) == 2:
        #print("----------begin ws_add -------------")
        message.reply_channel.send({"accept": True})
        cmd = info[0]
        roomID = info[1]
        message.channel_session['room'] = roomID
        Group("%s-%s" % (cmd,roomID)).add(message.reply_channel)

        #print("ws_add operation is: ")
        #print("%s-%s" % (cmd,roomID))
        user = message.user.username
        #print("USer is "+user)
        if cmd == "room":
            Group("%s-%s" % (cmd,roomID)).send({"text": json.dumps({"user": user})})
        #print("----------end ws_add----------------")


@channel_session
def ws_message(message):
    #print("--------ws_msg--------")
    array = json.loads(message.content['text'])
    arrayjson = json.loads(array)
    room = message.channel_session['room']

    cmd = arrayjson['command']
    if cmd == 'begin' or cmd == 'clear' or cmd== 'word' or cmd=='draw':
        Group("room-%s" % room).send({
            "text": json.dumps({
                "text": arrayjson,
            })})
    # command score, room, count go in here
    else:
        Group("%s-%s" % (cmd, room)).send(
            {
                "text": json.dumps({
                    "text": arrayjson,
                }),
            }
        )
    #print("send command : " + cmd + " to room : " + room)
    #print("----------end ws_msg----------------")


@channel_session
def ws_disconnect(message):
    Group("chat").discard(message.reply_channel)


# def room_leave(message):
#     room = Room.objects.get(message["room"], message["user"])

#     if NOTIFY_USERS_ON_ENTER_OR_LEAVE_ROOMS:
#         room.send_message(None, message.user)

#     room.websocket_group.discard(message.reply_channel)
#     message.channel_session['rooms'] = list(set(message.channel_session['rooms']).difference([room.id]))
#     message.reply_channel.send({
#         "text": json.dumps({
#             "leave": str(room.id),
#         }),
#     })