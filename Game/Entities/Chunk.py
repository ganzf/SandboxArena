# Area of the game loaded at the same time
from Game.Entities.GameObject import GameObject
from Engine.Components.Visible import Visible
from Engine.Components.Chunk import Chunk as ChunkComponent
from Engine.Store import store


class Chunk(GameObject):
    def __init__(self):
        GameObject.__init__(self)
        # Visible components are parsed by the camera system
        # Visible items can be hidden to not overload display (they are still parsed but nothing is shown on screen)
        self.attachComponent(ChunkComponent())