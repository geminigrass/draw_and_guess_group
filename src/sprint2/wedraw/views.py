from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

from wedraw.models import *
from wedraw.forms import *
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect

import datetime
import time
from random import randint
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from haikunator import Haikunator

# haikunator is used to generate random room names
haikunator = Haikunator()

# Create your views here.
@login_required
def home(request):    
    rooms = Room.objects.order_by("label")
    return render(request,'wedraw/home.html', {'rooms':rooms})

# Action for creating a new room
@login_required
def new_room(request):
    """
    Randomly create a new room, and redirect to it.
    """
    new_room = None
    while not new_room:
        label = haikunator.haikunate()

        if Room.objects.filter(label=label).exists():
            continue
        # create a new room with label and host being the request user
        new_room = Room.objects.create(label=label, host = request.user.username)
    return redirect(join_room, label=label)

# Action for join the room
@login_required
def join_room(request, label):
    
    rooms = Room.objects.get(label=label)
    user = request.user

    user.userprofile.room = rooms
    user.userprofile.save()

    users = rooms.users_join_room(rooms)
    # if the room is full of users, current user can't join that room
    if rooms.room_is_full(rooms):
        return redirect('home')
    # else let him join that room
    else:
        return render(request, "wedraw/gameroom.html", {
        'room': rooms,'users':users,'userprofile':user.userprofile
    })

# Action for leave the rooms.
# When user leaves the room, set his foreign key to default
# and redirect him to the home page
@login_required
def leave_room(request,label):
    default_room = Room.objects.get(label = "000")
    rooms = Room.objects.get(label = label)
    user = request.user 
    user.userprofile.room = default_room
    user.userprofile.save()

    # If the host left the room, change the room host
    if user.username == rooms.host:
        rooms.change_host(rooms)
        
    user_list = rooms.get_curr_user_list(rooms)
    # If the last user left the room, delete the room instance
    if (len(user_list) == 0):
        Room.objects.filter(label=rooms.label).delete()
    return redirect('home')


def clear_room(request):
    controller_game = Controller.objects.all()[1]
    controller_default = Controller.objects.all()[0]

    profile_list = UserProfile.objects.filter(room=controller_game)
    for profile in profile_list:
        profile.room = controller_default
        profile.save()
    return HttpResponse("hello")

@login_required
def add_score(request):
    #if request.method == 'POST':
    user = request.user
    profile = user.userprofile
    profile.add_score(profile)
    profile.save()
    
    context = {'username':user.username,'score':profile.score}
    return render(request,'wedraw/score.json',context, content_type = 'application/json')
    #return HttpResponse(profile)

def selectWordType(request):

    for p in tableword.objects.raw('select * from wedraw_tableword ORDER BY RANDOM() LIMIT 1'):
        return HttpResponse(p.word)
    
    return HttpResponse("")
# These functions might be useful in sprint 2
# def get_curr_painter(request):
#     controller = Controller.objects.all()[1]
#     curr_paiter = controller.get_curr_painter(controller)
#     return HttpResponse(curr_paiter == request.user)

# def new_turn(request):

#     controller = Controller.objects.all()[1]

#     next_user = controller.get_next_painter(controller)
#     return HttpResponse(next_user == request.user)

@login_required
def guesser_page(request,label):
    room = Room.objects.get(label = label)
    users = room.users_join_room(room)
    user_list = room.get_curr_user_list(room)
    score1 = 0
    score2 = 0
    #user = User.objects.filter(userprofile__in=user_list)
    for user in user_list:
        if user == request.user.userprofile:
            # guesser score
            score1 = user.score
        else:
            # drawer score
            score2 = user.score
    
    return render(request, 'wedraw/game_guesser.html', {'room':room,'users':users,'score1':score1,'score2':score2})

@login_required
def drawer_page(request,label):
    room = Room.objects.get(label = label)
    users = room.users_join_room(room)
    user_list = room.get_curr_user_list(room)
    score1 = 0
    score2 = 0
    #user = User.objects.filter(userprofile__in=user_list)
    for user in user_list:
        if user == request.user.userprofile:
            # drawer score
            score2 = user.score
        else:
            # guesser score
            score1 = user.score
    return render(request, 'wedraw/game_drawer.html', {'room':room,'users':users,'score1':score1,'score2':score2})

@login_required
def getwordsInfo(request):
    # Render to game_drawer page, for now
    context = {}
    count = len(tableword.objects.all())
    if count > 0 :
        random_index = randint(0, count-1) # should change to count in python 3 
        randomWord = tableword.objects.all()[random_index]

        context = {'word': randomWord.word,'hint1':randomWord.hint1,'hint2':randomWord.hint2,'hint3':randomWord.hint3}
    else:
        context["words"]="no words existing"
    return render(request, 'wedraw/worddetail.json', context, content_type='application/json')

# def appendNewUser(request,time):

#     if time == "undefined" :
#         time="1970-01-01T00:00+00:00"
#     max_time = time
#     newuser =  User.objects.order_by('last_login').reverse()
#     if len(newuser) > 0 :
#         max_time = newuser[0].last_login
#     user = User.objects.filter(last_login__gt=time).distinct()
#     # if len(user) > 0:
#     #     print("user[0].userprofile.score")
#     #     print(user[0].userprofile.score)
#     context = {"max_time":max_time, "users":user}
    
#     return render(request, 'wedraw/newUsers.json', context, content_type='application/json')

def checkstatues(request):
    count = len(tableword.objects.all())
    context = {'userStatus': "true"}

    return render(request, 'wedraw/userStatus.json', context, content_type='application/json')

@login_required
def getwords(request, word_id):

    mywords = tableword.objects.filter(wordId=word_id)
    myword = mywords[0]

    context = {'word': myword.word,'hint1':myword.hint1,'hint2':myword.hint2,'hint3':myword.hint3}

    return render(request, 'wedraw/word.json', context, content_type='application/json')

# Action for the signup route
def signup(request):
    if request.user.is_authenticated():
        return redirect('home')
    context={}
    errors=[]

    # Just display the signup form if this is a GET request
    if request.method== 'GET':
        context['form'] = SignUpForm()
        return render(request,'wedraw/signup.html',context)

    form = SignUpForm(request.POST)
    context['form'] = form

    if not form.is_valid():
        errors.append(form.errors)
        context = {'form':form,'errors':errors}
        return render(request,'wedraw/signup.html', context)

# # # TODO:create Defalult Controller for every profile
    if Room.objects.count() == 0 :
        room = Room.objects.create(label = "000")
        room.save()
    else:
        room = Room.objects.get(label = "000")

# TODO:create User ,UserProfile, Controller
    # Create the new user from the valid form data
    new_user = User.objects.create_user(username = form.cleaned_data['username'], \
                                        password = form.cleaned_data['password1'],)
    new_user.save()
    profile = UserProfile.objects.create(user=new_user,room = room)
    profile.save()


     # Logs in the new user and redirects to his/her home page
    new_user = authenticate(username = request.POST['username'], \
                            password = request.POST['password1'])

    login(request,new_user)

    return redirect('/wedraw/')

# Action for join the game
@login_required
def join_game(request,label):

# # There is only 1 Default Controller
#     if Controller.objects.count() == 1 :
#         controller = Controller.objects.create(curr_round_number=0,
#                                         curr_turn_number = 0,)
#         controller.room_name="111"
#         controller.save()
# # already exist the game controller
#     else:
#         controller = Controller.objects.all()[1]
    room = Room.objects.get(label = label)
    user = request.user
# TODO: Enter the REAL Controller
    user.userprofile.room = room
    user.userprofile.save()
    user.save()

    profile_list = UserProfile.objects.filter(room=room)
    # find out who is going to be the drawer
    drawer = room.is_drawer(room)

    if user.username == drawer:
         return redirect('drawer',label)
    else:
        return redirect('guesser',label)
   
