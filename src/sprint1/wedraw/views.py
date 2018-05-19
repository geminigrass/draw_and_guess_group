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


# Create your views here.
@login_required
def home(request):    
    return render(request,'wedraw/join_page.html', {})

def clear_room(request):
    controller_game = Controller.objects.all()[1]
    controller_default = Controller.objects.all()[0]

    profile_list = UserProfile.objects.filter(room=controller_game)
    for profile in profile_list:
        profile.room = controller_default
        profile.save()
    return HttpResponse("hello")


def add_score(request):
    if request.method == 'POST':
        user = request.user
        profile = user.userprofile
        profile.add_score(profile)
        profile.save()
    return HttpResponse(profile.score)

def selectWordType(request, type):
    print("type is :")
    print(type)
    if request.method == 'GET':
        return HttpResponse("")
    for p in tableword.objects.raw('select * from wedraw_tableword where wordfield = %s', [type] ):
        return HttpResponse(p.word)
    print("=====comehere!!!!!!!!!!!!!!!")
    
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
def guesser_page(request):
    return render(request, 'wedraw/game_guesser.html', {})

@login_required
def drawer_page(request):
    return render(request, 'wedraw/game_drawer.html', {})

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

def appendNewUser(request,time):

    if time == "undefined" :
        time="1970-01-01T00:00+00:00"
    max_time = time
    newuser =  User.objects.order_by('last_login').reverse()
    if len(newuser) > 0 :
        max_time = newuser[0].last_login
    user = User.objects.filter(last_login__gt=time).distinct()
    # if len(user) > 0:
    #     print("user[0].userprofile.score")
    #     print(user[0].userprofile.score)
    context = {"max_time":max_time, "users":user}
    
    return render(request, 'wedraw/newUsers.json', context, content_type='application/json')

def checkstatues(request):
    count = len(tableword.objects.all())
    context = {'userStatus': "true"}
    # print("checkstatues")
    # print(context)
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

# # TODO:create Defalult Controller for every profile
    if Controller.objects.count() == 0 :
        controller = Controller.objects.create(curr_round_number=0,
                                        curr_turn_number = 0,)
        controller.save()
    else:
        controller = Controller.objects.all()[0]
# TODO:create User ,UserProfile, Controller
    # Create the new user from the valid form data
    new_user = User.objects.create_user(username = form.cleaned_data['username'], \
                                        password = form.cleaned_data['password1'],)
    new_user.save()
    profile = UserProfile.objects.create(user=new_user,room=controller)
    profile.save()


     # Logs in the new user and redirects to his/her home page
    new_user = authenticate(username = request.POST['username'], \
                            password = request.POST['password1'])

    login(request,new_user)

    return redirect('/wedraw/')

@login_required
def join_game(request):

# There is only 1 Default Controller
    if Controller.objects.count() == 1 :
        controller = Controller.objects.create(curr_round_number=0,
                                        curr_turn_number = 0,)
        controller.room_name="111"
        controller.save()
# already exist the game controller
    else:
        controller = Controller.objects.all()[1]
    user = request.user
# TODO: Enter the REAL Controller
    user.userprofile.room = controller
    user.userprofile.save()
    user.save()

    profile_list = UserProfile.objects.filter(room=controller)
    # he is the painter
    if len(profile_list) == 1 :
        return redirect(reverse('drawer'))
    else:
        return redirect(reverse('guesser'))
