#!/usr/bin/env python
"""
  Web server for GeoSub Front-end
"""

import os, sys, inspect, time, math
this_folder = os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0])
tornado_folder = os.path.join(this_folder, "tornado")
if tornado_folder not in sys.path:
  sys.path.insert(0, tornado_folder)
lib_folder = os.path.join(this_folder, "lib")
if lib_folder not in sys.path:
  sys.path.insert(0, lib_folder)


import base64
import logging
import json
import os.path
import tornado.ioloop
import tornado.options
import tornado.web
import uuid
from hub import UserManager
from hub import DataManager

from tornado.options import define, options

default_port = 8080
if 'PORT' in os.environ:
  default_port = os.environ['PORT']
define("port", default=default_port, help="port", type=int)

rootLogger = logging.getLogger('')
rootLogger.setLevel(logging.ERROR)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/config", ConfigHandler)
        ]
        settings = dict(
            cookie_secret=base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes),
            template_path=os.path.join(os.path.dirname(__file__), "template"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
            autoescape=None,
        )
        UserManager.install(handlers)
        DataManager.install(handlers)
        tornado.web.Application.__init__(self, handlers, **settings)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html", CLIENT_ID=CLIENT_ID)

class ConfigHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("config.html")

def main():
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
