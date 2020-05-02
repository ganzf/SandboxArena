from Engine.Components.AComponent import AComponent

class Visible(AComponent):
    def __init__(self, hide=False):
        AComponent.__init__(self, "Visible")
        self.hide = hide