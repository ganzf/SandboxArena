import pygame
import time
import random
from Engine.Store import store
from Engine.Debug import debug
from Engine.Entity import Entity
from Engine.Datastructures import Point, Rect
import math

class Combat(object):
    def __init__(self):
        self.name = "Combat"
        self.game = store.get('game')
        self.camera = None
        self.world = None

    def run(self, elapsed, events):
        if not self.camera:
            self.camera = list(filter(lambda x: x.name == 'Camera', store.get('systems')))[0]
        if not self.world:
            self.world = list(filter(lambda x: x.name == 'World', store.get('systems')))[0]
        
        entities = store.get('entities')
        if entities:
            for entity in entities:
                t = entity.components.get('Transform')
                box = entity.components.get('Box')
                alive = entity.components.get("Alive")
                skills = entity.components.get("Skills")

                if t and box and alive:
                    point = self.camera.to_screen(t)

                    if skills:
                        if skills.active:
                            results = list(filter(lambda x: x.name == skills.active, skills.known_skills))
                            if results:
                                skill = results[0]
                                if skill.charge < skill.cast_time:
                                    skill.charge += elapsed
                                if skill:
                                    pygame.draw.rect(self.game.screen, self.game.palette.white, [point.x - 15, point.y - 20, 30, 5], 0)
                                    pygame.draw.rect(self.game.screen, self.game.palette.red, [point.x - 15, point.y - 20, (skill.charge / skill.cast_time) * 30, 5], 0)
                                    # print("Charging skill {}".format(skill.name))


                    if alive.target:
                        t_target = alive.target.components.get("Transform")
                        if t_target:
                            p_target = self.camera.to_screen(t_target)
                            pygame.draw.line(self.game.screen, self.game.palette.red, [point.x, point.y], [p_target.x, p_target.y], 2)

                    #pygame.draw.ellipse(self.game.screen, self.game.palette.black, [point.x - alive.vision_range, point.y - alive.vision_range, alive.vision_range * 2, alive.vision_range * 2], 1)
                    #pygame.draw.ellipse(self.game.screen, self.game.palette.red, [point.x - alive.attack_range, point.y - alive.attack_range, alive.attack_range * 2, alive.attack_range * 2], 2)

                    if alive.current_hp != alive.hp:
                        pygame.draw.rect(self.game.screen, self.game.palette.red, [point.x - 5, point.y - 5, 40, 5])
                        if alive.current_hp > 0:
                            size_of_healthbar = (alive.current_hp / alive.hp) * 40
                            pygame.draw.rect(self.game.screen, self.game.palette.green, [point.x - 5, point.y - 5, (alive.current_hp / alive.hp) * 40, 5])
                        

                    for other_entity in entities:
                        if str(other_entity.id) == str(entity.id):
                            continue
                        other_alive = other_entity.components.get('Alive')
                        if other_alive:
                            t_other = other_entity.components.get('Transform')
                            diff = [abs(t_other.x - t.x), abs(t_other.y - t.y)]
                            distance = math.sqrt(diff[0] * diff[0] + diff[1] * diff[1])
                            # Insert ai scripting or gambits system here ?
                            if distance < alive.vision_range and distance > alive.attack_range:
                                other_point = self.camera.to_screen(t_other)
                                if not entity.components.get("Human"):
                                    alive.destination = Point(t_other.x, t_other.y)
                                    #pygame.draw.line(self.game.screen, self.game.palette.red, [point.x, point.y], [other_point.x, other_point.y], 1)
                                else:
                                    pass
                                    #pygame.draw.line(self.game.screen, self.game.palette.blue, [point.x, point.y], [other_point.x, other_point.y], 1)
                                    # alive.targets[other_entity.id] = other_entity
                        
                            if skills:
                                if skills.active:
                                    results = list(filter(lambda s: s.name == skills.active, skills.known_skills))
                                    if results:
                                        skill = results[0]
                                        if skill:
                                            pygame.draw.ellipse(self.game.screen, self.game.palette.red, [point.x - skill.range, point.y - skill.range, skill.range * 2, skill.range * 2], 2)
                                        if skill.charge < skill.cast_time:
                                            pass
                                        elif distance < skill.range: 
                                            print("{} Casting spell {}".format(time.time(), skill.name))
                                            other_alive.current_hp -= skill.damage
                                            if other_alive.current_hp <= 0:
                                                self.game.remove_entity_by_id(other_entity.id)
                                                alive.target = None
                                                skills.active = None
                                            skill.charge = 0
                                            if not skill.auto_reload:
                                                skills.active = None