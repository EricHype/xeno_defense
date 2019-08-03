import pygame
from pygame import *
from actors.entity import Entity

class SquareFragment(Entity):
    millisecondsToLive = 800
    def __init__(self, x, y, size, color, direction, xvel, yvel, manager):
        Entity.__init__(self)
        self.yvel = yvel
        self.image = Surface((16,16))
        self.image.fill(Color(color))
        self.image.convert()
        self.rect = Rect(x, y, size, size)
        self.isActive = True
        self.isMoving = True
        self.manager = manager

        if(direction == "left"):
            self.xvel = -xvel
            self.xmomentum = -2
        if(direction == "right"):
            self.xmomentum = 2
            self.xvel = xvel

        self.startTime = pygame.time.get_ticks()
        self.endTime = self.startTime + SquareFragment.millisecondsToLive

    def update(self, platforms):
        if(self.isMoving):
            self.rect.left += self.xvel
            self.rect.top += self.yvel
            self.yvel += 0.3
            self.collide(platforms)
            self.xvel -= 1
        
        ticks = pygame.time.get_ticks()
        print("Ticks: {0}, EndTime: {1}".format(ticks, self.endTime))
        if(ticks >= self.endTime):
            self.die()
    
    def collide(self, platforms):
        if(not self.isActive):
            return
        
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                self.isMoving = False

    def die(self):
        self.isActive = False
        self.image.fill(Color("#000000"))
        self.manager.removeEntity(self)