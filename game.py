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

WIN_WIDTH = 800
WIN_HEIGHT = 640
HALF_WIDTH = int(WIN_WIDTH / 2)
HALF_HEIGHT = int(WIN_HEIGHT / 2)

DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
DEPTH = 32
FLAGS = 0
CAMERA_SLACK = 30

ENEMY_COLOR = "#FF0000"
DEAD_COLOR = "#000000"

entityManager = EntityManager(pygame.sprite.Group())

def simple_camera(camera, target_rect):
        l, t, _, _ = target_rect # l = left,  t = top
        _, _, w, h = camera      # w = width, h = height
        return Rect(-l+HALF_WIDTH, -t+HALF_HEIGHT, w, h)

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

    ss = spritesheet.spritesheet('PixelAtlas.png')
    groundImage = ss.load_image_at((0, 0, 32, 32))
    skyimage = ss.load_image_at((32, 96, 32, 32))

    up = down = left = right = running = False

    player = Player(32, 32)
    platforms = []
    enemies = []
    x = y = 0
    level = Level("level0.lvl")

    # build the level
    for row in level.contents:
        for col in row:
            if col == "P":
                p = Platform(x, y, groundImage)
                platforms.append(p)
                entityManager.addEntity(p)
            if col == "E":
                e = Enemy(x,y, ENEMY_COLOR, entityManager)
                enemies.append(e)
                entityManager.addEntity(e)
            x += 32
        y += 32
        x = 0
    
    print("level width:" + str(level.width) )
    print("level height:" + str(level.height))

    total_level_width  = level.width * 32 # calculate size of level in pixels
    total_level_height = level.height * 32    # maybe make 32 an constant
    camera = Camera(complex_camera, total_level_width, total_level_height)

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
                screen.blit(skyimage, (x * 32, y * 32))

        camera.update(player) # camera follows player. Note that we could also follow any other sprite

        # update player, draw everything else
        for e in entityManager.getEntities():
            if type(e) is Player:
                e.update(up, down, left, right, running, platforms, enemies)
            if type(e) is Enemy:
                e.update(platforms)
            if(type(e) is SquareFragment):
                e.update(platforms)
            # apply the offset to each entity.
            # call this for everything that should scroll,
            # which is basically everything other than GUI/HUD/UI
            if(e.isActive):
                screen.blit(e.image, camera.apply(e)) 

        pygame.display.update()
                
if __name__ == "__main__":
    main()