import hashlib

from party_rooms.models import MeetingPlace, PlaceVote, MeetingTime, TimeVote, CachedResult
from party_rooms.ajax_helper import *
from party_rooms.ws_sender import send_new_place, send_new_time, send_scenario


@needs_auth
@contains("POST", "description")
@specify_room
@integrity
def add_place(request, data, room):
    place = MeetingPlace.objects.create(room=room, author_id=request.user.pk, description=data["description"])
    send_new_place(place)
    return send_response(data={'place_id': place.pk})


@needs_auth
@contains("POST", "description")
@specify_room
@need_admin
def modify_description(request, data, room):
    room.description = data["description"]
    room.save()
    return send_response(data={'room_id': room.pk})


@needs_auth
@contains("POST", "password1", "password2")
@specify_room
@need_admin
def change_password(request, data, room):
    if data["password1"] != data["password2"]:
        return send_response(False)
    room.pass_hash = hashlib.md5(data["password1"].encode("utf-8")).hexdigest()
    room.save()
    return send_response(data={'room_id': room.pk})


@needs_auth
@contains("POST", "description", "time")
@specify_room
@integrity
def add_time(request, data, room):
    time = MeetingTime.objects.create(room=room, author_id=request.user.pk,
                                      description=(data["time"] + " " + data["description"]))
    send_new_time(time)
    return send_response(data={'time_id': time.pk})


@needs_auth
@contains("GET", "choice", "type", "id")
@specify_room
@save_vote(MeetingPlace)
def add_place_answer(request, meeting_place):
    return PlaceVote.objects.get_or_create(user=request.user, place=meeting_place)[0]


@needs_auth
@contains("GET", "choice", "type", "id")
@specify_room
@save_vote(MeetingTime)
def add_time_answer(request, meeting_time):
    return TimeVote.objects.get_or_create(user=request.user, time=meeting_time)[0]


@needs_auth
@contains("POST", "option_id", "option_type")
@specify_room
@specify_scenario
@check_permissions
def delete_scenario(request, data, room, scenario):
    send_scenario(scenario, data["option_type"], "remove")
    return send_response(True, scenario.delete())


@needs_auth
@contains("POST", "option_id", "option_type", "description")
@specify_room
@specify_scenario
@check_permissions
def edit_scenario(request, data, room, scenario):
    scenario.description = data["description"]
    scenario.save()
    send_scenario(scenario, data["option_type"], "change")
    return send_response(True)


@needs_auth
def send_results(request, room_id):
    try:
        room = Room.objects.get(pk=room_id)
    except Room.DoesNotExist:
        return send_response(False)
    CachedResult.update_all(room)
    to_serializable = lambda x: {"place": str(x.place), "time": str(x.time),
                                 "people": x.participants, "rating": x.result_rating}
    return JsonResponse({
        'usercount': max(room.room_users.count(), 1),
        'results': [to_serializable(x) for x in
                    CachedResult.objects.filter(place__room=room)[:10]]})
