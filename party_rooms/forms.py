from django.forms import ModelForm
from registration.forms import RegistrationForm

from party_rooms.models import Room, User


class RoomForm(ModelForm):
    class Meta:
        model = Room
        exclude = []


class UserSettingsForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']