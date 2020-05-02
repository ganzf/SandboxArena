import uuid
from Engine.Store import store
from Engine.Components import Transform, Box, Alive, Human
from Engine.Components.Clickable import Clickable
from Game.Components.Skills import Skills

factory = {
    'Transform': Transform,
    'Box': Box,
    'Alive': Alive,
    'Human': Human,
    'Skills': Skills,
    'Clickable': Clickable
}
    

fast_components = [
    'Transform',
    'Visible',
    'Chunkless'
]

class Entity(object):
    def __init__(self, name=None):
        self.id = str(uuid.uuid4())
        self.name = name
        self.components = {}

        # Quick Access to certain components
        self._display = None
        self._transform = None

        store.add_to('entities', self)

    def attach(self, componentName):
        if componentName in factory.keys():
            if componentName not in self.components.keys():
                c = factory[componentName]()
                if componentName == 'Display':
                    self._display = c
                self.components[componentName] = c
                self.components[componentName]._entity = self.id
                self.components[componentName]._parent = self
                if componentName == 'Transform':
                    store.transforms.add(c)
                if componentName == 'Visible':
                    store.visibles.add(c)
                if componentName == 'Chunkless':
                    store.chunkless.add(c)
                if componentName == 'Chunk':
                    store.chunks.add(c)
                return c
            else:
                raise Exception("Component {} already exists in {}".format(componentName, self.id))
        raise Exception("Could not create and attach component " + componentName + " to " + self.name)

    def attachComponent(self, component):
        componentName = component.name
        if not componentName:
            raise Exception("Component has no name")

        if componentName in self.components.keys():
            return self.components[componentName]
        if componentName == 'Display':
            self._display = component
        if componentName == 'Transform':
            store.transforms.add(component)
        if componentName == 'Visible':
            store.visibles.add(component)
        if componentName == 'Chunkless':
            store.chunkless.add(component)
        if componentName == 'Chunk':
            store.chunks.add(component)
        self.components[componentName] = component
        component._entity = self.id
        component._parent = self
        return component

    def detach(self, componentName):
        if componentName in self.components.keys():
            c = self.components[componentName]
            if componentName == 'Transform':
                store.transforms.remove(c)
            if componentName == 'Visible':
                print("A visible shouldb be removed from double buffer of store")
                store.visibles.remove(c)
            if componentName == 'Chunkless':
                store.chunkless.remove(c)
            # This one should never occur, chunks always exist... no ?
            if componentName == 'Chunk':
                store.chunks.remove(c)