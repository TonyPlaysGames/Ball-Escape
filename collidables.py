import pygame

class Collidable(pygame.sprite.Sprite):
    def __init__ (self, path, type):
        self.path = path
        self.type = type

    def getImage(self):
        return self.path
        
    def getType(self):
        return self.type