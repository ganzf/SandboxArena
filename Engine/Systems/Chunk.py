import pygame
import sys
import random
import math
from Engine.Systems.ASystem import ASystem
from Engine.Store import store
from Engine.Debug import debug
from Engine.Entity import Entity
from Engine.Datastructures import Point, Rect
from Game.Entities.GameObject import GameObject
from Engine.Components.Display import Display
from Engine.Components.Visible import Visible
from Game.Entities.World import World as WorldEntity
from Game.Entities.Chunk import Chunk as GO_Chunk

class Chunk(ASystem):
    def __init__(self):
        ASystem.__init__(self, "Chunk")
        self.screen = store.get("game").screen
        screen_size = store.get("game").screen_size
        self.screen_size = Rect(screen_size[0], screen_size[1])
        #self.list = []
        self.split = False
        self.visible_chunks = {}
        self.palette = store.get('palette')
        self.max_chunk_load_per_frame = 0
        self.chunk_load_delay = 0.1
        self.loaded_this_frame = 0
        self.available_chunk_load = 0.0
        self.mask = [
            # Distance 1
            (-1, -1), (0, -1), (1, -1),
            (-1, 0), (0, 0), (1, 0),
            (-1, 1), (0, 1), (1, 1),
            # Distance 2
            (0, 2), (0, -2),
            (2, 0), (-2, 0),
            (1, 2), (1, -2),
            (2, 1), (-2, 1),
            (2, 2), (2, -2),
            (-2, 2), (-2, -2)
        ]

    def split_world(self, world):
        # Building chunk list based on world info
        world_w = world.size.w
        world_h = world.size.h
        chunk_h = 8
        chunk_w = 8
        self.chunk_w = chunk_w
        self.chunk_h = chunk_h
        self.chunk_map = []
        nbr_chunks_x = int(world_w / chunk_w)
        nbr_chunks_y = int(world_h / chunk_h)
        for x in range(nbr_chunks_x):
            self.chunk_map.append([])
            for y in range(nbr_chunks_y):
                self.chunk_map[x].append(y)

        pos = Point()
        while pos.y < world_h:
            if pos.x >= world_w:
                pos.y += chunk_h
                pos.x = 0
                sys.stdout.write('\n')
            if pos.y >= world_h:
                break

            # For each chunk
            go = GO_Chunk()
            info = go.get("Chunk")
            t = go.get("Transform")
            go.setPosition(pos.x, pos.y, 0)
            t.scale.x = chunk_w
            t.scale.y = chunk_h
            t.scale.z = 3
            t.position.z = 0
            t.color = self.palette.pink
            info.position.x = int(math.floor(pos.x / chunk_w))
            info.position.y = int(math.floor(pos.y / chunk_h))
            
            self.chunk_map[info.position.x][info.position.y] = go
            #print("Created chunk {}.{} in {}.{}".format(pos.x, pos.y, info.position.x, info.position.y))
            sys.stdout.write("[X]")
            #self.list.append(go)

            pos.x += chunk_w
        self.split = True

    def update_chunk(self, GO_chunk):
        info = GO_chunk.get("Chunk")
        t = GO_chunk.get("Transform")
        t.color = self.palette.green
        #print("Loading chunk {}.{}".format(t.position.x, t.position.y))
        #if store.debug and t.screen:
            #pygame.gfxdraw.line(self.screen, int(self.screen_size.w / 2), int(self.screen_size.h / 2), int(t.screen.x), int(t.screen.y), self.palette.green)
        if len(info.children.items()) == 0 and not info.loaded and self.loaded_this_frame < self.max_chunk_load_per_frame:
            self.load_chunk(t, info)
        #for id, child in info.children.items():
            #child.attachComponent(Visible())
            # If the child is static
            # And it is next to another static child within the chunk (obvisouly)
            # and that other object is on the same Z level
            # And that other object has the same height in world size (scale.z or t.screen.z ?)
            # MERGE OBJECTS ! (And enjoy fps increase drastically)

    def pos_is_in_chunk(self, pos, chunk):
        return pos.x >= chunk.position.x and pos.y >= chunk.position.y and pos.x < chunk.position.x + chunk.scale.x and pos.y < chunk.position.y + chunk.scale.y

    def get_chunk_at(self, pos):
        if pos.x >= 0 and pos.y >= 0:
            if pos.x < len(self.chunk_map):
                if pos.y < len(self.chunk_map[pos.x]):
                    return self.chunk_map[pos.x][pos.y]

    def load_chunk(self, t, info):
        for chunkless in store.chunkless.get_list():
            chunkless_object = chunkless._parent
            t_c = chunkless_object.get("Transform")
            if self.pos_is_in_chunk(t_c.position, t):
                #print("Object not yet affected to chunk added to chunk: {} {}".format(chunkless_object.id, GO_chunk.id))
                chunkless_object.detach("Chunkless")
                
                info.children[chunkless_object.id] = chunkless_object
        info.loaded = True
        t.color = store.get('palette').blue
        self.loaded_this_frame += 1
        

    def unload_chunk(self, GO_chunk):
        t = GO_chunk.get("Transform")
        t.color = store.get('palette').green
        info = GO_chunk.get("Chunk")
        #print("Unloading chunk {}.{}".format(t.position.x, t.position.y))
        #for id, chunk_obj in info.children.items():
        #    chunk_obj.detach("Visible") # Not chunkless (we know where it is in the world) but is should no longer be parsed by the Camera system
        # Do not set info.loaded to false or it will computed by the camera again
        
    def run(self, elapsed, events):
        # Run once every 5 frames (no need to be frame perfect on chunk detection, because it happens offscreen)
        if store.get('frame') % 2:
            return
        for world in store.components("World"):             
            self.loaded_this_frame = 0
            if elapsed:
                self.available_chunk_load += elapsed
                if self.available_chunk_load >= self.chunk_load_delay:
                    self.available_chunk_load = 0.0
                    self.max_chunk_load_per_frame = 1
                else:
                    self.max_chunk_load_per_frame = 0
            if not self.split:
                self.split_world(world)
            else:
                # Save chunks visible last frame
                last_frame_visible = self.visible_chunks
                self.visible_chunks = {}

                cam = world.camera.get("Camera")
                cam_t = cam.target.get("Transform")
                
                cam_point = Point(int(cam_t.position.x / self.chunk_w), int(cam_t.position.y / self.chunk_h))
                main_chunk = self.get_chunk_at(cam_point)
                
                if main_chunk: # This should always be true, otherwise character is OOB
                    for diff in self.mask:
                        near_pos = Point(cam_point.x + diff[0], cam_point.y + diff[1])
                        near_chunk = self.get_chunk_at(near_pos)
                        if near_chunk:
                            near_chunk_info = near_chunk.getUnsafe("Chunk")
                            self.update_chunk(near_chunk)
                            self.visible_chunks[near_chunk.id] = near_chunk
                for id, chunk in self.visible_chunks.items():
                    # Was not present the last time we checked
                    if id not in last_frame_visible.keys():
                        print("Chunk {} is now visible".format(id))
                        chunk.attachComponent(Visible())
                for id, chunk in last_frame_visible.items():
                    if id not in self.visible_chunks.keys():
                        self.unload_chunk(chunk)
                        chunk.detach("Visible")
                        print("Chunk {} is no longer visible".format(id))
                            
            return