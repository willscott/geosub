#!/usr/bin/env python

import sys
import requests
import json
import store
import datetime
import time
import md5
import random

class Daemon:
  """ Deals with feeds and pulls in new items. """

  def __init__(self, db):
    self.store = store.Store(db)

  def start(self):
    latest_time = ''
    while True:
      if latest_time is '':
        print "RETRIEVING ALL"
        endpoint = "http://data.seattle.gov/resource/kzjm-xkqj.json?$select= address,longitude,latitude,incident_number,type,report_location,datetime &$where=longitude is not null and latitude is not null and datetime is not null&$order=datetime DESC"
        r = requests.get(endpoint)
      else:
        print "RETRIEVING NEWER THAN " + latest_time
        endpoint = "http://data.seattle.gov/resource/kzjm-xkqj.json?$select= address,longitude,latitude,incident_number,type,report_location,datetime &$where=longitude is not null and latitude is not null and datetime is not null and datetime > '" + latest_time + "'&$order=datetime DESC"
        print endpoint
        r = requests.get(endpoint)

      data = json.loads(r.text)
      if (len(data) > 0):
        latest = data[0]
        latest_time = datetime.datetime.fromtimestamp(int(latest["datetime"])).strftime('%m-%d-%Y %H:%M:%S')

        for item in data:
          for k,v in item.items():
            print k, v
          id = md5.new(str(item["datetime"])+str(random.random())).hexdigest()
          category_id = 1
          self.store.addItem(id, 1, (item['latitude'], item['longitude']), item['datetime'], item['type'])
      else:
        print "No NEW DATA"
        time.sleep(60)


def main():
    app = Daemon("live")
    app.start()

if __name__ == "__main__":
    main()


