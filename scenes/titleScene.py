import pygame
from pygame import *

class TitleScene(object):
    def __init__(self, argsMap):
        super(TitleScene, self).__init__()
        self.font = pygame.font.SysFont('Arial', 56)
        self.sfont = pygame.font.SysFont('Arial', 32)

    def render(self, screen):
        # beware: ugly! 
        screen.fill((0, 200, 0))
        text1 = self.font.render('Evil Red Squares', True, (255, 255, 255))
        text2 = self.sfont.render('> press space to start <', True, (255, 255, 255))
        screen.blit(text1, (200, 50))
        screen.blit(text2, (200, 350))

    def update(self, keys):
        pass

    def handle_events(self, events):
        shouldQuit = False

        for e in events:
            if e.type == KEYDOWN: 
                if e.key == K_SPACE:
                    self.manager.scene_change("Game", {"level" : 0})
                if e.key == K_ESCAPE:
                    shouldQuit = True
            
        return {
            "shouldQuit" : shouldQuit,
            "up" : False,
            "down" : False,
            "left" : False,
            "right" : False,
            "running" : False
        }