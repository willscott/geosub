import time
import md5
import string
import urllib2
import json

url = "http://data.seattle.gov/resource/kzjm-xkqj.json"

class Fire:
  def pull(self):
    qry = "?$select= address,longitude,latitude,incident_number,type,report_location,datetime &$where=longitude is not null and latitude is not null and datetime is not null&$order=datetime DESC"
    text = urllib2.urlopen(url + qry).readlines()
    data = json.loads(text)
    return map(self.prepare, data)

  def prepare(self, item):
    def makeItem():
      #TODO: can we find a good link for at least big events?
      return {
        'time': time.time(),
        'lat': item["latitude"],
        'lon': item["longitude"],
        'data': {
          "addr": item["address"],
          "title": item["type"],
          "desc": item["incident_number"]
        }
      }
    id = md5.new(str(item["datetime"])+str(item["incident_number"])).hexdigest()
    
    return {'id': id , 'get':makeItem}
