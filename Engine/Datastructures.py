import math
from Engine.Colors import default_palette

class Point(object):
    def __init__(self, x=0, y=0, z=None):
        self.x = x
        self.y = y
        self.z = z

    def distance(self, other):
        diff_x = other.x - self.x
        diff_y = other.y - self.y
        return math.sqrt(diff_x**2 + diff_y**2)

    def normalize(self):
        distance = self.distance(Point(0, 0))
        if distance > 0:
            self.x /= distance
            self.y /= distance
        return self

    def distance_3d(self, other):
        if not self.z:
            return self.distance(other)
        diff_x = other.x - self.x
        diff_y = other.y - self.y
        diff_z = other.z - self.z
        return math.sqrt(diff_x**2 + diff_y**2 + diff_z**2)

    def __str__(self):
        return "Point({}, {}, {})".format(self.x, self.y, self.z)
    
class Rect(object):
    def __init__(self, w, h, color=default_palette.black):
        self.w = w
        self.h = h
        self.color = color