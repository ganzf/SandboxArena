from Game.Entities.GameObject import GameObject
from Game.Components.Camera import Camera as CameraComponent

class Camera(GameObject):
    def __init__(self):
        GameObject.__init__(self)
        self.attachComponent(CameraComponent())