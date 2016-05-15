import os

import tornadoredis.pubsub
import tornado.gen

import partisan.settings
import partisan.wsgi
import tornado.web
import tornado.websocket
import tornado.wsgi


class Application(tornado.web.Application):
    """
    Tornado application which serves our Django application.
    Tornado handles staticfiles and web sockets, Django handles everything else.
    """

    def __init__(self):
        settings = dict()
        settings["debug"] = True if partisan.settings.DEBUG else False

        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "partisan.settings")
        wsgi_app = tornado.wsgi.WSGIContainer(partisan.wsgi.application)
        static_path = partisan.settings.STATIC_ROOT

        handlers = [
            (r"/ws/(?P<room>\d+)/?", WebSocketHandler),
            (r"/ws/(?P<room>\d+)/(?P<specific>\w+)/?", WebSocketHandler),
            (r"/static/(.*)", tornado.web.StaticFileHandler, {'path': static_path}),
            (r".*", tornado.web.FallbackHandler, dict(fallback=wsgi_app)),
        ]

        tornado.web.Application.__init__(self, handlers, **settings)


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def __init__(self, application, request, *args, **kwargs):
        super().__init__(application, request, **kwargs)
        self.channels = []
        self.client = tornadoredis.Client(**partisan.settings.REDIS_SETTINGS)
        self.client.connect()

    @tornado.gen.engine
    def listen(self):
        if len(self.channels):
            yield tornado.gen.Task(self.client.subscribe, self.channels)
            self.client.listen(self.on_message)

    def open(self, *args, **kwargs):
        if 'room' in kwargs:
            self.channels.append("chat_for_{room}".format(**kwargs))
            if 'specific' in kwargs:
                self.channels.append("{specific}_for_{room}".format(**kwargs))
        self.listen()

    def on_message(self, msg):
        print(msg)
        if msg.kind == 'message':
            self.write_message(msg.body)
        elif msg.kind == 'disconnect':
            self.close()

    def on_close(self):
        if self.client.subscribed:
            self.client.unsubscribe(self.channels)
            self.client.disconnect()

    def check_origin(self, origin):
        return True


def broadcast(channel, message):
    c = tornadoredis.Client()
    c.connect()
    c.publish(channel, message)
    c.disconnect()
