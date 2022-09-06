import os
import pygame
import random
from collidables import Collidable


class Room():
    doors = [True, True, True, True] #sets which doors are useable
    cachedBackground = None

    def __init__(self, seed, position, doors, roomType, surface, roomXY):
        self.seed = seed #will be a array, parsed to determine room contents
        self.position = position
        self.doors = doors
        self.roomType = roomType
        self.surface = surface
        self.maxX = roomXY[0]+2
        self.maxY = roomXY[1]+2
        self.cachedBackground = pygame.surface.Surface((surface.get_width(),surface.get_height()))
        self.group = pygame.sprite.Group()


    def getRoomType(self):
        return self.roomType
    
    def getSpriteGroup(self):
        return self.group

    def loadRoomCache(self):
        self.surface = self.cachedBackground.copy()


    
    def drawRoom(self, image_room_paths):
        h = self.surface.get_height()
        w = self.surface.get_width()
        cellSize = (w/self.maxX, h/self.maxY)


        scaledStone = pygame.transform.scale(image_room_paths[0], cellSize)

        for y in range(self.maxY):
            for x in range(self.maxX):
                xPos=(w/self.maxX)*x-(w/self.maxX)+w/self.maxX
                yPos=(h/self.maxY)*y-(h/self.maxY)+h/self.maxY
                if((x != 0 and y != 0) and (x != 16 and y != 0)  and (x != 16 and y != 11)):
                    self.surface.blit(scaledStone, (xPos,yPos))
                  

                if isinstance(self.seed[y][x], Collidable):
                    obstacle = self.seed[y][x].getImage()

                    
                else:
                    obs = self.seed[y][x]
                    if (obs == "Nothing"):
                        continue
                    elif (obs == "Blocked"):
                        obstacle = image_room_paths[4]

                scaledObstacle = pygame.transform.scale(obstacle, cellSize)
                self.surface.blit(scaledObstacle, (xPos,yPos))
                
        self.cachedBackground = self.surface.copy()




    

        
        
    
    

    
