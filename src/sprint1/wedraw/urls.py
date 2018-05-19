from django.conf.urls import include, url
#from django.contrib.auth import views as auth_views
from wedraw import views
from django.contrib import admin
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', views.home, name = 'home'),
    # TODO:
    url(r'^join-game$', views.join_game, name = 'join-game'),
    url(r'^login$',auth_views.login, {'template_name':'wedraw/login.html','redirect_authenticated_user': True},name = 'login'),
    #url(r'^grumblr/login',views.custom_login, name = 'userlogin'),
    # Route to log out a user and send them back to the log in page.
    url(r'^logout$',auth_views.logout_then_login,name='logout'),
    url(r'^signup',views.signup, name='signup'),

    # Route for our application's home page
    url(r'^drawer', views.drawer_page, name = 'drawer'),
    url(r'^guesser', views.guesser_page, name = 'guesser'),
    url(r'^getWord/(?P<word_id>\d+)$', views.getwords, name = 'getwords'),
    url(r'^getWordInfo', views.getwordsInfo, name = 'getwordsInfo'),
    url(r'^appendNewUser/(?P<time>.+)$', views.appendNewUser, name = 'appendNewUser'),
    url(r'^appendNewUser/?$', views.appendNewUser, name = 'appendNewUser'),
    #url(r'^new-a-turn', views.new_turn, name = 'new-a-turn'),
    #url(r'^get-curr-painter',views.get_curr_painter,name='get-curr-painter'),
    url(r'^add-score',views.add_score,name='add-score'),
    url(r'^clear-room',views.clear_room,name='clear-room'),
    url(r'^currentuser',views.checkstatues,name='check-userstatus'),
    url(r'^select/(?P<type>[a-zA-Z0-9_@\+\-]+)',views.selectWordType,name='selectWordType'),
]