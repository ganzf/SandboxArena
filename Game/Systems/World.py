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
from Engine.Components.Visible import Visible
from Engine.Components.Mesh import Mesh
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
        player.setPosition(0, 0, 1) # Middle of square 0,0
        t = player.get("Transform")
        a = player.attach("Alive")
        player.attach("Human")
        player.attachComponent(Visible())
        print("Player id {}".format(player.id))
        a.speed = 2
        t.scale.x = 0.5
        t.scale.y = 0.5
        t.scale.z = 1
        t.color = palette.purple
        
        mesh = player.attachComponent(Mesh())
        mesh.spritesheet = 'player_spritesheet.png'
        mesh.framesize.w = 128
        mesh.framesize.h = 128
        # Requires explaination
        mesh.base_frame_offset = 1.32

        def load_line(name, start_x, end_x, y):
            for index in range(end_x - start_x):
                n = '{}_{}'.format(name, index)
                mesh.frames[n] = Point(start_x + index, y)
                print("Loaded {}".format(n))
        
        x = 3
        load_line('b', x, 12, 0)
        load_line('br', x, 12, 1)
        load_line('r', x, 12, 2)
        load_line('tr', x, 12, 3)
        load_line('t', x, 12, 4)
        load_line('tl', x, 12, 5)
        load_line('l', x, 12, 6)
        load_line('bl', x, 12, 7)
        mesh.animation = 'b'



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
        self.waters = []
        
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
            t.scale.z = 1
            t.color = palette.white
            t.position.z = 0
            t.color = palette.green
            if random.randint(0, 100) > 75:
                self.waters.append(t)
                t.color = palette.dark_blue
                t.position.z = -0.2
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
                t.position.z = random.randint(0, 2)
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
        pass