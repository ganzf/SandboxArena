class Event(object):
    def __init__(self, name, description, data={}):
        self.name = name
        self.description = description
        self.data = data

    def duplicate(self, data):
        return Event(self.name, self.description, data or self.data)

class EventsFactory(object):
    def __init__(self):
        self.knownEvents = [
            Event("startFrame", "Event emitted at the beginning of a new frame"),
            Event("endFrame", "Event emitted before updating the frame"),
            Event('quitRequested', 'Event thrown when quit is requested'),
            Event("keyDown", "When a key is pressed"),
            Event("keyUp", 'When a key is released'),
            Event("mouseDown", "When the mouse button is pressed"),
            Event("click", 'When the mouse button is released'),
            Event("mouseMove", "When the mouse moves"),
            Event("clickOnEntity", "When an entity is clicked by the player")
        ]

    def build(self, name, data=None):
        for event in self.knownEvents:
            if event.name == name:
                return event.duplicate(data)
    

class Observer(object):
    def __init__(self, name):
        self.name = name
        self.observed = {}
    
    def observe(self, name):
        self.observed[name] = True

    def forget(self, name):
        self.observed[name] = False

    def on_call(self, callback):
        self.callback = callback

    def cares_about(self, name):
        return name in self.observed.keys()

    def call(self, event):
        if self.callback:
            self.callback(event)

class EventManager(object):
    def __init__(self):
        self.observers = []

    def emit(self, event):
        for observer in self.observers:
            if observer.cares_about(event.name):
                observer.call(event)

    def add_observer(self, observer):
        self.observers.append(observer)
