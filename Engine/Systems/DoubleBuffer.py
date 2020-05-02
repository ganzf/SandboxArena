from Engine.Systems.ASystem import ASystem
from Engine.Store import store, DoubleBuffer as DB

class DoubleBuffer(ASystem):
    def __init__(self):
        ASystem.__init__(self, "DoubleBuffer")

    def run(self, elapsed, events):
        store.transforms.update()
        store.visibles.update()
        store.chunkless.update()
        store.chunks.update()