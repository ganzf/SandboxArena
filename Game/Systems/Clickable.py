import pygame
import math
from Engine.Debug import debug
from Engine.Store import store
from Engine.Datastructures import Point

class Clickable(object):
    def __init__(self):
        self.name = "Clickable"
        self.controller = None
        self.camera = None
        self.game = store.get('game')

    def run(self, elapsed, events):
        if not self.controller:
            self.controller = list(filter(lambda x: x.name == 'PlayerController', store.get('systems')))[0]
            self.camera = list(filter(lambda x: x.name == 'Camera', store.get('systems')))[0]
        else:
            entities = store.get('entities')
            if entities:
                mouse = self.camera.to_world(self.controller.mouse_position)
                for entity in entities:
                    other_alive = entity.components.get("Alive")
                    if other_alive:
                        t = entity.components.get("Transform")
                        b = entity.components.get("Box")
                        clickable = entity.components.get("Clickable")

                        diff = [abs(mouse.x - t.x), abs(mouse.y - t.y)]
                        distance = math.sqrt(diff[0] * diff[0] + diff[1] * diff[1])

                        if distance <= b.w / 2 + 1 or distance <= b.h / 2 + 1:
                            clickable.hover = True
                            if self.controller.mouse_down == True:
                                clickable.pressed = True
                            if self.controller.mouse_clicked == True:
                                clickable.clicked = True
                                self.game.event_manager.emit(self.game.eventsFactory.build("clickOnEntity", { 'id': str(entity.id) }))
                            else:
                                clickable.clicked = False
                        else:
                            clickable.hover = False