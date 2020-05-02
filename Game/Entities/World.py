from Game.Entities.GameObject import GameObject
from Game.Components.World import World as WorldComponent

class World(GameObject):
    def __init__(self):
        GameObject.__init__(self)
        self.attachComponent(WorldComponent())