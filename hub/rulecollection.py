class RuleCollection:
  def __init__(self):
    self.map = []

  def add(self, geoArea, user):
    self.map.push((geoArea.toShape(), user))

  def match(self, point):
    users = []
    for (region, user) in self.map:
      if region.contains(point):
        users.push(user)
    return users
