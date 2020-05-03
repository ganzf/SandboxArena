import pygame
import random
import time
import argparse
from Engine.Events import EventsFactory, EventManager, Event, Observer
from Engine.Colors import Palette
from Engine.Store import store
from Engine.Systems.Display import Display
from Engine.Systems.Chunk import Chunk
from Engine.Systems.Mesh import Mesh
from Engine.Systems.DoubleBuffer import DoubleBuffer
from Engine.Systems.Animation2D import Animation2D
from Game.Systems.Camera import Camera
from Game.Systems.World import World
from Game.Systems.PlayerController import PlayerController
from Game.Systems.Combat import Combat 
from Game.Systems.Stamina import Stamina
from Game.Systems.Spellbar import Spellbar
from Game.Systems.Clickable import Clickable
from Game.Systems.Vision import Vision

class Arena(object):
    def __init__(self):
        pygame.init()
        store.add('game', self)
        
        parser = argparse.ArgumentParser(description='SandboxArena is the shit')

        # REQUIRED ARGS
        # !REQUIRED ARGS

        # OPTIONAL ARGS
        parser.add_argument('-d', '--debug', help='Allow debug features', required=False, action="store_true")
        # !OPTIONAL ARGS

        args = parser.parse_args()
        debug = args.debug
        if debug:
            store.debug = True
            store.timers_allowed = True        
        else:
            store.debug = False
            store.timers_allowed = False

        self.palette = Palette()
        store.add("palette", self.palette)

        self.carryOn = True
        self.clock = pygame.time.Clock()
        self.screen_size = (1600, 900)
        self.screen = pygame.display.set_mode(self.screen_size, pygame.DOUBLEBUF)
        self.event_manager = EventManager()
        self.eventsFactory = EventsFactory()
        
        self.last_system_call = None
        self.fps = 60
        self.sleep_duration = None
        self.scale = 30
        self.time_multiplier = 1 # Reducing it will enable slow motion, etc

        pygame.mouse.set_visible(False)

        store.add("entities", [])
        store.add("systems", [
            World(),
            Chunk(),
            Camera(),
            #Display(),
            #Clickable(),
            PlayerController(),
            Vision(),
            #Combat(),
            #Stamina(),
            #Spellbar(),
            Animation2D(),
            Mesh(),
            DoubleBuffer(),
        ])

        quitObserver = Observer("quitObserver")
        quitObserver.observe("quitRequested")
        quitObserver.on_call(self.onQuitRequested)
        self.event_manager.add_observer(quitObserver)

        newFrameObserver = Observer("startFrame")
        newFrameObserver.observe("startFrame")
        newFrameObserver.on_call(self.clearScreen)
        self.event_manager.add_observer(newFrameObserver)

        endFrameObserver = Observer("endFrame")
        endFrameObserver.observe("endFrame")
        endFrameObserver.on_call(self.updateScreen)
        self.event_manager.add_observer(endFrameObserver)

        pygame.display.set_caption("Sandbox Arena Prototype")

    def onQuitRequested(self, event):
        self.carryOn = False

    def clearScreen(self, event):
        # Should be done by the camera system when event begin frame is received
        self.screen.fill(self.palette.background)

    def updateScreen(self, event):
        pygame.display.flip()
        self.clock.tick(self.fps)

    def poll_events(self):
        list = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                list.append(self.eventsFactory.build("quitRequested"))
            
            if event.type == pygame.KEYDOWN:
                list.append(self.eventsFactory.build("keyDown", { 'key': event.key }))

            if event.type == pygame.KEYUP:
                list.append(self.eventsFactory.build("keyUp", { 'key': event.key }))

            if event.type == pygame.MOUSEBUTTONDOWN:
                list.append(self.eventsFactory.build("mouseDown", { 'position': event.pos }))

            if event.type == pygame.MOUSEBUTTONUP:
                list.append(self.eventsFactory.build("click", { 'position': event.pos }))

            if event.type == pygame.MOUSEMOTION:
                list.append(self.eventsFactory.build("mouseMove", { 'position': event.pos, 'rel': event.rel }))
        return list

    def remove_entity_by_id(self, id):
        entities = store.get('entities')
        entities = list(filter(lambda entity: str(entity.id) != str(id), entities))
        store.add('entities', entities)

    def loop(self):
        elapsed = None
        second = 0.0
        frames = 0
        self.avg = []
        self.time_multiplier = 1
        time_in_system = {}
        max_time = 15
        frame_idx = 0
        while self.carryOn and max_time >= 0:
            frame_idx += 1
            store.add("frame", frame_idx)
            frames += 1
            if self.last_system_call:
                elapsed = (time.time() - self.last_system_call) * self.time_multiplier
                second += elapsed / self.time_multiplier
                store.total_time += elapsed
                if second >= 1:
                    self.avg.append(frames)
                    print("FPS: {}".format(frames))
                    second = 0.0
                    
                    max_time -= 1
                    frames = 0
            # A new frame is starting
            self.event_manager.emit(self.eventsFactory.build("startFrame"))

            # Get engine events
            events = self.poll_events()

            # Emit all events
            for event in events:
                self.event_manager.emit(event)

            self.last_system_call = time.time()
            # Run all systems
            if store.get('systems'):
                for system in store.get('systems'):
                    before = time.time()
                    system.run(elapsed, events)
                    after = time.time()
                    if not time_in_system.get(system.name):
                        time_in_system[system.name] = []
                    time_in_system[system.name].append(after - before)
                    
            # The frame is ready to update
            #TODO: Fix event manager freeze
            # self.event_manager.emit(self.eventsFactory.build("endFrame"))
            store.begin_time("Flip")
            pygame.display.flip()
            store.end_time("Flip")
            store.begin_time("Sleep")
            self.clock.tick(self.fps)
            store.end_time("Sleep")
        s = 0
        for f in self.avg:
            s += f
        avg = s / len(self.avg)
        print("Average fps: {}".format(avg))
        print("Total time: {}".format(store.total_time))
        for k, v in time_in_system.items():
            s = 0
            for t in v:
                s += t            
            avg = s / len(v)
            avg = round(avg, 5)
            pct = (s / store.total_time) * 100
            pct = round(pct, 2)
            print("Average time in sytem '{}' is\t\t{} (total: {} {}%)".format(k, avg, round(s, 4), pct))
        
        if store and store.times:
            for k, v in store.times['avg'].items():
                pct = (store.times['sum'][k] / store.total_time) * 100
                pct = round(pct, 2)
                print("Average of timer '{}' is\t\t{} (total {} {}%)".format(k, round(v, 5), round(store.times['sum'][k], 4), pct))