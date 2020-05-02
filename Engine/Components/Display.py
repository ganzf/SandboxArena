from Engine.Datastructures import Point, Rect
from Engine.Components.AComponent import AComponent

TILE = 0
SPRITE = 1
CUBE = 2
LEFT_FACE = 3
RIGHT_FACE = 4

class Display(AComponent):
    def __init__(self, file=None):
        AComponent.__init__(self, "Display")
        self.visible = False
        self.size = Rect(0, 0)
        self.file = file
        self.type = TILE
        self.center = Point()
        self.color = (255, 255, 255)
        self.scale = Point(1, 1)
        self.invisible = False
        self.camera_correction = 1
        self.show_cell = False
        self.reference_point = 0 # Vertical offset to reach 1m above ground in "game world"