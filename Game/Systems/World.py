import pygame
import random
from Engine.Systems.ASystem import ASystem
from Engine.Store import store
from Engine.Debug import debug
from Engine.Entity import Entity
from Engine.Datastructures import Point, Rect
from Game.Entities.GameObject import GameObject
from Engine.Components.Display import Display
from Engine.Components.Chunkless import Chunkless
from Game.Entities.World import World as WorldEntity
import math

class World(ASystem):
    def __init__(self):
        ASystem.__init__(self, "World")
        world = WorldEntity()
        self.seed(world)

    def seed(self, world):
        tmp = Point()
        world_info = world.get("World")
        size = world_info.size
        factor = size.w
        scale = world_info.scale
        palette = store.get("palette")
        tiles = 0

        player = GameObject()
        #player.setPosition(world_info.size.w / 2, world_info.size.h / 2)
        player.setPosition(0.5, 0.5) # Middle of square 0,0
        t = player.get("Transform")
        t.color = palette.purple
        a = player.attach("Alive")
        player.attach("Human")
        a.speed = 3
        t.scale.x = 1
        t.scale.y = 1
        t.position.z = 1
        #d = player.attachComponent(Display("./Game/assets/player.png"))
        #d.show_cell = False
        #d.reference_point = 0.97
        
        camera = world_info.camera
        #camera.setPosition(t.position.x, t.position.y, 10) # Camera is 10 meters above ground
        #print("Camera position: {}".format(camera.getPosition()))
        camera_info = camera.get("Camera")
        camera_info.target = player
        camera_info.is_filming = True
        game = store.get("game")
        camera_info.width = game.screen_size[0]
        camera_info.height = game.screen_size[1]
        camera_info.fps = 60
        camera_info.zoom = 1

        tmp.x = 0
        tmp.y = 0
        self.tiles = []
        print("Seeding world {}-{} of scale {}".format(size.w, size.h, scale))
        while tmp.y < size.h:
            if tmp.x >= size.w:
                tmp.y += 1
                tmp.x = 0
            if tmp.y >= size.h:
                break
            #print("Seeding tile {}.{}".format(tmp.x, tmp.y))
            
            tile = GameObject()
            #tile.setPosition((tmp.x - tmp.y) / 2, (tmp.x + tmp.y) / 4,  0)

            tile.setPosition(tmp.x, tmp.y, 0)
            #print(tile.getPosition())

            # This object is not yet added to a chunk
            # Having a component for chunkless objects makes it easy to iterate over
            tile.attachComponent(Chunkless())

            t = tile.get("Transform")
            self.tiles.append(t)
            t.scale.x = 1
            t.scale.y = 1
            t.scale.z = 0
            #d = tile.attachComponent(Display("./Game/assets/tilde.png"))
            #tiles += 1
            tmp.x += 1

        return 
        tmp.x = 0
        tmp.y = 0
        while tmp.y < size.h:
            if tmp.x >= size.w:
                tmp.y += 1
                tmp.x = 0
            if tmp.y >= size.h:
                break
            print("Seeding tile {}.{}".format(tmp.x, tmp.y))
            dice = random.randint(0, 100)
            if dice >= 92 and tmp.x - size.w / 2 != 0 and tmp.y - size.h / 2 != 0:
                tile = GameObject()
                tile.setPosition(tmp.x - tmp.y + 1/2, (tmp.x + tmp.y) / 2 - 1/3,  0)
                t = tile.get("Transform")
                t.static = True
                t.scale.x = 1
                t.scale.y = 0.1
                t.position.z = 1
                d = tile.attachComponent(Display("./Game/assets/tree_low.png"))
                d.show_cell = False
                d.reference_point = 0.99
                # d.scale.x = 3
                # d.scale.y = 3
            elif dice >= 93:
                monster = GameObject()
                monster.setPosition(tmp.x - tmp.y + 1/2, (tmp.x + tmp.y) / 2 - 1/3, 1)
                d = monster.attachComponent(Display("./Game/assets/monster.png"))
                d.show_cell = True
                d.reference_point = 0.97
            tmp.x += 1
        print("Tiles: {}".format(tiles))
        
                
    def run(self, elapsed, events=None):
        i = 0
        for tile in self.tiles:
            #tile.position.z = math.sin(store.total_time + i)
            i += 1
        return 

        if not self.camera:
            self.camera = list(filter(lambda x: x.name == 'Camera', store.get('systems')))[0]
        if self.old_color != self.target_color:
            r = self.old_color[0]
            g = self.old_color[1]
            b = self.old_color[2]
            r_diff = self.target_color[0] - r
            g_diff = self.target_color[1] - g
            b_diff = self.target_color[2] - b
            # Fade to right color over a second
            color = (int(r + math.ceil(r_diff / self.game.fps)), int(g + math.ceil(g_diff / self.game.fps)), int(b + math.ceil(b_diff / self.game.fps)))
            """             debug({
                'old': self.old_color,
                'next': self.target_color,
                'color': color,
                'diffs': {
                    'r': r_diff,
                    'g': g_diff,
                    'b': b_diff,
                }
            }) """
            self.old_color = self.game.background_color
            self.game.background_color = color
        else:
            self.old_color = self.target_color
            self.target_color = self.game.palette.background()

        debug_box = Point(0, 0)
        debug_box = self.camera.to_screen(debug_box)
        pygame.draw.rect(self.game.screen, self.game.palette.random(), [debug_box.x, debug_box.y, 1, 1], 0)

    