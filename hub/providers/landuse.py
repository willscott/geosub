import feedparser
import re
import time
import md5
import string
from geopy import geocoders
import urllib2

url = "http://web1.seattle.gov/dpd/luib/RSSAllAreas.aspx"

class LandUse:
  def __init__(self):
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
    addr = re.sub('\(Project[^()]*\)', '', item.description)
    place = self.coder.geocode(addr + " Seattle, WA")
    out['lat'] = place[1][0]
    out['lon'] = place[1][1]
    lines = urllib2.urlopen(item.link).readlines()
    page = string.join(map(string.strip, lines), '')
    desc = re.sub('</td.*','',re.sub('.*trProjectDescription"><[^>]*>','',y))
    out['data'] = {
      "addr": addr.lower().strip(),
      "title": item.title,
      "desc": desc,
      "link": item.link
    }
    
    return out

