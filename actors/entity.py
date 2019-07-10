import pygame

from enum import Enum

class EntityState(Enum):
    ALIVE = 1
    RECOVER = 2
    DYING = 3
    DEAD = 4
    INERT = 5 

class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

