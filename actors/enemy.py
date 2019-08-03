import pygame
from pygame import *
from actors.entity import Entity

class Enemy(Entity):
    def __init__(self, x, y, color, manager):
        Entity.__init__(self)
        self.walkingSpeed = 8
        self.xvel = 0
        self.yvel = 0
        self.onGround = False
        self.image = Surface((32,32))
        self.image.fill(Color(color))
        self.image.convert()
        self.rect = Rect(x, y, 32, 32)
        self.speed = 4
        self.xvel = self.speed
        self.isActive = True
        self.color = color
        self.manager = manager

    def update(self, platforms):
        if(not self.isActive):
            return
     
        if(not self.onGround):
            # only accelerate with gravity if in the air
            self.yvel += 0.3
            # max falling speed
            if self.yvel > 100: self.yvel = 100
        
        # increment in x direction
        self.rect.left += self.xvel

         # do x-axis collisions
        self.collide(self.xvel, 0, platforms)
        # increment in y direction
        self.rect.top += self.yvel
        # assuming we're in the air
        self.onGround = False;
        # do y-axis collisions
        self.collide(0, self.yvel, platforms)


    def collide(self, xvel, yvel, platforms):
        if(not self.isActive):
            return

        self.onGround = False

        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                if xvel > 0:
                    self.rect.right = p.rect.left
                    print("enemy collide right")
                    self.xvel = -self.speed;
                if xvel < 0:
                    self.rect.left = p.rect.right
                    print("enemy collide left")
                    self.xvel = self.speed;
                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.yvel = 0
                if yvel < 0:
                    self.rect.top = p.rect.bottom
                    self.yvel =0
    
    def die(self):
        self.isActive = False
        self.image.fill(Color("#000000"))
        self.manager.killEntity(self)

