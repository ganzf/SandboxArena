from Engine.Components.AComponent import AComponent
from Engine.Datastructures import Point

class Transform(AComponent):
    def __init__(self):
        AComponent.__init__(self, "Transform")
        self.position = Point(0, 0, 0) # Z index in meters
        self.rotation = Point(0, 0)
        self.scale = Point(1, 1, 1)
        self.color = (0, 0, 0)
        self.screen = None # Position of center of object on screen
        self.static = False
