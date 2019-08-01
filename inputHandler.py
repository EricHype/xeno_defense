import pygame
from pygame import *

def handleKeys(events):
    pressed = pygame.key.get_pressed()
    up, left, down, right, running, shouldQuit = [pressed[key] for key in 
        (K_UP, K_LEFT, K_DOWN, K_RIGHT, K_SPACE, K_ESCAPE)]
    return {
        "up" : up,
        "left" : left,
        "down" : down,
        "right" : right,
        "running" : running,
        "shouldQuit" : shouldQuit,
    }