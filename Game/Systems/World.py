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

    def get_at(self, x, y):
        if y < len(self.map):
            if x < len(self.map[y]):
                return self.map[y][x]
        return None

    def seed_correct(self, world, depth = 0):
        if depth >= 10:
            return
        world_info = world.get("World")
        size = world_info.size
        tmp = Point()
        tmp.x = 0
        tmp.y = 0
        
        prev_is_top = 10
        while tmp.y < size.h:
            if tmp.x >= size.w:
                tmp.y += 1
                tmp.x = 0
            if tmp.y >= size.h:
                break

            t = self.get_at(tmp.x, tmp.y)

            if t.position.z == 0:
                near = [
                    self.get_at(tmp.x - 1, tmp.y),
                    self.get_at(tmp.x + 1, tmp.y),
                    self.get_at(tmp.x, tmp.y - 1),
                    self.get_at(tmp.x, tmp.y + 1),
                ]
                is_single_land = True
                for n in near:
                    if n and n.position.z != 0:
                        is_single_land = False
                if is_single_land:
                    t.position.z < 0

            if t.position.z < 0:
                near = [
                    self.get_at(tmp.x - 1, tmp.y),
                    self.get_at(tmp.x + 1, tmp.y),
                    self.get_at(tmp.x, tmp.y - 1),
                    self.get_at(tmp.x, tmp.y + 1),
                ]
                is_single_water = True
                is_deep_water = True
                for n in near:
                    if n and n.position.z < 0:
                        if not is_single_water:
                            n.position.z = -0.7
                            n._parent.get("Mesh").spritesheet = "water.png"
                        is_single_water = False
                    if n and n.position.z >= 0:
                        is_deep_water = False
                if is_single_water:
                    t.position.z = 0
                    t._parent.get("Mesh").spritesheet = "grass.png"
                else:
                    if is_deep_water:
                        t._parent.get("Mesh").spritesheet = "deep_water.png"
                        t.position.z -= 0.1

            tmp.x += 1
        return self.seed_correct(world, depth + 1)

    def seed(self, world):
        tmp = Point()
        world_info = world.get("World")
        size = world_info.size
        factor = size.w
        scale = world_info.scale
        palette = store.get("palette")
        tiles = 0

        player = GameObject()
        player.setPosition(world_info.size.w / 2, world_info.size.h / 2, 1)
        #player.setPosition(0, 0, 1) # Middle of square 0,0
        t = player.get("Transform")
        a = player.attach("Alive")
        a.species = "SmartAndFast"
        player.attach("Human")
        player.attachComponent(Visible())
        print("Player id {}".format(player.id))
        a.speed = 3.5
        t.scale.x = 0.5
        t.scale.y = 0.5
        t.scale.z = 1
        t.position.z = 1
        t.color = palette.purple
        
        mesh = player.attachComponent(Mesh())
        mesh.spritesheet = 'player_spritesheet.png'
        mesh.framesize.w = 128
        mesh.framesize.h = 128
        # Requires explaination (This is the offset of the sprite within the transform box)
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
        self.map = [[]]
        prev_is_top = 10
        while tmp.y < size.h:
            if tmp.x >= size.w:
                tmp.y += 1
                tmp.x = 0
                self.map.append([]) # A new row
            if tmp.y >= size.h:
                break
            #print("Seeding tile {}.{}".format(tmp.x, tmp.y))
            
            tile = GameObject()
            #tile.setPosition((tmp.x - tmp.y) / 2, (tmp.x + tmp.y) / 4,  0)
            mesh = tile.attachComponent(Mesh())
            mesh.spritesheet = 'grass.png'
            mesh.framesize.w = 128
            mesh.framesize.h = 126
            mesh.frames['static_0'] = Point(0, 0)
            mesh.frame = 'static_0'
            mesh.base_frame_offset = 1.5
            
            tile.setPosition(tmp.x, tmp.y, 0)
            #print(tile.getPosition())

            # This object is not yet added to a chunk
            # Having a component for chunkless objects makes it easy to iterate over
            tile.attachComponent(Chunkless())

            if random.randint(0, 100) < 1:
                monster = GameObject()
                mesh = monster.attachComponent(Mesh())
                mesh.spritesheet = 'player_spritesheet.png'
                mesh.framesize.w = 128
                mesh.framesize.h = 128
                # Requires explaination
                mesh.base_frame_offset = 1.32

                def load_line(name, start_x, end_x, y):
                    for index in range(end_x - start_x):
                        n = '{}_{}'.format(name, index)
                        mesh.frames[n] = Point(start_x + index, y)
                
                x = 3
                load_line('b', x, 12, 0)
                load_line('br', x, 12, 1)
                load_line('r', x, 12, 2)
                load_line('tr', x, 12, 3)
                load_line('t', x, 12, 4)
                load_line('tl', x, 12, 5)
                load_line('l', x, 12, 6)
                load_line('bl', x, 12, 7)
                anim = random.randint(0, 4)
                anims = ['b', 'br', 'r', 'bl', 'l']
                mesh.animation = anims[anim]

                monster.setPosition(tmp.x, tmp.y, 1)
                a = monster.attach("Alive")
                monster.attachComponent(Visible())
                a.speed = 2

            t = tile.get("Transform")
            t.scale.x = 1
            t.scale.y = 1
            t.scale.z = 1
            t.color = palette.white
            t.position.z = random.randint(-25, 130)
            if t.position.z < 0:
                t.position.z = -1
            elif t.position.z > 120:
                t.position.z = 0.6
                mesh.spritesheet = 'rock.png'
                ground = GameObject()
                #tile.setPosition((tmp.x - tmp.y) / 2, (tmp.x + tmp.y) / 4,  0)
                ground_mesh = ground.attachComponent(Mesh())
                ground_mesh.spritesheet = 'grass.png'
                ground_mesh.framesize.w = 128
                ground_mesh.framesize.h = 126
                ground_mesh.frames['static_0'] = Point(0, 0)
                ground_mesh.frame = 'static_0'
                ground_mesh.base_frame_offset = 1.5
                
                ground.setPosition(tmp.x, tmp.y, 0)
                #print(tile.getPosition())

                # This object is not yet added to a chunk
                # Having a component for chunkless objects makes it easy to iterate over
                ground.attachComponent(Chunkless())
            else:
                t.position.z = 0

            if t.position.z < 0:
                mesh.spritesheet = 'water.png'
            t.color = palette.green
            #d = tile.attachComponent(Display("./Game/assets/tilde.png"))
            #tiles += 1
            self.map[tmp.y].append(t)
            tmp.x += 1
        self.seed_correct(world)
                
    def run(self, elapsed, events=None):
        for water in self.waters:
            water.position.z = -(math.sin(store.total_time / 6 + water.position.x) + 1) / 2 - 0.2