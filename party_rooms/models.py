from django.db import models
from django.contrib.auth.models import User
from party_rooms.logic import *


class Room(models.Model):
    usermade = models.BooleanField(default=True)
    room_users = models.ManyToManyField(User)
    admin_id = models.IntegerField(null=True)
    pass_hash = models.CharField(max_length=32, null=True)
    description = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.description

    def drop_caches(self):
        results = CachedResult.objects.filter(place__room_id=self.pk)
        Vote.mark_to_update(results)


class MeetingOption(models.Model):
    description = models.TextField(verbose_name="описание места")
    room = models.ForeignKey("Room")
    author_id = models.IntegerField(default=0)

    def __str__(self):
        return self.description

    class Meta:
        abstract = True
        unique_together = (("description", "room"),)


class MeetingTime(MeetingOption):
    pass


class MeetingPlace(MeetingOption):
    pass


class Conflict(models.Model):
    place = models.ForeignKey("MeetingPlace")
    time = models.ForeignKey("MeetingTime")


class Vote(models.Model):
    user = models.ForeignKey(User)
    possibility = models.IntegerField(choices=((UNDEFINED, "не задано"),
                                               (GOOD, "подходит"),
                                               (BAD, "не подходит"),
                                               (NOT_SURE, "возможно, подходит")),
                                      default=UNDEFINED)
    rating = models.IntegerField(choices=((UNDEFINED, "не задано"),
                                          (GOOD, "одобрительно"),
                                          (BAD, "неодобрительно"),
                                          (NOT_SURE, "нейтрально")),
                                 default=0)

    class Meta:
        abstract = True

    @staticmethod
    def mark_to_update(collection):
        for result in collection:
            result.need_calc = True
            result.save()


class PlaceVote(Vote):
    place = models.ForeignKey("MeetingPlace")

    def __str__(self):
        return "%s: %s" % (self.user, self.place)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(PlaceVote, self).save(force_insert, force_update, using, update_fields)
        self.mark_to_update(CachedResult.objects.filter(place=self.place))
        self.mark_to_update(UserCachedResult.objects.filter(user=self.user, place=self.place))


class TimeVote(Vote):
    time = models.ForeignKey("MeetingTime")

    def __str__(self):
        return "%s: %s" % (self.user, self.time)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(TimeVote, self).save(force_insert, force_update, using, update_fields)
        self.mark_to_update(CachedResult.objects.filter(time=self.time))
        self.mark_to_update(UserCachedResult.objects.filter(user=self.user, time=self.time))


class AbstractCachedResult(models.Model):
    need_calc = models.BooleanField(default=True)
    place = models.ForeignKey("MeetingPlace")
    time = models.ForeignKey("MeetingTime")
    result_rating = models.IntegerField(null=True)

    def get_room(self):
        return self.place.room

    class Meta:
        abstract = True


class CachedResult(AbstractCachedResult):
    participants = models.IntegerField(default=0)

    def calc(self):
        if self.need_calc:
            self.participants = 0
            self.result_rating = 0
            for user in self.get_room().room_users.all():
                user_result = UserCachedResult.objects.get_or_create(
                    user=user, place=self.place, time=self.time)[0].calc()
                self.result_rating += user_result.result_rating
                if user_result.is_possible:
                    self.participants += 1
            self.need_calc = False
            self.save()
        return self

    @staticmethod
    def update_all(room):
        for m_place in MeetingPlace.objects.filter(room=room):
            for m_time in MeetingTime.objects.filter(room=room):
                CachedResult.objects.get_or_create(place=m_place, time=m_time)[0].calc()

    class Meta:
        ordering = ["-result_rating"]


class UserCachedResult(AbstractCachedResult):
    is_possible = models.BooleanField(default=True)
    user = models.ForeignKey(User)

    def calc(self):
        if self.need_calc:
            place_vote = PlaceVote.objects.get_or_create(user=self.user, place=self.place)[0]
            time_vote = TimeVote.objects.get_or_create(user=self.user, time=self.time)[0]
            self.result_rating = calc_rating(place_vote, time_vote)
            self.is_possible = check_possibility(place_vote, time_vote)
            self.need_calc = False
            self.save()
        return self
