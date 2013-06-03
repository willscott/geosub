registry = {}

def addProvider(url, cls):
  registry[url] = cls;
  
def getProvider(url):
  if not url in registry:
    return None
  return registry[url]()

import providers
for provider in providers.providers:
  addProvider(provider[0], provider[1])

def ensureIds(store):
  for url in registry:
    res = store.db.execute("select id from categories where label=(?)", (url,)).fetchall()
    if res == None:
      store.db.execute("insert into categories (label) values ((?))", (url,))
      store.db.commit()
