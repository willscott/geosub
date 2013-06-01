import sqlite3
import json

class Store:
  """ Creates & maintains a location-filterable storage of items. """
  def __init__(self, db):
    if isinstance(db, str):
      db = sqlite3.connect(db)
    self.db = db;
    self.ensureSchema()

  def ensureSchema(self):
    sql = 'create table if not exists items (id text PRIMARY KEY, category integer, lat real, lon real, ts real, data BLOB)'
    self.db.execute(sql)
    sql = 'create table if not exists categories (id INTEGER PRIMARY KEY AUTOINCREMENT, label text)'
    self.db.execute(sql)
    sql = 'create table if not exists users (id text PRIMARY KEY, credentials text, session text, prefs text)'
    self.db.execute(sql)
    sql = 'create table if not exists rules (user text not null, category integer not null, geofence text, primary key (user, category))'
    self.db.commit()

  def getItems(self, area, since):
    sql = 'select * from items where ts > (?) and '
    values = (since, )
    areaInfo = [descriptor.toSql() for descriptor in area]
    sql += ' and '.join([itm[0] for itm in areaInfo])
    values += tuple([itm[1] for itm in areaInfo])

    c = self.db.cursor()
    c.execute(sql, values)
    return c

  def has(self, id, fr="items"):
    sql = 'select * from ' + fr + ' where id=(?)'
    val = self.db.execute(sql, (id,))
    for l in val:
      return True
    return False

  def addItem(self, id, category, location, time, item):
    c = self.db.cursor()
    sql = 'insert into items values (?, ?, ?, ?, ?, ?)'
    vals = (id, category, location[0], location[1], time, json.dumps(item))
    print vals
    c.execute(sql, vals)
    self.db.commit()
    #TODO: Notify subscribers.
