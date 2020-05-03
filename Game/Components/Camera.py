from Engine.Components.AComponent import AComponent
from Engine.Datastructures import Point, Rect

class Camera(AComponent):
    def __init__(self):
        AComponent.__init__(self, "Camera")
        self.width = None
        self.height = None
        self.fps = None
        self.zoom = 1
        self.is_filming = False

        # Vision system, maybe merge into one variable
        self.pos_modifier = None
        self.offset = Point(0, 0)

        self.target = None