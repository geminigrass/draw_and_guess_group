from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db import models
import datetime

DEFAULT_CONTROLLER_ID = 0

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
    room = models.ForeignKey(Controller,
                             on_delete=models.SET_NULL,
                             null=True,
                             default=DEFAULT_CONTROLLER_ID)

    def __str__(self):
        return self.user.username

    @staticmethod
    def get_score(self):
        return self.score

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