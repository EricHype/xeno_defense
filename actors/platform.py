from pygame import *
from actors.entity import Entity

class Platform(Entity):
    def __init__(self, x, y, image):
        Entity.__init__(self)
        self.image = image
        self.rect = Rect(x, y, 32, 32)
        self.isActive = True

    def update(self):
        pass