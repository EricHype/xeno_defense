import pygame
from pygame import *
from actors.entity import Entity

class SquareFragment(Entity):
    def __init__(self, x, y, size, color, direction, xvel, yvel):
        Entity.__init__(self)
        self.yvel = yvel
        self.image = Surface((16,16))
        self.image.fill(Color(color))
        self.image.convert()
        self.rect = Rect(x, y, size, size)
        self.isActive = True
        self.isMoving = True

        if(direction == "left"):
            self.xvel = -xvel
            self.xmomentum = -2
        if(direction == "right"):
            self.xmomentum = 2
            self.xvel = xvel

    def update(self, platforms):
        if(not self.isActive):
            return

        if(not self.isMoving):
            return
        self.rect.left += self.xvel
        self.rect.top += self.yvel
        self.yvel += 0.3
        self.collide(platforms)
    
    def collide(self, platforms):
        if(not self.isActive):
            return
        
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                self.isMoving = False