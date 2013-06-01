import tornado.web
from apiclient.discovery import build

import httplib2
from oauth2client.client import AccessTokenRefreshError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

import json
import random
import store
import string

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']

class UserManager(tornado.web.RequestHandler):
  def initialize(self):
    self.store = store.Store("hub/live")

  @classmethod
  def install(cls, handlers):
    handlers.append((r"/user/?(.*)", UserManager))

  def check_xsrf_cookie(self):
    return True
  
  def mksession(self):
    return ''.join(random.choice(string.ascii_uppercase + string.digits)
                      for x in xrange(32))

  def post(self, path):
    if path == 'connect':
      try:
        code = self.get_argument("data")
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
      except FlowExchangeError:
        self.set_status(401)
        self.content_type = 'application/json'
        self.write(
            json.dumps('Failed to upgrade the authorization code.'))
        return

      gplus_id = credentials.id_token['sub']
      print "seeing user id " + gplus_id
      if self.store.has(gplus_id, 'users'):
        data = self.store.db.execute('select * from users where id=(?)', (gplus_id,)).fetchall();
        session = self.mksession()
        print "Current session for user should now be  " + session
        self.store.db.execute('update users set session=(?) where id=(?)', (session, gplus_id))
        self.store.db.commit()        
        self.content_type = 'application/json'
        self.write(json.dumps({'status':'existing', 'uid':gplus_id,'session':session, 'prefs':data[0][3]}))
      else:
        print "store doesn't have user"
        session = self.mksession()
        self.store.db.execute('insert into users (id, session, credentials) values ((?), (?), (?))', (gplus_id, session, credentials.to_json()))
        self.store.db.commit()
        self.content_type = 'application/json'
        # TODO: cleanup default prefs.
        self.write(json.dumps({'status':'new','uid': gplus_id,'session': session,'prefs':"{\"feeds\":{\"feed_construction\":true}}"}))
    elif path == 'sync':
      try:
        token = self.get_argument("token")
        id = self.get_argument("id")
        prefs = self.get_argument("data")
        user_query = self.store.db.execute('select * from users where id=(?) and session=(?)', (id, token)).fetchall()
        if len(user_query):
          return self.sync(id, user_query[0][3], json.loads(prefs))
        print "USR lookup " + id + " for session " + token
        user_query = self.store.db.execute('select * from users where id=(?)', (id, )).fetchall()
        print "in db is session " + user_query[0][2]
        self.write(json.dumps({'status':'user lookup / auth error'}))
      except Exception as e:
        self.write(json.dumps({'status':'real error:' + str(e)}))
    else:
      self.write("hello")

  def sync(self, id, db_prefs, prefs):
    base = {}
    if len(db_prefs):
      base = json.loads(db_prefs)
    
    #Update the portion of user prefs that the user can change.
    if prefs['email_id']: base['email_id'] = prefs['email_id']
    if prefs['feeds']: base['feeds'] = prefs['feeds']
    
    #TODO: syncronize prefs with db rules table.
    

    prefstr = json.dumps(base)
    self.store.db.execute('update users set prefs=(?) where id=(?)', (prefstr, id));
    self.store.db.commit()
    self.write(json.dumps({'status':'good', 'prefs': prefstr}))
    print "Syncing " + id
