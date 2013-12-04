from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado import autoreload
from server import create_app

import logging
import signal
import time

def sig_handler(sig, frame):
    logging.warning('Caught signal: %s', sig)
    IOLoop.instance().add_callback(stopTornado)

def startTornado():
    global http_server
    http_server = HTTPServer(WSGIContainer(create_app("settings.DevelopmentConfig")))
    http_server.listen(80)
    ioloop = IOLoop.instance()
    autoreload.start(ioloop)
    ioloop.start()

def stopTornado():
    logging.info('Stopping http server')
    http_server.stop()
    io_loop = IOLoop.instance()
    deadline = time.time() + 3
    def stop_loop():
        now = time.time()
        if now < deadline and (io_loop._callbacks or io_loop._timeouts):
            io_loop.add_timeout(now + 1, stop_loop)
        else:
            io_loop.stop()
            logging.info('Shutdown')
    stop_loop()


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, sig_handler)
    signal.signal(signal.SIGINT, sig_handler)
    startTornado()

