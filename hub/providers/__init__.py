import os, sys, inspect
this_folder = os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0])
geopy_folder = os.path.join(this_folder, "geopy")
if geopy_folder not in sys.path:
  sys.path.insert(0, geopy_folder)

import landuse

providers = [(landuse.url, landuse.LandUse)]
