import pygame
import time
import random
from Engine.Store import store
from Engine.Debug import debug
from Engine.Entity import Entity
from Engine.Datastructures import Point, Rect
from Game.Components.UI import UI
import math

class Combat(object):
    def __init__(self):
        self.name = "Combat"
        self.game = store.get('game')
        self.camera = None
        self.world = None

    def run(self, elapsed, events):         
        life = store.components("Alive")
        for alive in life:
            t = alive._parent.getUnsafe('Transform')
            for other in life:
                # Entities of the same species will not attack one another
                if other._parent.id == alive._parent.id:
                    continue
                other_t = other._parent.getUnsafe("Transform")
                dist = t.position.distance(other_t.position) # This is in meters
                if dist < alive.vision_range:
                    mesh = alive._parent.get("Mesh")
                    if not alive.target and other.species != alive.species:
                        alive.target = other._parent.id
                        print("Added target {}".format(alive.target))
                    
                    if not alive._parent.get("Human"):
                        if dist <= alive.aggression_range and other.species != alive.species:
                            alive.destination = other_t.position

                        if t.screen and other_t.screen:
                            # target_line = alive._parent.get("UI")
                            # if not target_line:
                            #     target_line = alive._parent.attachComponent(UI())    
                                
                            # target_line.type = 'Bezier'
                            # target_line.x1 = t.screen.x
                            # target_line.y1 = t.screen.y
                            # target_line.x2 = other_t.screen.x
                            # target_line.y2 = other_t.screen.y
                            # target_line.style.color = store.get('palette').crimson

                            vec = Point(other_t.screen.x - t.screen.x, other_t.screen.y - t.screen.y)
                            vision_tolerance = 30 # This is in pixels

                            if vec.x > vision_tolerance and mesh:
                                if vec.y > vision_tolerance:
                                    mesh.animation = 'br'
                                elif vec.y < -vision_tolerance:
                                    mesh.animation = 'tr'
                                else:
                                    mesh.animation = 'r'
                            elif vec.x < -vision_tolerance and mesh:
                                if vec.y > vision_tolerance:
                                    mesh.animation = 'bl'
                                elif vec.y < -vision_tolerance:
                                    mesh.animation = 'tl'
                                else:
                                    mesh.animation = 'l'
                            elif mesh:
                                if vec.y > vision_tolerance:
                                    mesh.animation = 'b'
                                else:
                                    mesh.animation = 't'
                elif alive.target == other._parent.id:
                    alive.target = None
                    alive.destination = None