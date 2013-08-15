"""
Keep a collection of geographic areas of interest for users,
and then match points back to the list of users interested in them.

TODO: make this efficient using a quad-tree of some sort to allow
for less comparisons than having to match against every possible shape.
"""
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
