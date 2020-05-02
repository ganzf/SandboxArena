import uuid

class AComponent(object):
    def __init__(self, name):
        self.name = name
        self.id = str(uuid.uuid4())
        self._entity = None
        self._parent = None

    def remove(self):
        if self._parent and self.name in self._parent.components.keys():
            print("Removed component {} from {}".format(self.name, self._parent.id))
            del self._parent.components[self.name]