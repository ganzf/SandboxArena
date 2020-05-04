class Alive(object):
    def __init__(self):
        self.name = "Alive"
        self.species = "Smart"
        self.hp = 100
        self.current_hp = self.hp
        self.max_stamina = 100
        self.stamina = self.max_stamina
        self.stamina_exhausted = False
        self.vision_range = 4 # Meters
        self.speed = 1
        self.aggression_range = 2.5
        self.attack_range = 1 # meters
        self.attack_speed = 1
        self.strength = 5
        self.wisdom = 10
        self.agility = 4
        self.target = None
        self.destination = None
        self.sprint = False
