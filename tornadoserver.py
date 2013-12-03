from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from server import create_app

http_server = HTTPServer(WSGIContainer(create_app("settings.DevelopmentConfig")))
http_server.listen(80)
IOLoop.instance().start()
