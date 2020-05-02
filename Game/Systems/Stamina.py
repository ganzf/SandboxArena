import pygame
import math
from Engine.Debug import debug
from Engine.Store import store
from Engine.Datastructures import Point

class Stamina(object):
    def __init__(self):
        self.name = "Stamina"
        self.game = store.get('game')
        self.player = None

    def run(self, elapsed, events):
        if store.get('systems') and not self.player:
            world = list(filter(lambda x: x.name == 'World', store.get('systems')))[0]
            camera = list(filter(lambda x: x.name == 'Camera', store.get('systems')))[0]
            self.player = world.player
            self.camera = camera
            self.world = world

        if self.player:
            alive = self.player.components.get("Alive")
            hp = alive.current_hp
            max_hp = alive.hp
            pygame.draw.rect(self.game.screen, self.game.palette.red, [ 50, 5, max_hp * 2, 10], 0)
            pygame.draw.rect(self.game.screen, self.game.palette.dark_green, [ 50, 5, hp * 2, 10], 0)

            stamina = alive.stamina
            max = alive.max_stamina
            pygame.draw.rect(self.game.screen, self.game.palette.red, [ 50, 20, max * 2, 10], 0)
            pygame.draw.rect(self.game.screen, self.game.palette.dark_green, [ 50, 20, stamina * 2, 10], 0)
        
            if alive.sprint and stamina <= 0:
                alive.sprint = False
                alive.stamina_exhausted = True

            if alive.stamina < max and not alive.sprint:
                alive.stamina += 15 * elapsed
                if alive.stamina_exhausted and alive.stamina > 30:
                    alive.stamina_exhausted = False

            if alive.stamina >= 0 and alive.sprint:
                alive.stamina -= 40 * elapsed
            