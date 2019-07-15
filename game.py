import pygame
from pygame import *

import constants
import spritesheet
from camera import Camera

from actors.entity import Entity
from actors.player import Player
from actors.enemy import Enemy
from actors.explodingSquare import getExplodingSquareEntities
from actors.platform import Platform
from actors.squareFragment import SquareFragment
from entityManager import EntityManager
from level import Level
from spritemap import getSpriteMap

WIN_WIDTH = 800
WIN_HEIGHT = 640
HALF_WIDTH = int(WIN_WIDTH / 2)
HALF_HEIGHT = int(WIN_HEIGHT / 2)

DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
DEPTH = 32
FLAGS = 0
CAMERA_SLACK = 30

PLAYER_COLOR = "#0000FF"
ENEMY_COLOR = "#FF0000"
DEAD_COLOR = "#000000"

TILE_SIZE = 32

entityManager = EntityManager(pygame.sprite.Group())

def complex_camera(camera, target_rect):
    # we want to center target_rect
    x = -target_rect.center[0] + WIN_WIDTH/2 
    y = -target_rect.center[1] + WIN_HEIGHT/2
    # move the camera. Let's use some vectors so we can easily substract/multiply
    camera.topleft += (pygame.Vector2((x, y)) - pygame.Vector2(camera.topleft)) * 0.06 # add some smoothness coolnes
    # set max/min x/y so we don't see stuff outside the world
    camera.x = max(-(camera.width-WIN_WIDTH), min(0, camera.x))
    camera.y = max(-(camera.height-WIN_HEIGHT), min(0, camera.y))

    return camera

def main():
    global cameraX, cameraY
    #pygame.init()
    screen = pygame.display.set_mode(DISPLAY, FLAGS, DEPTH)
    pygame.display.set_caption("Use arrows to move!")
    timer = pygame.time.Clock()

    spriteMap = getSpriteMap(TILE_SIZE)

    up = down = left = right = running = False

    player = Player(TILE_SIZE, TILE_SIZE, PLAYER_COLOR, entityManager)
    
    x = y = 0
    level = Level("level0.lvl", TILE_SIZE, spriteMap, entityManager)
    camera = Camera(complex_camera, level.pixelWidth, level.pixelHeight)
 
    entityManager.addEntity(player)
    while 1:
        timer.tick(60)
        for e in pygame.event.get():
            if e.type == QUIT: 
                raise SystemExit("QUIT")
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    raise SystemExit("ESCAPE")
                if e.key == K_UP:
                    up = True
                if e.key == K_DOWN:
                    down = True
                if e.key == K_LEFT:
                    left = True
                if e.key == K_RIGHT:
                    right = True
                if e.key == K_SPACE:
                    running = True

            if e.type == KEYUP:
                if e.key == K_UP:
                    up = False
                if e.key == K_DOWN:
                    down = False
                if e.key == K_RIGHT:
                    right = False
                if e.key == K_LEFT:
                    left = False
                if e.key == K_RIGHT:
                    right = False

        # draw background
        for y in range(32):
            for x in range(32):
                screen.blit(spriteMap[" "], (x * 32, y * 32))

        camera.update(player) # camera follows player. Note that we could also follow any other sprite

        # update player, draw everything else
        for e in entityManager.getEntities():
            if type(e) is Player:
                e.update(up, down, left, right, running, entityManager.platforms, entityManager.enemies)
            if type(e) is Enemy:
                e.update(entityManager.platforms)
            if(type(e) is SquareFragment):
                e.update(entityManager.platforms)
            # apply the offset to each entity.
            # call this for everything that should scroll,
            # which is basically everything other than GUI/HUD/UI
            if(e.isActive):
                screen.blit(e.image, camera.apply(e)) 

        pygame.display.update()
                
if __name__ == "__main__":
    main()