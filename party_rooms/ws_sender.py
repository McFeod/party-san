import json
from functools import partial
import redis

import partisan.settings


class RedisPublisher:
    class __Publisher:
        def __init__(self):
            self.redis = redis.Redis(**partisan.settings.REDIS_SETTINGS)

        def publish(self, channel, data):
            self.redis.publish(channel, data)

    instance = None

    @classmethod
    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = cls.__Publisher()
        return cls.instance


def send_scenario(obj, name, command):
    room_id = obj.room.pk
    channel = "%s_for_%d" % (name, room_id)
    data = {"id": room_id,
            "description": obj.description,
            "author_id": obj.author_id,
            "option_id": obj.pk,
            "channel": channel,
            "command": command
            }
    RedisPublisher().publish(channel, json.dumps(data))

send_new_place = partial(send_scenario, name="place", command="add")
send_new_time = partial(send_scenario, name="time", command="add")
