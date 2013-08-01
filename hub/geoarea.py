from lib.shapely.geometry import Point, MultiPoint

class PointRadiusGeoArea:
  def __init__(self, lat, long, r):
    self = GeoArea.__init__(self)
    self.lat = lat
    self.long = long
    self.r = r

  def toShape(self):
    p = Point(self.lat, self.long)
    return p.buffer(self.r)
  
  def toSql(self):
    return tuple("lat > (?) and lat < (?) and lon > (?) and lon < (?)", tuple(self.lat - self.r, self.lat + self.r, self.long - self.r, self.long + self.r))

class RectGeoArea:
  def __init__(self, lat_min, lat_max, long_min, long_max):
    self = GeoArea.__init__(self)
    self.lat_min = lat_min
    self.lat_max = lat_max
    self.long_min = long_min
    self.long_max = long_max

  def toSql(self):
    return tuple("lat > (?) and lat < (?) and lon > (?) and lon < (?)", tuple(self.lat_min, self.lat_max, self.long_min, self.long_max))

  def toShape(self):
    box = MultiPoint([(self.lat_min, self.long_min), (self.lat_min, self.long_max), (self.lat_max, self.long_max), (self.lat_max, self.long_min)])
    return box.convex_hull
