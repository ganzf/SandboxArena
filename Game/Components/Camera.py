from Engine.Components.AComponent import AComponent
from Engine.Datastructures import Rect

class Camera(AComponent):
    def __init__(self):
        AComponent.__init__(self, "Camera")
        self.width = None
        self.height = None
        self.fps = None
        self.zoom = 1
        self.is_filming = False
        self.pos_modifier = None
        self.target = None