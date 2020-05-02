import pygame
import math
from Engine.Debug import debug
from Engine.Store import store
from Engine.Datastructures import Point

class Quadstate(object):
    GOING_DOWN = 0
    DOWN = 1
    GOING_UP = 2
    UP = 3

    def __init__(self, key):
        self.key = key
        self.state = Quadstate.UP

    def is_up(self):
        return self.state == Quadstate.UP

    def is_down(self):
        return self.state == Quadstate.DOWN

    def is_pressed(self):
        return self.state == Quadstate.GOING_DOWN

    def is_released(self):
        return self.state == Quadstate.GOING_UP

    def press(self):
        self.state = Quadstate.GOING_DOWN
    
    def release(self):
        self.state = Quadstate.GOING_UP

class Keyboard(object):
    def __init__(self):
        self.up_key = Quadstate(pygame.K_w)
        self.down_key = Quadstate(pygame.K_s)
        self.left_key = Quadstate(pygame.K_a)
        self.right_key = Quadstate(pygame.K_d)
        self.space_bar = Quadstate(pygame.K_SPACE)
        self.cancel_key = Quadstate(pygame.K_c)
        self.l_shift = Quadstate(pygame.K_LSHIFT)
        self.key_1 = Quadstate(pygame.K_1)
        self.key_2 = Quadstate(pygame.K_2)
        self.key_3 = Quadstate(pygame.K_3)
        self.keys = [
            self.up_key,
            self.down_key,
            self.left_key,
            self.right_key,
            self.l_shift,
            self.space_bar,
            self.key_1, 
            self.key_2,
            self.key_3,
            self.cancel_key,
        ]


class PlayerController(object):
    def __init__(self):
        self.name = "PlayerController"
        self.game = store.get('game')
        self.player = None
        self.destination = None
        self.speed = 0.5
        self.mouse_position = None
        self.mouse_clicked = 0
        self.mouse_color = self.game.palette.black
        self.mouse_down = False
        self.keyboard = Keyboard()

    def run(self, elapsed, events):
        if self.mouse_clicked > 0:
            self.mouse_clicked -= 1

        if store.get('systems') and not self.player:
            world = list(filter(lambda x: x.name == 'World', store.get('systems')))[0]
            camera = list(filter(lambda x: x.name == 'Camera', store.get('systems')))[0]
            humans = store.components("Human")
            if humans:
                human = humans[0]
                human = human._parent
                if human:
                    self.player = human

            self.camera = camera
            self.world = world

        if self.player:        
            t = self.player.components.get('Transform')
            for key in self.keyboard.keys:
                if key.state == Quadstate.GOING_UP:
                    key.state = Quadstate.UP
                if key.state == Quadstate.GOING_DOWN:
                    key.state = Quadstate.DOWN

            for event in events:
                if event.name == 'keyDown':
                    key = event.data.get('key')
                    for keyboard_key in self.keyboard.keys:
                        if key == keyboard_key.key:
                            if keyboard_key.is_up():
                                keyboard_key.press()
                            elif keyboard_key.state == Quadstate.GOING_DOWN:
                                keyboard_key.state = Quadstate.DOWN

                if event.name == 'keyUp':
                    key = event.data.get('key')
                    for keyboard_key in self.keyboard.keys:
                        if key == keyboard_key.key:
                            if keyboard_key.is_down() or keyboard_key.state == Quadstate.GOING_DOWN:
                                keyboard_key.release()
                            elif keyboard_key.state == Quadstate.GOING_UP:
                                keyboard_key.state = Quadstate.UP

                if event.name == 'click':
                    self.mouse_down = False
                    self.mouse_clicked = 1

                if event.name == 'mouseDown':
                    self.mouse_down = True
                    self.mouse_clicked = 0

                """ if event.name == 'click':
                    data = event.data.get('position')
                    point = self.camera.to_world(Point(data[0], data[1]))
                    player_alive = self.player.components.get("Alive")
                    if not player_alive.destination:
                        player_alive.destination = Point()
                    player_alive.destination.x = point.x
                    player_alive.destination.y = point.y
                    if player_alive.destination.x < -self.world.size.w / 2:
                        player_alive.destination.x = -self.world.size.w / 2
                    if player_alive.destination.x > self.world.size.w / 2:
                        player_alive.destination.x = self.world.size.w / 2
                    if player_alive.destination.y < -self.world.size.h / 2:
                        player_alive.destination.y = -self.world.size.h / 2
                    if player_alive.destination.y > self.world.size.h / 2:
                        player_alive.destination.y = self.world.size.h / 2 """

                if event.name == 'mouseMove':
                    data = event.data.get('position')
                    point = Point(data[0], data[1])
                    # point = self.camera.to_world(Point(data[0], data[1]))
                    self.mouse_position = point

            if self.keyboard.space_bar.is_pressed():
                self.game.time_multiplier = 0.1
            if self.keyboard.space_bar.is_released():
                self.game.time_multiplier = 1
                
            player_alive = self.player.components.get("Alive")
            if player_alive:
                if self.keyboard.l_shift.is_down() and not player_alive.stamina_exhausted:
                    player_alive.sprint = True
                else:
                    player_alive.sprint = False

            if self.keyboard.cancel_key.is_released():
                if player_alive:
                    if player_alive.target:
                        player_alive.target = None

            if self.keyboard.right_key.state == Quadstate.DOWN or self.keyboard.right_key.state == Quadstate.GOING_DOWN:
                if not player_alive.destination:
                    player_alive.destination = Point(t.position.x, t.position.y)
                player_alive.destination.x += 1
                player_alive.destination.y -= 1
                
            if self.keyboard.left_key.state == Quadstate.DOWN or self.keyboard.left_key.state == Quadstate.GOING_DOWN:
                if not player_alive.destination:
                    player_alive.destination = Point(t.position.x, t.position.y)
                player_alive.destination.x -= 1
                player_alive.destination.y += 1

            if self.keyboard.up_key.state == Quadstate.DOWN or self.keyboard.up_key.state == Quadstate.GOING_DOWN:
                if not player_alive.destination:
                    player_alive.destination = Point(t.position.x, t.position.y)
                player_alive.destination.x -= 1
                player_alive.destination.y -= 1

            if self.keyboard.down_key.state == Quadstate.DOWN or self.keyboard.down_key.state == Quadstate.GOING_DOWN:
                if not player_alive.destination:
                    player_alive.destination = Point(t.position.x, t.position.y)
                player_alive.destination.x += 1
                player_alive.destination.y += 1

            skills = self.player.components.get("Skills")
            if skills:
                if self.keyboard.key_1.is_pressed():
                    if len(skills.equipped) > 0:
                        if skills.selected == skills.equipped[0]:
                            skills.selected = None
                        else:
                            skills.selected = skills.equipped[0]
                if self.keyboard.key_2.is_pressed():
                    if len(skills.equipped) > 1:
                        if skills.selected == skills.equipped[1]:
                            skills.selected = None
                        else:
                            skills.selected = skills.equipped[1]
                if self.keyboard.key_3.is_pressed():
                    if len(skills.equipped) > 2:
                        if skills.selected == skills.equipped[2]:
                            skills.selected = None
                        else:
                            skills.selected = skills.equipped[2]
            
            
            def color_for_key(key):
                if key.state == Quadstate.UP:
                    return self.game.palette.white
                if key.state == Quadstate.DOWN:
                    return self.game.palette.red
                if key.state == Quadstate.GOING_DOWN:
                    return self.game.palette.green
                if key.state == Quadstate.GOING_UP:
                    return self.game.palette.blue

        entities = store.get('entities')
        if entities:
            for entity in entities:
                alive = entity.components.get('Alive')
                if alive and alive.destination:
                    speed_multiplier = 1.75 if alive.sprint else 1
                    t = entity.components.get("Transform")
                    if t:
                        if alive.destination.x != t.position.x:
                            diff = alive.destination.x - t.position.x
                            if diff > 0:
                                diff = 1 * alive.speed
                            else:
                                diff = -1 * alive.speed
                            t.position.x += diff * elapsed
                        if alive.destination.y != t.position.y:
                            diff = alive.destination.y - t.position.y
                            if diff > 0:
                                diff = 1 * alive.speed
                            else:
                                diff = -1 * alive.speed
                            t.position.y += diff * elapsed 

                        worlds = store.components("World")
                        world = worlds[0]

                        if t.position.x < 0:
                            t.position.x = 0
                        if t.position.y < 0:
                            t.position.y = 0
                        if t.position.x >= world.size.w:
                            t.position.x = world.size.w - 0.01
                        if t.position.y >= world.size.h:
                            t.position.y = world.size.h - 0.01

                        #point = self.camera.to_screen(alive.destination)
                        #pygame.draw.ellipse(self.game.screen, self.game.palette.black, [point.x - self.game.scale / 2, point.y - self.game.scale / 2, self.game.scale, self.game.scale], 2)

                        if abs(alive.destination.x - t.position.x) <= alive.attack_range and abs(alive.destination.y - t.position.y) <= alive.attack_range:
                            alive.destination = None

        player_alive = self.player.components.get("Alive")
        if player_alive and player_alive.destination:
            pass
            #point = self.camera.to_screen(player_alive.destination)
            #pygame.draw.ellipse(self.game.screen, self.game.palette.black, [point.x - self.game.scale / 2, point.y - self.game.scale / 2, self.game.scale, self.game.scale], 2)
        

