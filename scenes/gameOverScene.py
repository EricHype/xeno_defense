import pygame
from pygame import *

class GameOverScene(object):
    def __init__(self, argsMap):
        self.text = argsMap["text"]
        super(GameOverScene, self).__init__()
        self.font = pygame.font.SysFont('Arial', 56)

    def render(self, screen):
        # ugly! 
        screen.fill((0, 200, 0))
        text1 = self.font.render(self.text, True, (255, 255, 255))
        screen.blit(text1, (200, 50))

    def update(self, keys):
        pass

    def handle_events(self, events):
        for e in events:
            if e.type == KEYDOWN:
                self.manager.scene_change("Title", {})