from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado import autoreload
from server import create_app


http_server = HTTPServer(WSGIContainer(create_app("settings.DevelopmentConfig")))
http_server.listen(5000)
ioloop = IOLoop.instance()
autoreload.start(ioloop)
ioloop.start()
