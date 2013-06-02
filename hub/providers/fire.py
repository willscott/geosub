import time
import md5
import string
import requests
import json

url = "http://web1.seattle.gov/dpd/luib/RSSAllAreas.aspx"

class Fire:
  def pull(self):
    qry = "?$select= address,longitude,latitude,incident_number,type,report_location,datetime &$where=longitude is not null and latitude is not null and datetime is not null&$order=datetime DESC"
    r = requests.get(endpoint)
    data = json.loads(r.text)
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
