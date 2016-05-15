from django.contrib import admin
from party_rooms.models import *
# Register your models here.

admin.site.register(Room)
admin.site.register(MeetingPlace)
admin.site.register(MeetingTime)
admin.site.register(PlaceVote)
admin.site.register(CachedResult)
admin.site.register(UserCachedResult)
