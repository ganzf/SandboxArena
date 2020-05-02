class Alive(object):
    def __init__(self):
        self.name = "Alive"
        self.hp = 100
        self.current_hp = self.hp
        self.max_stamina = 100
        self.stamina = self.max_stamina
        self.stamina_exhausted = False
        self.vision_range = 100
        self.speed = 1
        self.attack_range = 38
        self.attack_speed = 1
        self.strength = 5
        self.wisdom = 10
        self.agility = 4
        self.target = None
        self.destination = None
        self.sprint = False
