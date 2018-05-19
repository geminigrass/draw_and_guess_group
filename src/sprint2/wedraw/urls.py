from django.conf.urls import include, url
#from django.contrib.auth import views as auth_views
from wedraw import views
from django.contrib import admin
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', views.home, name = 'home'),
    # TODO:
    url(r'^join-game/(?P<label>[\w-]{,50})/$', views.join_game, name = 'join-game'),
    url(r'^login$',auth_views.login, {'template_name':'wedraw/login.html','redirect_authenticated_user': True},name = 'login'),
    #url(r'^grumblr/login',views.custom_login, name = 'userlogin'),
    # Route to log out a user and send them back to the log in page.
    url(r'^logout$',auth_views.logout_then_login,name='logout'),
    url(r'^signup',views.signup, name='signup'),

    # Route for our application's home page

    url(r'^(?P<label>[\w-]{,50})/drawer$', views.drawer_page, name = 'drawer'),
    url(r'^(?P<label>[\w-]{,50})/guesser$', views.guesser_page, name = 'guesser'),
    url(r'^getWord/(?P<word_id>\d+)$', views.getwords, name = 'getwords'),
    url(r'^getWordInfo', views.getwordsInfo, name = 'getwordsInfo'),
    # url(r'^appendNewUser/(?P<time>.+)$', views.appendNewUser, name = 'appendNewUser'),
    # url(r'^appendNewUser/?$', views.appendNewUser, name = 'appendNewUser'),
    #url(r'^new-a-turn', views.new_turn, name = 'new-a-turn'),
    #url(r'^get-curr-painter',views.get_curr_painter,name='get-curr-painter'),
    url(r'^add-score',views.add_score,name='add-score'),
    url(r'^clear-room',views.clear_room,name='clear-room'),

    url(r'^new/$', views.new_room, name='new_room'),
    # join game room
    url(r'^currentuser',views.checkstatues,name='check-userstatus'),
    url(r'^select/$',views.selectWordType,name='selectWordType'),
    url(r'^leave-room/(?P<label>[\w-]{,50})/$',views.leave_room,name='leave-room'),
    # url(r'^get_ready/(?P<label>[\w-]{,50})/$',views.get_ready,name = 'get-ready'),
    # url(r'^get_unready/(?P<label>[\w-]{,50})/$',views.get_unready,name = 'get-unready'),

    url(r'^(?P<label>[\w-]{,50})/$', views.join_room, name='join_room'),
]