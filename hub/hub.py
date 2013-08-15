providerCategories = {}

def addProvider(url, cls):
  providerCategories[url] = cls;
  
def getProvider(url):
  if not url in providerCategories:
    print "Could not find provider ", url
    return None
  return providerCategories[url]()

import providers
for provider in providers.providers:
  addProvider(provider[0], provider[1])

publisherCategories = {}

def addPublisher(url, cls):
  publisherCategories[url] = cls;
  
def getPublisher(url):
  if not url in publisherCategories:
    print "Could not find publisher ", url
    return None
  return publisherCategories[url]()

import publishers
for publisher in publishers.publishers:
  addPublisher(publisher[0], publisher[1])

def ensureIds(store):
  for url in providerCategories:
    res = store.db.execute("select id from categories where label=(?)", (url,)).fetchall()
    if res == None or len(res) == 0:
      print "Adding category ", url
      store.db.execute("insert into categories (label) values ((?))", (url,))
      store.db.commit()
