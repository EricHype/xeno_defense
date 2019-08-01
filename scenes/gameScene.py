from scene import Scene

import pygame
from pygame import *

import constants
import spritesheet
from camera import Camera, complex_camera

from actors.entity import Entity
from actors.player import Player
from actors.enemy import Enemy
from actors.explodingSquare import getExplodingSquareEntities
from actors.platform import Platform
from actors.squareFragment import SquareFragment
from entityManager import EntityManager
from level import Level
from spritemap import getSpriteMap
from inputHandler import handleKeys

CAMERA_SLACK = 30

PLAYER_COLOR = "#0000FF"
ENEMY_COLOR = "#FF0000"
DEAD_COLOR = "#000000"

TILE_SIZE = 32

entityManager = EntityManager(pygame.sprite.Group())

class GameScene(Scene):
    def __init__(self, argsMap):
        global cameraX, cameraY

        self.spriteMap = getSpriteMap(TILE_SIZE)

        self.player = Player(TILE_SIZE, TILE_SIZE, PLAYER_COLOR, entityManager)
        lvl = argsMap["level"]
        self.level = Level("level{0}.lvl".format(lvl), TILE_SIZE, self.spriteMap, entityManager)
        self.camera = Camera(complex_camera, self.level.pixelWidth, self.level.pixelHeight)
    
        entityManager.addEntity(self.player)

    def render(self, screen):
        # draw background
        for y in range(32):
            for x in range(32):
                screen.blit(self.spriteMap[" "], (x * 32, y * 32))

        w, h = screen.get_size()
        self.camera.update(self.player, w, h) # camera follows player. Note that we could also follow any other sprite

        for e in entityManager.getEntities():
            if(e.isActive):
                screen.blit(e.image, self.camera.apply(e)) 
        pygame.display.update()

    def update(self, keys):
        if keys["shouldQuit"]:
            raise SystemExit

        for e in entityManager.getEntities():
            if type(e) is Player:
                e.update(keys["up"], keys["down"], keys["left"], keys["right"], 
                    keys["running"], entityManager.platforms, entityManager.enemies)
            if type(e) is Enemy:
                e.update(entityManager.platforms)
            if(type(e) is SquareFragment):
                e.update(entityManager.platforms)

        if not self.player.isActive:
           self.manager.scene_change("GameOver", { "text": "You lose!"})
        
        m = list(filter(lambda enemy: enemy.isActive, entityManager.enemies))
        if(len(m)< 1):
            self.manager.scene_change("GameOver", { "text": "You win!"})

    def handle_events(self, events):
        return handleKeys(events)
        
        

    
