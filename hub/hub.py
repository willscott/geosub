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