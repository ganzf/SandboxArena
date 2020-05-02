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
            e = camera._parent
            pos = e.getPosition()
            mouse = pg.mouse.get_pos()
            mouse = Point(mouse[0], mouse[1])
            x1 = self.size[0] / 2
            y1 = self.size[1] / 2
            x2 = mouse.x
            y2 = mouse.y
            distance = mouse.distance(Point(x1, y1))
            if distance > 25:
                distance = 25
            vec = Point(x2 - x1, y2 - y1).normalize()
            camera.pos_modifier = {
                'vec': vec,
                'distance': distance,
            }
            #pg.draw.line(self.screen, store.get("palette").blue, [x1, y1], [x1 + vec.x * distance, y1 + vec.y * distance], 2)
    
            # world_scale = 20
            # x = x1 + vec.x * distance
            # y = y1 + vec.y * distance
            # pg.gfxdraw.filled_polygon(self.screen, [
            #     (x, y - world_scale / 2),
            #     (x + world_scale, y),
            #     (x, y + world_scale / 2),
            #     (x - world_scale, y)
            # ], store.get('palette').debug_color)

