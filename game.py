import pygame
from pygame import *

from entityManager import EntityManager
from sceneManager import SceneMananger

entityManager = EntityManager(pygame.sprite.Group())

WIN_WIDTH = 800
WIN_HEIGHT = 640
HALF_WIDTH = int(WIN_WIDTH / 2)
HALF_HEIGHT = int(WIN_HEIGHT / 2)
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
DEPTH = 32
FLAGS = 0

def main():
    pygame.init()
    screen = pygame.display.set_mode(DISPLAY, FLAGS, DEPTH)
    pygame.display.set_caption("Use arrows to move!")
    timer = pygame.time.Clock()

    manager = SceneMananger()

    while 1:
        timer.tick(60)
        if pygame.event.get(QUIT):
            return

        scene = manager.get_scene()    
        keys = scene.handle_events(pygame.event.get())
        scene.update(keys)
        scene.render(screen)

        pygame.display.flip()

                        
if __name__ == "__main__":
    main()