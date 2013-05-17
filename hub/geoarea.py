class PointRadiusGeoArea:
  def __init__(self, lat, long, r):
    self = GeoArea.__init__(self)
    self.lat = lat
    self.long = long
    self.r = r
  
  def toSql(self):
    return tuple("lat > (?) and lat < (?) and lon > (?) and lon < (?)", tuple(self.lat - self.r, self.lat + self.r, self.long - self.r, self.long + self.r))
