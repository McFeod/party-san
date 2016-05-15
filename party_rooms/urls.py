from django.conf.urls import url
from party_rooms.views import *
from party_rooms.ajax import *


urlpatterns = [
    url("^$", start_page, name="start_page"),
    url("^logout/", logout_view, name="logout"),
    url("^new_room/$", add_room, name="add_room"),
    url("^help/", help_view, name="help"),
    url("^profile/", profile_view, name="profile"),
    url("^room/(?P<room_id>\d+)/$", room, name="room"),
    url("^room/(?P<room_id>\d+)/auth/$", room_auth, name="room_auth"),
    url("^room/(?P<room_id>\d+)/enter/$", enter_room, name="enter_room"),
    url("^room/(?P<room_id>\d+)/settings/$", settings_room, name="settings_room"),
    url("^room/(?P<room_id>\d+)/change_description/$", modify_description, name="change_description"),
    url("^room/(?P<room_id>\d+)/change_password/$", change_password, name="change_password"),
    url("^room/(?P<room_id>\d+)/add_users/$", add_users, name="add_users"),
    url("^room/(?P<room_id>\d+)/place/$", place_room, name="place_room"),
    url("^room/(?P<room_id>\d+)/delete/$", delete_scenario, name="delete_scenario"),
    url("^room/(?P<room_id>\d+)/edit/$", edit_scenario, name="edit_scenario"),
    url("^room/(?P<room_id>\d+)/time/$", time_room, name="time_room"),
    url("^room/(?P<room_id>\d+)/result/$", result_room, name="result_room"),
    url("^room/(?P<room_id>\d+)/result/get/$", send_results, name="send_results"),
    url("^room/(?P<room_id>\d+)/new_place/$", add_place, name="add_place"),
    url("^room/(?P<room_id>\d+)/new_time/$", add_time, name="add_time"),
    url("^room/(?P<room_id>\d+)/place/new_answer/$", add_place_answer, name="add_place_answer"),
    url("^room/(?P<room_id>\d+)/time/new_answer/$", add_time_answer, name="add_time_answer"),
    url(r'^accounts/password_change/done/$', go_to_profile, name='password_change_done'),
]
