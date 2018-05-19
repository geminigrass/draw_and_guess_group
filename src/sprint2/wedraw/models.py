from django.contrib.auth.models import User

# Create your models here.
from django.db import models
from channels import Group
import datetime

DEFAULT_CONTROLLER_ID = 0
DEFAULT_ROOM_LABLE = "000"

class Room(models.Model):
    name = models.TextField()
    label = models.SlugField(unique=True)
    host = models.CharField(max_length = 250,default = "",blank = True)

    # get the current users in the room
    @staticmethod
    def users_join_room(self):  
        users = []
        # get User queryset from get_curr_user_list
        # and append them to user_list
        user_list = self.get_curr_user_list(self)
        user = User.objects.filter(userprofile__in=user_list)
        for i in range(len(user)):
            users.append(user[i].username)
       
        return users

    @staticmethod
    def change_host(self):
        user_list = self.get_curr_user_list(self)
        user = User.objects.filter(userprofile__in=user_list)
        if len(user) != 0:
            self.host = user[0].username
            self.save()
            return self.host

    # get the drawer of the game
    @staticmethod
    def is_drawer(self):  
        # get User queryset from get_curr_user_list
        # and append them to user_list
        host = self.host
        drawer = host

        return drawer

    # @staticmethod
    # def user_status_change(self):
    #     user_list = self.get_curr_user_list(self)
    #     for i in user_list:
    #         i[0].status = 1
    #     return i

    def __unicode__(self):
        return self.id

    @staticmethod
    # TODO:we'll filter user by room in later sprint
    def get_curr_user_list(self):
        user_list = UserProfile.objects.filter(room=self)
        return user_list        

    # Check whether the room is full
    @staticmethod
    def room_is_full(self):
        max_number = 2
        users = self.users_join_room(self)
        if len(users) > max_number:
            return True
        else:
            return False

class Controller(models.Model):
    curr_round_number = models.IntegerField(default=0,blank=True)
    curr_turn_number = models.IntegerField(default=0,blank=True)
    room_name = models.CharField(default="000",blank=True,max_length=42)
    def __str__(self):
        return self.room_name

    # # curr_painter = models.ForeignKey(SimpleUser)
    # # TODO:in later work,we'll need an one-to-one field (host/room)to .get() controller
    #
    # # getters
    @staticmethod
# TODO:we'll filter user by room in later sprint
    def get_curr_user_list(self):
        profile_list = UserProfile.objects.filter(room=self)
        return User.objects.filter(userprofile__in=profile_list)
    #
    @staticmethod
# TODO: we'll change the parameter to be .get() the controller later
    def get_curr_painter(self):
        profile_list = UserProfile.objects.filter(room=self)
        curr_user_list = User.objects.filter(userprofile__in=profile_list)
        return curr_user_list[self.curr_turn_number]
    #
    @staticmethod
    def get_next_painter(self):
        profile_list = UserProfile.objects.filter(room=self)
        curr_user_list = User.objects.filter(userprofile__in=profile_list)
        curr_user_number = len(curr_user_list)
        self.curr_turn_number = (self.curr_turn_number + 1)%curr_user_number
        self.save()
        return curr_user_list[self.curr_turn_number]


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    score = models.IntegerField(default=0,blank=True)
    time = models.DateTimeField(auto_now_add=True)
    room = models.ForeignKey(Room,
                             on_delete=models.SET_NULL,
                             null=True,
                             default=DEFAULT_ROOM_LABLE)
    status = models.IntegerField(default = 0)

    def __str__(self):
        return self.user.username

    @staticmethod
    def get_score(self):
        return self.score

    @staticmethod
    def get_ready(self):
        self.status = 1
        return self.status

    @staticmethod
    def get_unready(self):
        self.status = 0
        return self.status

    @staticmethod
    def add_score(self):
        self.score += 3
        self.save()
        return self.score

    # old profile first
    class Meta:
        ordering = ['time']


class tableword(models.Model):
    wordId = models.IntegerField(primary_key = True)
    wordfield = models.CharField(max_length=30)
    word = models.CharField(max_length=30)
    hint1 = models.CharField(max_length=30)
    hint2 = models.CharField(max_length=30)
    hint3 = models.CharField(max_length=30)