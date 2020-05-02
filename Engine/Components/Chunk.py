from Engine.Components.AComponent import AComponent
from Engine.Datastructures import Point

class Chunk(AComponent):
    def __init__(self):
        AComponent.__init__(self, "Chunk")
        self.loaded = False
        self.position = Point()
        self.children = {}