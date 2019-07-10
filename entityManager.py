from actors.explodingSquare import getExplodingSquareEntities
import random

class EntityManager(object):
    def __init__(self, entities):
        self.entites = entities

    def getEntities(self):
        return self.entites

    def addEntity(self, entity):
        self.entites.add(entity)

    def removeEntity(self, entity):
        self.entites.remove(entity)

    def killEntity(self, entity):
        forceMultiplier = random.uniform(1.0, 3.0)
        deathEntities = getExplodingSquareEntities(entity.rect.centerx, 
            entity.rect.centery, entity.color, 16, forceMultiplier)
        self.removeEntity(entity)    
        self.entites.add(deathEntities)

    