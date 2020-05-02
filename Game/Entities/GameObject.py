from Engine.Entity import Entity

class GameObject(Entity):
    def __init__(self, name=None):
        Entity.__init__(self)
        self.attach("Transform")
        self.name = name

    def __str__(self):
        return self.id

    def setPosition(self, x=0, y=0, z=0, point=None):
        t = self.get("Transform")
        if not t:
            return False
        if point:
            t.position.x = point.x
            t.position.y = point.y
            t.position.z = point.z
        else:
            t.position.x = x
            t.position.y = y
            t.position.z = z
        return True

    def getPosition(self):
        t = self.get("Transform")
        if not t:
            return None
        return t.position

    def getUnsafe(self, componentName):
        return self.components[componentName]

    def get(self, componentName):
        return self.components.get(componentName)
                