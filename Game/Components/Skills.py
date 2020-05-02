class Weapon(object):
    def __init__(self):
        self.name = "Weapon"
        self.cooldown = 0
        self.cast_time = 5
        self.auto_reload = False
        self.range = 250
        self.damage = 50
        self.charge = 0

    def __str__(self):
        return self.name

class Autofight(object):
    def __init__(self):
        self.name = "Autofight"
        self.cooldown = 0
        self.cast_time = 3
        self.auto_reload = True
        self.range = 100
        self.damage = 20
        self.charge = 0

    def __str__(self):
        return self.name

class Skills(object):
    def __init__(self):
        self.max_skills_equipped = 3
        self.active = None
        self.known_skills = [
            Weapon(),
            Autofight(),
        ]
        self.equipped = [
            "Weapon",
            "Autofight",
        ]
        self.selected = None
        