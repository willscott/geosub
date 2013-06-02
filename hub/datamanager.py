import tornado.web

import json
import random
import store
import string
import sys

class DataManager(tornado.web.RequestHandler):
  def initialize(self):
    self.store = store.Store("hub/live")

  @classmethod
  def install(cls, handlers):
    handlers.append((r"/data/?(.*)", DataManager))

  def check_xsrf_cookie(self):
    return True
  
  def post(self, path):
    if path == 'list':
        self.write(
            json.dumps('DO something'))
        return
    else:
      self.write("hello")

  def get(self, path):
    if path == 'list':
        self.content_type = 'application/json'
        data = self.store.db.execute('select lat, lon, data from items').fetchall();
        self.write(json.dumps(data))
        return
