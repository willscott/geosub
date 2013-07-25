import os, sys, inspect
this_folder = os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0])
lib_folder = os.path.join(this_folder, "..", "lib")
if lib_folder not in sys.path:
  sys.path.insert(0, lib_folder)

import store
import hub
import time

class Daemon:
  """ Deals with feeds and pulls in new items. """

  def __init__(self, db):
    self.store = store.Store(db)

  def start(self):
    while True:
      feeds = self.store.db.execute("SELECT * FROM categories")
      for (fid, url) in feeds:
        data = self.getItems(url)
        for itm in data:
          if not self.store.has(itm['id']):
            print "daemon added new item"
            parsed = itm['get']()
            self.store.addItem(itm['id'], fid, (parsed['lat'], parsed['lon']), parsed['time'], parsed['data'])
      time.sleep(60)

  def getItems(self, url):
    try:
      return hub.getProvider(url).pull()
    except:
      print "No provider found for " + url
      return []

def main():
    app = Daemon("live")
    app.start()

if __name__ == "__main__":
    main()