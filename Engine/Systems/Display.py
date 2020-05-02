import pygame as pg
import pygame.gfxdraw
import math
import time
from Engine.Systems.ASystem import ASystem
from Engine.Datastructures import Point, Rect
from Engine.Store import store

debug_image = None
files = {
    
}
surfaces = {

}

class Sprite(pg.sprite.Sprite):
    def __init__(self, file, scale=None):
        super().__init__()
        if not file:
            image = debug_image
        else:
            image = files.get(file)
            if not image:
                try:
                    image = pg.image.load(file).convert_alpha()
                    files[file] = image
                except Exception as e:
                    print(e)
                    image = debug_image
        if scale:
            mem = surfaces.get('{}.{}.{}'.format(file, int(scale.x), int(scale.y)))
            res = Point()
            if not mem:
                size = image.get_rect().size
                res.x = int(size[0] * 1 / scale.x)
                res.y = int(size[1] * 1 / scale.y)
            self.image = mem if mem else pg.transform.scale(image, (res.x, res.y))
            if not mem:
                surfaces['{}.{}.{}'.format(file, int(scale.x), int(scale.y))] = self.image
            self._scale = scale
        else:
            mem = surfaces.get(file)
            self.image = mem if mem else image
            if not mem:
                surfaces[file] = image
            self._scale = Point(1, 1)
        self.rect = self.image.get_rect(center=(0, 0))
        

class Display(ASystem):
    def __init__(self):
        ASystem.__init__(self, "Display")
        global debug_image
        debug_image = pg.image.load("./Game/assets/debug_tile.png").convert_alpha()
        self.screen = store.get('game').screen
        # Keep sprites in memory here
        self.sprites = {}
        self.groups = {
            'default': pg.sprite.Group()
        }

    def get_sort_info(self, transform):
        e = transform._parent
        display = e.get("Display")
        y = transform.position.y
        if display and display.visible: 
            y = display.center[1] + display.size.h * display.reference_point
        return (transform.position.z, y)

    def run(self, elapsed, events):
        
        blit = 0
        
        displayable = store.components("Display")
        transforms = []
        for d in displayable:
            if d.visible:
                t = d._parent.get("Transform")
                if t:
                    transforms.append(t)
        # transforms = store.components("Transform")
        

        
        transforms.sort(key = lambda x: self.get_sort_info(x))
        
        for t in transforms:
            
            # e = store.entity(t._entity, fast=True)
            e = t._parent
            
            
            display = e.get("Display")
            
            if not display:
                continue
            id = display._entity
            store.begin_time("get sprite")
            s = self.sprites.get(id)
            store.end_time('get sprite')
            if not s:
                store.begin_time("create sprite")
                s = Sprite(display.file, display.scale)
                display.size = Rect(s.rect.size[0], s.rect.size[1])
                store.end_time("create sprite")
                #print("New sprite of size {}.{}".format(display.size.w, display.size.h))
                self.sprites[id] = s
                # No need to add to group for now
                #self.groups['default'].add(s)
            else:
                # Scale changed ! Wont happen much
                if s._scale.x != display.scale.x or s._scale.y != display.scale.y:
                    print("Rescaling sprite {}".format(id))
                    store.begin_time("rescaling sprite")
                    s = Sprite(display.file, scale=display.scale)
                    store.end_time("rescaling sprite")
                    display.size = Rect(s.rect.size[0], s.rect.size[1])
                    print("Rescaled sprite to size {}.{}".format(display.size.w, display.size.h))
                    self.sprites[id] = s
                if display.visible:
                    s.rect.center = display.center
                    center = display.center
                    size = display.size
                    if display.type == 0:
                        top_left = (center[0] - display.camera_correction, center[1] - display.camera_correction)
                    else:
                        top_left = (center[0] - display.camera_correction, center[1] - display.camera_correction)
                    store.begin_time("blit")
                    blit += 1
                    # Ground hitbox
                    if display.show_cell:
                        #pygame.gfxdraw.line(self.screen, int(top_left[0]), int(top_left[1] + size.h), int(top_left[0] + size.w), int(top_left[1] + size.h), store.get('palette').red)
                        pygame.gfxdraw.line(self.screen, int(top_left[0]), int(top_left[1] + size.h * display.reference_point), int(top_left[0] + size.w), int(top_left[1] + size.h * display.reference_point), store.get('palette').green)
                        pygame.gfxdraw.aaellipse(self.screen, int(top_left[0] + 1/2 * size.w), int(top_left[1] + size.h - size.h / 6), int(size.w / 3), int(size.h / 6), store.get('palette').red)
                        #pygame.gfxdraw.rectangle(self.screen, [top_left[0] + 1/3 * size.w, top_left[1] + size.h - display.camera_correction * 2, 1/3*size.w, display.camera_correction * 2], store.get('palette').debug_color)
                    self.screen.blit(s.image, top_left)
                    store.end_time("blit")
        return
