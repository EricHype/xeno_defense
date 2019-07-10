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
        # increment in x direction
        self.rect.left += self.xvel
        # do x-axis collisions
        self.collide(self.xvel, 0, platforms)

    def collide(self, xvel, yvel, platforms):
        if(not self.isActive):
            return

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
    
    def die(self):
        self.isActive = False
        self.image.fill(Color("#000000"))
        self.manager.killEntity(self)
        # entities.add(SquareFragment(self.rect.left, self.rect.top, 16, ENEMY_COLOR, "left", 8, 6))
        # entities.add(SquareFragment(self.rect.left+16, self.rect.top, 16, ENEMY_COLOR, "right", 8, 3))
        # entities.add(SquareFragment(self.rect.left, self.rect.top+16, 16, ENEMY_COLOR, "left", 2, 6))
        # entities.add(SquareFragment(self.rect.left+16, self.rect.top+16, 16, ENEMY_COLOR, "right", 2, 3))
