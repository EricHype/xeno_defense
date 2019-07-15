import pygame
from pygame import *
from actors.entity import Entity

class Player(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.jumpVelocity = 10
        self.bounceVelocity = 12
        self.runningSpeed = 12
        self.walkingSpeed = 8
        self.xvel = 0
        self.yvel = 0
        self.onGround = False
        self.image = Surface((32,32))
        self.image.fill(Color("#0000FF"))
        self.image.convert()
        self.rect = Rect(x, y, 32, 32)
        self.isActive = True

    def update(self, up, down, left, right, running, platforms, enemies):
        if up:
            # only jump if on the ground
            if self.onGround: self.yvel -= self.jumpVelocity
        if down:
            pass
        if running:
            self.xvel = self.runningSpeed
        if left:
            self.xvel = -self.walkingSpeed
        if right:
            self.xvel = self.walkingSpeed
        if not self.onGround:
            # only accelerate with gravity if in the air
            self.yvel += 0.3
            # max falling speed
            if self.yvel > 100: self.yvel = 100
        if not(left or right):
            self.xvel = 0
        # increment in x direction
        self.rect.left += self.xvel
        # do x-axis collisions
        self.collide(self.xvel, 0, platforms, enemies)
        # increment in y direction
        self.rect.top += self.yvel
        # assuming we're in the air
        self.onGround = False;
        # do y-axis collisions
        self.collide(0, self.yvel, platforms, enemies)

    def collide(self, xvel, yvel, platforms, enemies):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                if xvel > 0:
                    self.rect.right = p.rect.left
                if xvel < 0:
                    self.rect.left = p.rect.right
                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.yvel = 0
                if yvel < 0:
                    self.rect.top = p.rect.bottom
                    self.yvel =0
        
        for e in enemies:
            if not e.isActive:
                continue
            if pygame.sprite.collide_rect(self, e):
                if self.yvel > 0.01:
                    print("Self bottom: " + str(self.rect.bottom) + " enemy top: " + str(e.rect.top))
                    if self.rect.bottom <= (e.rect.top + 12):
                        self.yvel -= 15
                        e.die()
                else:
                    print("player dead") 