import pygame
import pygame.gfxdraw
from shapely.geometry import Point as ShapelyPoint
from shapely.geometry.polygon import Polygon
from Engine.Systems.ASystem import ASystem
from Engine.Store import store
from Engine.Debug import debug
from Engine.Entity import Entity
from Engine.Datastructures import Point, Rect
import math

DEBUG_IMAGE = pygame.image.load("./Game/assets/debug.png")

class Camera(ASystem):
    def __init__(self):
        ASystem.__init__(self, "Camera")
        game = store.get("game")
        self.screen_width = game.screen_size[0]
        self.screen_height = game.screen_size[1]
        self.screen = game.screen
        self.palette = game.palette
        self.draw = pygame.gfxdraw
    
    # def to_world(self, point_on_screen):
    #     return Point(point_on_screen.x - self.width / 2 + self.position.x, point_on_screen.y - self.height / 2 + self.position.y)

    # def to_screen(self, point_in_world):
    #     return Point(point_in_world.x + self.width / 2 - self.position.x, point_in_world.y + self.height / 2 - self.position.y)

    def line(self, x1, y1, x2, y2, color=None):
        c = color or self.palette.white
        pygame.gfxdraw.line(self.screen, int(x1), int(y1), int(x2), int(y2), c)

    def update_transform(self, t, pos, world, camera_info):
        world_scale = world.scale
        half_world_scale = world_scale / 2
        #store.begin_time("CameraPerEntityTime")
        entity = t._parent
        color = self.palette.debug_color
        offset = camera_info.offset
        # Only required for chunks, not for all objects
        # Therefore, it is a chunk loading optimization
        # if pos.distance(t.position) <= drawing_distance:
        if t.position.z < pos.z: # Object is in front of the camera
            # Apply iso projection
            #tile.setPosition((tmp.x - tmp.y) / 2, (tmp.x + tmp.y) / 4,  0)
            
            
            # Iso projection to find top corner of object on screen
            x = (t.position.x - t.position.y) / 2
            y = (t.position.x + t.position.y) / 4

            # Adapt to camera position
            # Where is the camera in an iso proj:
            iso_cam_x = (pos.x - pos.y) + offset.x
            iso_cam_y = (pos.x + pos.y) / 2 + offset.y

            x += (x - iso_cam_x)
            y += (y - iso_cam_y)

            y -= t.position.z
            # Scale to world
            x *= world_scale / 2
            y *= world_scale / 2

            # Adapt to camera z level
            
            
            # Center on screen
            x += camera_info.width / 2
            y += camera_info.height / 2

            # Scale to world and camera position
            #x = x * world_scale + offset_x
            #y = y * world_scale + offset_y - half_world_scale * t.position.z

            # (x, y) is the top of a tile on screen
            # This polygon is the bottom of a box
            
            
            if x < 0 or x > camera_info.width or y < 0 or y > camera_info.height:
                t.screen = None
            else:
                #if store.debug:
                #    self.line(x, y, camera_info.width / 2, camera_info.height / 2)
                t.screen = Point(x, y)
                #pygame.gfxdraw.aacircle(self.screen, int(x), int(y), 10, t.color)
            #pygame.gfxdraw.rectangle(self.screen, [x, y, world_scale, world_scale], store.get('palette').white)

            #store.end_time("CameraPerEntityTime")
            return t.screen != None

    def render_transform(self, t, world):
        if not t.screen:
            return
        if not store.debug and t._parent.get("Mesh"):
            return
        world_scale = world.scale
        half_world_scale = world_scale / 2
        box_width = half_world_scale * t.scale.x
        store.begin_time("CameraPerEntityDraw")
        # Top corner of tile
        x = t.screen.x
        y = t.screen.y
        pygame.gfxdraw.polygon(self.screen, [
            (x, y),
            (x + box_width, y + box_width / 2),
            (x, y + box_width),
            (x - box_width, y + box_width / 2)
        ], t.color)
        
        box_height = half_world_scale * t.scale.z
        top = y - box_height
        top_color = t.color

        # X face
        pygame.gfxdraw.polygon(self.screen, [
            (x, y + box_width),
            (x, y - box_height),
            (x + box_width, y + box_width / 2 - box_height),
            (x + box_width, y + box_width / 2)
        ], t.color)

        # Y Face
        pygame.gfxdraw.polygon(self.screen, [
            (x, y + box_width),
            (x, y - box_height),
            (x - box_width, y + box_width / 2 - box_height),
            (x - box_width, y + box_width / 2)
        ], t.color)



        pygame.gfxdraw.polygon(self.screen, [
            (x, y - box_height),
            (x + box_width, y + box_width / 2 - box_height),
            (x, y + box_width - box_height),
            (x - box_width, y + box_width / 2 - box_height)
        ], top_color)

        store.end_time("CameraPerEntityDraw")


    def film(self, camera_info):
        camera = camera_info._parent
        humans = store.components("Human")
        human = None
        if humans:
            human = humans[0]
        

        palette = self.palette
        drawing_distance = math.sqrt((camera_info.width/2)**2 + (camera_info.height/2)**2)
        
        # To uncomment
        # visibles = store.visibles.get_list()

        worlds = store.components("World")
        # There should ideally be only one world at a time. A world is like a level
        for world in worlds:
            if world.ignore:
                continue
            world_scale = world.scale
            half_world_scale = world_scale / 2
            
            target_pos = camera_info.target.getPosition()
            pos = Point(target_pos.x, target_pos.y, target_pos.z + 1)
            
            screen_center = Point(int(camera_info.width / 2), int(camera_info.height / 2))
            if store.debug:
                pygame.gfxdraw.line(self.screen, screen_center.x - 10, screen_center.y, screen_center.x + 10, screen_center.y, palette.purple)
                pygame.gfxdraw.line(self.screen, screen_center.x, screen_center.y + 10, screen_center.x, screen_center.y - 10, palette.purple)

            # mouse = pygame.mouse.get_pos()
            # mouse = ShapelyPoint(mouse[0], mouse[1])

            # Vision system
            offset = Point(0, 0)
            if camera_info.pos_modifier:
                mod = camera_info.pos_modifier
                vec = mod.get('vec')
                dist = mod.get('distance')
                if vec and dist:
                    offset.x = vec.x * dist
                    offset.y = vec.y * dist / 2
                    camera_info.offset = offset
            
            # Adapt to target z position
            offset.y -= (pos.z)

            visibles = store.visibles.get_list()
            layers = {}
            to_draw = []
            for visible in visibles:
                chunk = visible._parent.get("Chunk")
                if chunk:
                    chunk_t = visible._parent.getUnsafe("Transform")
                    self.update_transform(chunk_t, pos, world, camera_info)
                    if store.debug:
                        self.render_transform(chunk_t, world)
                    transforms = list(map(lambda chunk_child: chunk_child.getUnsafe("Transform"), chunk.children.values()))
                    for t in transforms:
                        render = self.update_transform(t, pos, world, camera_info)
                        if render:
                            if t._parent.get("Mesh"):
                                if not layers.get(t.position.z):
                                    layers[t.position.z] = []
                                layers[t.position.z].append(t)
                                to_draw.append(t)
                            self.render_transform(t, world)
                else:
                    t = visible._parent.get("Transform")
                    if t and self.update_transform(t, pos, world, camera_info):
                        if not layers.get(t.position.z):
                            layers[t.position.z] = []
                        self.render_transform(t, world)
            
            for alive in store.components("Alive"):
                t = alive._parent.getUnsafe("Transform")
                render = self.update_transform(t, pos, world, camera_info)
                mesh = alive._parent.get("Mesh")
                if render and mesh:
                    if not layers.get(t.position.z):
                        layers[t.position.z] = []
                    layers[t.position.z].append(t)
                    to_draw.append(t)
            
            ef = store.get('game').eventsFactory
            em = store.get("game").event_manager
            to_draw = sorted(to_draw, key=lambda t: t.position.x + t.scale.x + t.position.y + t.scale.y + t.position.z - t.scale.z)
            em.emit(ef.build('drawMeshRequest', { 'transforms': to_draw }))
            # for z, to_draw in sorted(layers.items(), key=lambda z: z[0]):           
            #     to_draw = sorted(to_draw, key=lambda t: t.screen.y)
            #     em.emit(ef.build("drawMeshRequest", { 'transforms': to_draw } ))


    def run(self, elapsed, events=None):
        cameras = store.components("Camera")
        for camera in cameras:
            if camera.is_filming:
                self.film(camera)
        return