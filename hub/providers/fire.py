import time
import md5
import string
import urllib2
import json

url = "http://data.seattle.gov/resource/kzjm-xkqj.json"

class Fire:
  def pull(self):
    qry = "?$select=%20address,longitude,latitude,incident_number,type,report_location,datetime%20&$where=longitude%20is%20not%20null%20and%20latitude%20is%20not%20null%20and%20datetime%20is%20not%20null&$order=datetime%20DESC"
    try:
      lines = urllib2.urlopen(url + qry).readlines()
      text = string.join(lines)
      data = json.loads(text)
      return map(self.prepare, data)
    except Exception as e:
      print e
      return []

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
