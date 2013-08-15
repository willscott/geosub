import store
import time
from rulecollection import RuleCollection
from shapely.geometry import Point

class Deliver:
  """ Manage delivery of items to users. """
  def __init__(self, store):
    self.store = store
    self.rules = self.buildRules()

  def buildRules(self):
    categories = self.store.db.execute("select id from categories")
    rules = {}
    for cat in categories:
      listing = self.store.db.execute("select user, geofence from rules where category=(?)", cat)
      collection = RuleCollection()
      [collection.add(user, fence) for (user, fence) in listing]
      rules[cat[0]] = collection
    return rules

  def process(self, id, cat, item):
    if cat in self.rules:
      listing = self.rules[cat]
      point = Point(item['lat'], item['lon'])
      users = listing.match(point)
      print users
