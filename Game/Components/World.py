from Engine.Components.AComponent import AComponent
from Game.Entities.Camera import Camera
from Engine.Datastructures import Rect

class World(AComponent):
    def __init__(self):
        AComponent.__init__(self, "World")
        self.size = Rect(25, 25) # Size in meters
        self.scale = 128 # How many pixels for 1 meter (size of the horizontal line inside a tile)
        self.ignore = False # Should whis world be skipped by the camera system ?
        self.camera = Camera()
        self.camera.name = "MainCamera"