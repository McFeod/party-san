import hashlib
import operator
from functools import reduce

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.views.decorators.http import require_POST

from party_rooms.forms import *
from party_rooms.models import Room, PlaceVote, TimeVote, User
from party_rooms.view_decorators import basic_view, find_room, check_room_auth


@login_required
@basic_view('party_rooms/all_rooms.html')
def start_page(request):
    return {'room_list': request.user.room_set.all}


@login_required
def add_room(request):
    if request.method == 'POST':
        description = request.POST['description']
        pass_hash = hashlib.md5(request.POST['password'].encode('utf-8')).hexdigest()
        new_room = Room.objects.create(pass_hash=pass_hash,
                                       description=description,
                                       admin_id=request.user.pk
                                       )
        new_room.room_users.add(request.user)
        new_room.save()
        return HttpResponseRedirect(reverse('party:room', kwargs={'room_id': new_room.pk}))
    else:
        return HttpResponseRedirect(reverse('party:start_page'))


@login_required
@find_room
@check_room_auth
@basic_view('party_rooms/room_generic.html')
def room(request, current_room):
    return {'room': current_room,
            'is_admin': (request.user.pk == current_room.admin_id)}


@login_required
@find_room
@check_room_auth
@basic_view('party_rooms/room_settings.html')
def settings_room(request, current_room):
    return {'room': current_room,
            'is_admin': (request.user.pk == current_room.admin_id),
            'form': RoomForm(instance=current_room),
            'possible_users': get_possible_users(current_room)}


@login_required
@find_room
@check_room_auth
@basic_view('party_rooms/room_for_place.html')
def place_room(request, current_room):
    def answer(offer):
        return offer, get_or_none(PlaceVote, user=request.user, place=offer)
    return {'room': current_room,
            'options': map(answer, current_room.meetingplace_set.all()),
            'is_admin': (request.user.pk == current_room.admin_id)}


@login_required
@find_room
@check_room_auth
@basic_view('party_rooms/room_for_time.html')
def time_room(request, current_room):
    def answer(offer):
        return offer, get_or_none(TimeVote, user=request.user, time=offer)
    return {'room': current_room,
            'options': map(answer, current_room.meetingtime_set.all()),
            'is_admin': (request.user.pk == current_room.admin_id)}


@login_required
@find_room
@check_room_auth
@basic_view('party_rooms/room_for_result.html')
def result_room(request, current_room):
    return {'room': current_room,
            'is_admin': (request.user.pk == current_room.admin_id)}


@login_required
@find_room
@basic_view('party_rooms/room_auth.html')
def room_auth(request, current_room):
    if request.user in current_room.room_users.all():
        return HttpResponseRedirect(reverse('party:room', kwargs={'room_id': current_room.pk}))
    return {'room': current_room}


@login_required
@require_POST
@find_room
def enter_room(request, current_room):
    if 'password' in request.POST:
        hash_sum = hashlib.md5(request.POST['password'].encode('utf-8')).hexdigest()
        if current_room.pass_hash == hash_sum:
            current_room.room_users.add(request.user)
            current_room.drop_caches()
            return HttpResponseRedirect(reverse('party:room', kwargs={'room_id': current_room.pk}))
    return HttpResponseRedirect(reverse('party:room_auth', kwargs={'room_id': current_room.pk}))


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('party:start_page'))


def go_to_profile(request):
    return HttpResponseRedirect(reverse('party:profile'))


@login_required
@basic_view("party_rooms/help.html")
def help_view(request):
    return {}


@login_required
@basic_view("party_rooms/profile.html")
def profile_view(request):
    if request.method == "POST":
        form = UserSettingsForm(request.POST, instance=request.user)
        try:
            form.save()
            return {"saved": True, "form": form}
        except ValueError:
            return {"saved": False, "form": form}
    return {"saved": False, "form": UserSettingsForm(instance=request.user)}


def get_or_none(model, *args, **kwargs):
    try:
        return model.objects.get(*args, **kwargs)
    except model.DoesNotExist:
        return None


@login_required
@require_POST
@find_room
def add_users(request, current_room):
    if request.user.pk == current_room.admin_id:
        try:
            for user_id in request.POST['users']:
                user = User.objects.get(pk=int(user_id))
                current_room.room_users.add(user)
            current_room.drop_caches()
        except (KeyError, User.DoesNotExist):
            pass
    return HttpResponseRedirect(reverse('party:settings_room',  kwargs={'room_id': current_room.pk}))


def get_possible_users(current_room):
    def make_set(from_room):
        return set(from_room.room_users.all())
    admin = User.objects.get(pk=current_room.admin_id)
    user_set = reduce(operator.or_, map(make_set, admin.room_set.all()))
    return user_set.difference(set(current_room.room_users.all()))
