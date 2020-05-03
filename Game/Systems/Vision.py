import pygame as pg
import math
from Engine.Store import store
from Engine.Datastructures import Point
from Engine.Systems.ASystem import ASystem

class Vision(ASystem):
    def __init__(self):
        ASystem.__init__(self, "Vision")
        game = store.get("game")
        self.screen = game.screen
        self.size = game.screen_size

    def run(self, elapsed, events):
        cameras = store.components("Camera")
        for camera in cameras:
            mouse = pg.mouse.get_pos()
            mouse = Point(mouse[0], mouse[1])
            x1 = self.size[0] / 2
            y1 = self.size[1] / 2
            x2 = mouse.x
            y2 = mouse.y
            distance = mouse.distance(Point(x1, y1))
            # Distance in world scale (1 = world.scale)
            distance /= self.size[1] # In pct of screen height
            distance = math.log(distance + 1, 2) * 2
            if distance >= 1.5: # 1 and a half world scale
                distance = 1.5

            vec = Point(x2 - x1, y2 - y1).normalize()
            camera.pos_modifier = {
                'vec': vec,
                'distance': distance,
            }
            #pg.draw.line(self.screen, store.get("palette").blue, [x1, y1], [x1 + vec.x * distance, y1 + vec.y * distance], 2)