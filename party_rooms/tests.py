from django.test import TestCase
from party_rooms.logic import *
from party_rooms.models import PlaceVote, TimeVote, User, MeetingTime, MeetingPlace


class PartyTestCase(TestCase):

    def test_result_on_defaults(self):
        first = PlaceVote(user=User(), place=MeetingPlace(), possibility=UNDEFINED, rating=UNDEFINED)
        second = TimeVote(user=User(), time=MeetingTime(), possibility=UNDEFINED, rating=UNDEFINED)
        self.assertEquals(calc_rating(first, second), 5)

    def test_result_if_dont_care(self):
        first = PlaceVote(user=User(), place=MeetingPlace(), possibility=NOT_SURE, rating=NOT_SURE)
        second = TimeVote(user=User(), time=MeetingTime(), possibility=NOT_SURE, rating=NOT_SURE)
        self.assertEquals(calc_rating(first, second), 5)

    def test_result_if_time_is_better(self):
        first = PlaceVote(user=User(), place=MeetingPlace(), possibility=NOT_SURE, rating=NOT_SURE)
        second = TimeVote(user=User(), time=MeetingTime(), possibility=GOOD, rating=GOOD)
        self.assertEquals(calc_rating(first, second), 5)

    def test_result_if_place_is_better(self):
        first = PlaceVote(user=User(), place=MeetingPlace(), possibility=GOOD, rating=GOOD)
        second = TimeVote(user=User(), time=MeetingTime(), possibility=NOT_SURE, rating=NOT_SURE)
        self.assertEquals(calc_rating(first, second), 5)

    def test_result_if_time_is_much_better(self):
        first = PlaceVote(user=User(), place=MeetingPlace(), possibility=BAD, rating=BAD)
        second = TimeVote(user=User(), time=MeetingTime(), possibility=GOOD, rating=GOOD)
        self.assertEquals(calc_rating(first, second), 0)

    def test_result_if_place_is_much_better(self):
        first = PlaceVote(user=User(), place=MeetingPlace(), possibility=GOOD, rating=GOOD)
        second = TimeVote(user=User(), time=MeetingTime(), possibility=BAD, rating=BAD)
        self.assertEquals(calc_rating(first, second), 0)

    def test_result_on_good_mid(self):
        first = PlaceVote(user=User(), place=MeetingPlace(), possibility=GOOD, rating=NOT_SURE)
        second = TimeVote(user=User(), time=MeetingTime(), possibility=GOOD, rating=NOT_SURE)
        self.assertEquals(calc_rating(first, second), 9)

    def test_result_on_good_bad(self):
        first = PlaceVote(user=User(), place=MeetingPlace(), possibility=GOOD, rating=BAD)
        second = TimeVote(user=User(), time=MeetingTime(), possibility=GOOD, rating=BAD)
        self.assertEquals(calc_rating(first, second), 3)

    def test_result_on_good_good(self):
        first = PlaceVote(user=User(), place=MeetingPlace(), possibility=GOOD, rating=GOOD)
        second = TimeVote(user=User(), time=MeetingTime(), possibility=GOOD, rating=GOOD)
        self.assertEquals(calc_rating(first, second), 10)

    def test_result_on_mid_good(self):
        first = PlaceVote(user=User(), place=MeetingPlace(), possibility=NOT_SURE, rating=GOOD)
        second = TimeVote(user=User(), time=MeetingTime(), possibility=NOT_SURE, rating=GOOD)
        self.assertEquals(calc_rating(first, second), 7)

    def test_result_on_mid_bad(self):
        first = PlaceVote(user=User(), place=MeetingPlace(), possibility=NOT_SURE, rating=BAD)
        second = TimeVote(user=User(), time=MeetingTime(), possibility=NOT_SURE, rating=BAD)
        self.assertEquals(calc_rating(first, second), 2)

    def test_result_on_bad_good(self):
        first = PlaceVote(user=User(), place=MeetingPlace(), possibility=BAD, rating=GOOD)
        second = TimeVote(user=User(), time=MeetingTime(), possibility=BAD, rating=GOOD)
        self.assertEquals(calc_rating(first, second), 1)

    def test_result_on_bad_mid(self):
        first = PlaceVote(user=User(), place=MeetingPlace(), possibility=BAD, rating=NOT_SURE)
        second = TimeVote(user=User(), time=MeetingTime(), possibility=BAD, rating=NOT_SURE)
        self.assertEquals(calc_rating(first, second), 0)

    def test_result_on_bad_bad(self):
        first = PlaceVote(user=User(), place=MeetingPlace(), possibility=BAD, rating=BAD)
        second = TimeVote(user=User(), time=MeetingTime(), possibility=BAD, rating=BAD)
        self.assertEquals(calc_rating(first, second), 0)
