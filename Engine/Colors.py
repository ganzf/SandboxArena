import datetime
import random

class Palette(object):
    def __init__(self):
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.red = (239, 71, 11)
        self.green = (6, 214, 160)
        self.blue = (17, 138, 178)
        self.dark_blue = (7, 59, 76)
        self.dark = (25, 24, 10)
        self.ground = (161, 130, 118)
        self.dark_green = (40, 180, 40)
        self.grey = (226, 218, 219)
        self.background = (15, 20, 21)
        self.pink = (234, 99, 140)
        self.purple = (180, 101, 140)
        self.crimson = (240, 64, 64)

        self.debug_color = (255, 52, 179)

    def random(self):
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

default_palette = Palette()