import tornado.web
from apiclient.discovery import build

import httplib2
from oauth2client.client import AccessTokenRefreshError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

import json
import store

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']

class UserManager(tornado.web.RequestHandler):
  def initialize(self):
    self.store = store.Store("live")

  @classmethod
  def install(cls, handlers):
    handlers.append((r"/user/?(.*)", UserManager))

  def get(self, path):
    if path=='connect':
      try:
        code = self.get_argument("data")
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = '/user/redirect'
        credentials = oauth_flow.step2_exchange(code)
      except FlowExchangeError:
        self.set_status(401)
        self.content_type = 'application/json'
        self.write(
            json.dumps('Failed to upgrade the authorization code.'))

      gplus_id = credentials.id_token['sub']
      if self.store.has(gplus_id, 'users'):
        data = self.store.db.execute('select * from users where id=(?)', gplus_id);
        self.content_type = 'application/json'
        self.write(json.dumps({'status':'existing', 'prefs':}))
      else:
        self.store.db.execute('insert into users (id, credentials) values ((?), (?))', (gplus_id, json.dumps(credentials)))
        self.content_type = 'application/json'
        self.write(json.dumps({'status':'new','prefs':}))
    else:
      self.write("hello")
