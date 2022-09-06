from copy import deepcopy
import os
import pygame
import copy


class minimap(pygame.sprite.Sprite):
    

    def __init__(self, size, surface):
        pygame.sprite.Sprite.__init__(self)
          
        self.rooms = []
        self.discoveredDoors = []
        self.discoveredRooms = []
        self.arrayMap = []
        for y in range(size):
            self.rooms.append([])
            self.discoveredDoors.append([])
            self.discoveredRooms.append([])
            for x in range(size):
                self.rooms[y].append(None)
                self.discoveredRooms[y].append(False)
                self.discoveredDoors[y].append([False, False, False, False])
        
        self.surface = surface
        self.size = size 
        self.cachedBackground = pygame.surface.Surface((surface.get_width(),surface.get_height()))



    def addRoom(self, room, location):
        self.rooms[location[1]][location[0]] = room 

    def discoverDoor(self, location, door):
        self.discoveredDoors[location[1]][location[0]][door] = True
        for d in self.discoveredDoors[location[1]][location[0]]:
            if not d:
                return
        self.discoveredRooms[location[1]][location[0]] = True
    
    def discoverRoom(self, location):
        self.discoveredDoors[location[1]][location[0]] = [True, True, True, True]
        self.discoveredRooms[location[1]][location[0]] = True
            
    def loadMap(self):
        self.surface = self.cachedBackground.copy()



    def drawMap(self, scale, currentLocation):
        path1 = os.path.join("assets/minimap/", "northPath.png")
        path2 = os.path.join("assets/minimap/", "eastPath.png")
        path3 = os.path.join("assets/minimap/", "southPath.png")
        path4 = os.path.join("assets/minimap/", "westPath.png")
        ##MAY CAUSE ERRORS IF SCALE IS OUTSIDE OF THE POSSIBLE ROOMS (ie; a corner)
        #mapSize = scale
        mapSize = (scale*2)-1
        possible = [[0,-1],[1,0],[0,1],[-1,0]] #Y,X
        doorCord = [2,3,0,1]

        for y in range(mapSize):
            self.arrayMap.append([])
            for x in range(mapSize):
                self.arrayMap[y].append(None)

        mapStart = (currentLocation[0]-(scale-1), currentLocation[1]-(scale-1))
        mapEnd = (currentLocation[0]+(scale-1), currentLocation[1]+(scale-1))
        
        # if scale % 2 == 0:
        #     mapStart = ((int)(currentLocation[0]-(scale/2)), (int)(currentLocation[1]-(scale/2)))
        #     mapEnd = ((int)(currentLocation[0]+(scale/2)-1), (int)(currentLocation[1]+(scale/2)-1))
        # else:
        #     mapStart = ((int)(currentLocation[0]-((scale-1)/2)), (int)(currentLocation[1]-((scale-1)/2)))
        #     mapEnd = ((int)(currentLocation[0]+((scale-1)/2)), (int)(currentLocation[1]+((scale-1)/2))) 
            
        h = self.surface.get_height()
        w = self.surface.get_width()
        cellSize = (w/mapSize, h/mapSize)

        mapPath = os.path.join("assets/minimap", "mapBackground.png")
        mapBkg = pygame.image.load(mapPath)
        mapBackground = pygame.transform.scale(mapBkg, (w, h))
        self.surface.blit(mapBackground, (0,0))
        
        
        
        
        for y in range(self.size):
            if(y >= mapStart[1] and y <= mapEnd[1]):
                for x in range(self.size):
                    if(x >= mapStart[0] and x <= mapEnd[0]):
                        if self.discoveredRooms[y][x]:
                            relativeY = y-mapStart[1]
                            relativeX = x-mapStart[0]
                            xPos=((w/mapSize)*(relativeX))
                            yPos=((h/mapSize)*(relativeY))

                            self.arrayMap[relativeY][relativeX] = self.rooms[y][x]

                            image_path = self.rooms[y][x].getRoomType()
                            roomSprite = pygame.image.load(image_path)
                            scaledRoom = pygame.transform.scale(roomSprite, cellSize)

                            self.surface.blit(scaledRoom, (xPos,yPos))
                            for r in range(4):
                                for count, door in enumerate(self.discoveredDoors[y+possible[r][1]][x+possible[r][0]]):
                                    if count == doorCord[r]:
                                        if door and self.rooms[y+possible[r][1]][x+possible[r][0]].doors[count]:
                                            if self.discoveredDoors[y][x][r] and self.rooms[y][x].doors[r]:
                                                if r == 0:
                                                    path = path1
                                                if r == 1:
                                                    path = path2
                                                if r == 2:
                                                    path = path3
                                                if r == 3:
                                                    path = path4
                                                        
                                                            
                                                pathSprite = pygame.image.load(path)
                                                scaledPath = pygame.transform.scale(pathSprite, cellSize)
                                                self.surface.blit(scaledPath, (xPos,yPos))

                                                
                                            


        self.cachedBackground = self.surface.copy()

        


                        


                



    
    
