import pygame
import math
from Engine.Debug import debug
from Engine.Events import Observer
from Engine.Store import store
from Engine.Datastructures import Point

class Spellbar(object):
    def __init__(self):
        self.name = "Spellbar"
        self.game = store.get('game')
        self.player = None

        observer = Observer("playerClickOnEntity")
        observer.observe("clickOnEntity")
        observer.on_call(self.onPlayerClick)
        self.game.event_manager.add_observer(observer)

    def onPlayerClick(self, event):
        print("Clicked on " + event.data.get("id"))
        entities = store.get('entities')
        target = None
        if entities:
            for entity in entities:
                if str(entity.id) == event.data.get("id"):
                    target = entity
        
        if target:
            self.cast(target)

    def cast(self, target):
        skills = self.player.components.get("Skills")
        spellName = skills.selected
        if spellName not in skills.equipped:
            print("Casting spell is not equiped: {}".format(spellName))
            return
        skills.active = spellName
        skills.selected = None
        alive = self.player.components.get("Alive")
        alive.target = target


    def run(self, elapsed, events):
        if store.get('systems') and not self.player:
            world = list(filter(lambda x: x.name == 'World', store.get('systems')))[0]
            camera = list(filter(lambda x: x.name == 'Camera', store.get('systems')))[0]
            controller = list(filter(lambda x: x.name == 'PlayerController', store.get('systems')))[0]
            self.player = world.player
            self.camera = camera
            self.world = world
            self.controller = controller

        if self.player:
            skills = self.player.components.get("Skills")
            selected_skill = None
            t = self.player.components.get("Transform")
            point = self.camera.to_screen(t)
            for x in range(skills.max_skills_equipped):
                skill = skills.equipped[x] if x < len(skills.equipped) else None
                color = self.game.palette.white
                if skill and skill == skills.selected:
                    color = self.game.palette.red
                    selected_skill = skill
                if not skill:
                    color = self.game.palette.grey
                pygame.draw.rect(self.game.screen, color, [ 25 + x * 25, 850, 24, 25 ], 0)

            if selected_skill:
                self.controller.mouse_color = self.game.palette.red
                skill = list(filter(lambda x: x.name == selected_skill, skills.known_skills))[0]
                pygame.draw.ellipse(self.game.screen, self.game.palette.red, [point.x - skill.range, point.y - skill.range, skill.range * 2, skill.range * 2], 2)
            else:
                self.controller.mouse_color = self.game.palette.black
            
