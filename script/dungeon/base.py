from gamemap import Map


class Dungeon:

    def __init__(self):
        self.shoproom_chance = 0.05
        self.restroom_chance = 0.12
        self.treasureroom_chance = 0
        self.eventroom_chance = 0.22
        self.eliteroom_chance = 0.08
        self.map = None

    def generate_map(self):
        height = 15
        width = 7
        density = 6
        self.map = Map(height, width, density)
        self.map.generator(self)

    def update(self, dt):
        self.map.update(dt)
