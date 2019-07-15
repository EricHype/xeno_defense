import os
import json

from actors.platform import Platform
from actors.enemy import Enemy

ENEMY_COLOR = "#FF0000"

class Level(object):
    def __init__(self, fileName, tileSize, spriteMap, entityManager):
        dirname = os.path.dirname(__file__)
        sub_dir = os.path.join(dirname, "levels")
        sub_file_path = os.path.join(sub_dir, fileName)

        file_object = open(sub_file_path, 'r')

        data = json.load(file_object)
        self.contents = data["entityMap"]

        self.height = self.__getHeight()
        self.width = self.__getWidth()

        self.pixelHeight = self.height * tileSize
        self.pixelWidth = self.width * tileSize

        file_object.close()
        x = y = 0
        
        for row in self.contents:
            for col in row:
                if col == "P":
                    p = Platform(x, y, spriteMap["P"])
                    entityManager.addPlatform(p)
                if col == "E":
                    e = Enemy(x,y, ENEMY_COLOR, entityManager)
                    entityManager.addEnemy(e)
                if col == "W":
                    wall = Platform(x,y, spriteMap["W"])
                    entityManager.addPlatform(wall)
                if col == "C":
                    ceiling = Platform(x,y, spriteMap["C"])
                    entityManager.addPlatform(ceiling)
                x += tileSize
            y += tileSize
            x = 0


    def __getWidth(self):
        max_length = max(map(len, self.contents))
        return max_length

    def __getHeight(self):
        return len(self.contents)