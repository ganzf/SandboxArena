from Engine.Store import store

class ASystem(object):
    def __init__(self, name):
        self.name = name
        systems = store.get('systems')
        if systems and self.name not in systems.keys():
            store.add_to('systems', self)

    def run(self, elapsedTime, frameEvents):
        raise Exception("Not Implemented")