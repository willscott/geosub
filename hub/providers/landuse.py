import feedparser
import re
import time
import md5
from geopy import geocoders

url = "http://web1.seattle.gov/dpd/luib/RSSAllAreas.aspx"

class LandUse:
  def __init__(self):
    print "landuse created"
    self.coder = geocoders.GoogleV3()

  def pull(self):
    feed = feedparser.parse(url)
    items = feed["items"]
    #map items to a useful format
    return map(self.prepare, items)

  def prepare(self, item):
    def makeItem():
      return self.feed2data(item)
    return {'id': md5.new(item.title).hexdigest() , 'get':makeItem}

  def feed2data(self, item):
    out = {'time': 0, 'lat':0, 'lon': 0, 'data': ''}
    out['time'] = time.time()
    loc = re.sub('\(Project[^()]*\)', '', item.description)
    place = self.coder.geocode(loc + " Seattle, WA")
    out['lat'] = place[1][0]
    out['lon'] = place[1][1]
    out['data'] = item.title
    return out