import numpy as np
import pygame
import random
import os
import tkinter
import copy
from pygame.math import Vector2
from math import sin, radians, degrees, copysign, atan
from minimap import minimap
from movables import *
from room import *
from collidables import *

class Button():
	def __init__(self, x, y, image, scale):
		width = image.get_width()
		height = image.get_height()
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False

	def draw(self, surface):
		action = False
		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				action = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		#draw button on screen
		surface.blit(self.image, (self.rect.x, self.rect.y))

		return action


#source credit: https://pythonprogramming.altervista.org/buttons-in-pygame/

class Game:
    rooms = []
    mapSize = 10
    mapScale = 3
    currentLocation = (5,5)

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Maze")
        self.width = 1403 ## ratio MUST ALWAYS be somewhere width ~~ height*1.8 or olse a bug will occur
        self.height = 792 ## if changing ratio, must play with exact numbers to find one that wont bug out
        #KNOWN RATIOS; 1800x1000, 900x500, 1397x772, NEW 1403x792

        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.ticks = 60
        self.exit = False
        

    def run(self, difficulty):
        print("Welcome the difficulty is " + difficulty)
        roomXY = (15,9)

        mapRoom = os.path.join("assets/minimap/", "mapRoom.png")
        notAccesible = os.path.join("assets/minimap/", "roomNotAccesible.png")
        blockedTop = os.path.join("assets/minimap/", "blockedTop.png")
        blockedBottom = os.path.join("assets/minimap/", "blockedBottom.png")
        blockedLeft1 = os.path.join("assets/minimap/", "blockedLeft1.png")
        blockedRight1 = os.path.join("assets/minimap/", "blockedRight1.png")
        blockedLeft3 = os.path.join("assets/minimap/", "blockedLeft3.png")
        blockedRight3 = os.path.join("assets/minimap/", "blockedRight3.png")

        room_img_paths = []
        stone = os.path.join("assets/room/", "stone.png")
        room_img_paths.append(pygame.image.load(stone))
        
        boxes = []
        box1 = os.path.join("assets/room/", "box1.png")
        box2 = os.path.join("assets/room/", "box2.png")
        box3 = os.path.join("assets/room/", "box3.png")
        box4 = os.path.join("assets/room/", "box4.png")
        box5 = os.path.join("assets/room/", "box5.png")
        box6 = os.path.join("assets/room/", "box6.png")
        boxes.append(pygame.image.load(box1))
        boxes.append(pygame.image.load(box2))
        boxes.append(pygame.image.load(box3))
        boxes.append(pygame.image.load(box4))
        boxes.append(pygame.image.load(box5))
        boxes.append(pygame.image.load(box6))
        room_img_paths.append(boxes)

        landmines = []
        landmine1 = os.path.join("assets/room/", "landmine1.png")
        landmine2 = os.path.join("assets/room/", "landmine2.png")
        landmine3 = os.path.join("assets/room/", "landmine3.png")
        landmines.append(pygame.image.load(landmine1))
        landmines.append(pygame.image.load(landmine2))
        landmines.append(pygame.image.load(landmine3))
        room_img_paths.append(landmines)

        puddles = []
        puddle1 = os.path.join("assets/room/", "puddle1.png")
        puddle2 = os.path.join("assets/room/", "puddle2.png")
        puddle3 = os.path.join("assets/room/", "puddle3.png")
        puddles.append(pygame.image.load(puddle1))
        puddles.append(pygame.image.load(puddle2))
        puddles.append(pygame.image.load(puddle3))
        room_img_paths.append(puddles)

        blocked = os.path.join("assets/room/", "blockedTile.png")
        #stoneWall = os.path.join("assets/room/", "stoneWall.png")
        room_img_paths.append(pygame.image.load(blocked))
        #room_img_paths.append(pygame.image.load(stoneWall))

        walls = []
        stoneUpper = os.path.join("assets/room/", "stoneUpper.png")
        stoneRight = os.path.join("assets/room/", "stoneRight.png")
        stoneLower = os.path.join("assets/room/", "stoneLower.png")
        stoneLeft = os.path.join("assets/room/", "stoneLeft.png")
        walls.append(pygame.image.load(stoneUpper))
        walls.append(pygame.image.load(stoneRight))
        walls.append(pygame.image.load(stoneLower))
        walls.append(pygame.image.load(stoneLeft))
        room_img_paths.append(walls)

        doors = []
        doorNORTH = os.path.join("assets/room/", "doorNORTH.png")
        doorEAST = os.path.join("assets/room/", "doorEAST.png")
        doorSOUTH = os.path.join("assets/room/", "doorSOUTH.png")
        doorWEST = os.path.join("assets/room/", "doorWEST.png")
        doors.append(pygame.image.load(doorNORTH))
        doors.append(pygame.image.load(doorEAST))
        doors.append(pygame.image.load(doorSOUTH))
        doors.append(pygame.image.load(doorWEST))
        room_img_paths.append(doors)

        roomSurface = pygame.surface.Surface(((int)(2*(self.width/3)), (int)(2*(self.height/3))))
        #(int)((2*(self.width/3))+(((2*(self.width/3))/roomXY[0]+2)*2)), 
        #((int)(2*(self.height/3))+(((2*(self.height/3))/roomXY[1]+2)*2))
        mapSurface = pygame.surface.Surface(((int)(self.width/6.82), (int)(self.height/4.09))) 
        mini = minimap(self.mapSize, mapSurface)

        for y in range(self.mapSize):
            self.rooms.append([])
            for x in range(self.mapSize):
                self.rooms[y].append(None)
                doorSpawn = random.choices(
                    ## Format, [North, East, South, West]
                    population = [([True,True,True,True], mapRoom), 
                                ([False,False,False,False], notAccesible), 
                                ([False,False,True,False], blockedTop), 
                                ([True,False,False,False], blockedBottom), 
                                ([False,True,False,False], blockedLeft1), 
                                ([False,False,False,True], blockedRight1),
                                ([True,True,True,False], blockedLeft3),
                                ([True,False,True,True], blockedRight3)],
                    weights = [0.7, 0.05, 0.025, 0.025, 0.025, 0.025, 0.075, 0.075], 
                    k = 1
                )

                if((y,x) == self.currentLocation):
                    doorSpawn = [([True,True,True,True], mapRoom)]

                seed = []
                for i in range(roomXY[1]):
                    s = random.choices(
                        population = ["Nothing", "Box", "Landmine", "Puddle"], 
                        weights = [0.9, 0.05, 0.03, 0.02], 
                        k = roomXY[0]
                        )
                    seed.append(s)
                    for j in range(len(s)):
                        if(s[j] == "Box"):
                            seed[i][j] = Collidable(random.choice(room_img_paths[1]), "Box")
                        elif(s[j] == "Landmine"):
                            seed[i][j] = Collidable(random.choice(room_img_paths[2]), "Landmine")
                        elif(s[j] == "Puddle"):
                            seed[i][j] = Collidable(random.choice(room_img_paths[3]), "Puddle")
                        else:
                            seed[i][j] = s[j]
                


                for i in range(roomXY[1]):
                    if doorSpawn[0][1] == mapRoom:
                        continue
                    elif doorSpawn[0][1] == notAccesible:
                        for row in seed:
                            for col in range(len(row)):
                                row[col] = "Blocked"

                    elif doorSpawn[0][1] == blockedTop:
                        for r, row in enumerate(seed):
                            if r < 5:
                                for col in range(len(row)):
                                    row[col] = "Blocked"
                            if r == 5:
                                for col in range(len(row)):
                                        row[col] = Collidable(room_img_paths[5], "Wall")
                    
                    elif doorSpawn[0][1] == blockedBottom:
                        for r, row in enumerate(seed):
                            if r > 5:
                                for col in range(len(row)):
                                    row[col] = "Blocked"
                            if r == 5:
                                for col in range(len(row)):
                                        row[col] = Collidable(room_img_paths[5], "Wall")
                        
                    elif doorSpawn[0][1] == blockedLeft3:
                        for row in seed:
                            for col in range(len(row)):
                                if col < 2:
                                    row[col] = "Blocked"
                                if col == 2:    
                                    row[col] = Collidable(room_img_paths[5][3], "stoneLeft")
                        
                    elif doorSpawn[0][1] == blockedRight3:
                        for row in seed:
                            for col in range(len(row)):
                                if col > 12:
                                    row[col] = "Blocked"
                                if col == 12:    
                                    row[col] = Collidable(room_img_paths[5][1], "stoneRight")
                        
                    elif doorSpawn[0][1] == blockedLeft1:
                        for row in seed:
                            for col in range(len(row)):
                                if col < 7:
                                    row[col] = "Blocked"
                                if col == 7:    
                                    row[col] = Collidable(room_img_paths[5], "Wall")
                        
                    elif doorSpawn[0][1] == blockedRight1:
                        for row in seed:
                            for col in range(len(row)):
                                if col > 9:
                                    row[col] = "Blocked"
                                if col == 9:    
                                    row[col] = Collidable(room_img_paths[5], "Wall")

                tempList = np.array(seed)
                seed = np.pad(tempList, 1).tolist()

                for r, row in enumerate(seed):
                    for col in range(len(row)):
                        if col == 0:
                            if 4 <= r <= 6:
                                row[col] = Collidable(room_img_paths[6][3], "DoorWEST")
                            elif(0 < r < 10):
                                row[col] = Collidable(room_img_paths[5][3], "stoneLeft")
                            else:
                                row[col] = "Nothing"
                        
                        elif col == 16:
                            if 4 <= r <= 6:
                                row[col] = Collidable(room_img_paths[6][1], "DoorEAST")
                            elif(0 < r < 10):
                                row[col] = Collidable(room_img_paths[5][1], "stoneRight")
                            else:
                                row[col] = "Nothing"

                        elif r == 0:
                            if 7 <= col <= 9:
                                row[col] = Collidable(room_img_paths[6][0], "DoorNORTH")
                            elif(0 < col < 16):
                                row[col] = Collidable(room_img_paths[5][0], "stoneUpper")
                            else:
                                row[col] = "Nothing"

                        elif r == 10:
                            if 7 <= col <= 9:
                                row[col] = Collidable(room_img_paths[6][2], "DoorSOUTH")
                            elif(0 < col < 16):
                                row[col] = Collidable(room_img_paths[5][2], "stoneLower")
                            else:
                                row[col] = "Nothing"

                self.rooms[y][x] = Room(copy.copy(seed), 1, copy.copy(doorSpawn[0][0]), copy.copy(doorSpawn[0][1]), roomSurface, roomXY)
                mini.addRoom(self.rooms[y][x],(x,y))

        self.rooms[self.currentLocation[1]][self.currentLocation[0]].drawRoom(room_img_paths) # does this need to happen in the game loop? -DMM
        mini.discoverRoom(self.currentLocation)
        # mini.discoverRoom((self.currentLocation[0]-1, self.currentLocation[1]))
        # mini.discoverRoom((self.currentLocation[0], self.currentLocation[1]-1))
        # mini.discoverRoom((self.currentLocation[0]+1, self.currentLocation[1]))
        # mini.discoverRoom((self.currentLocation[0], self.currentLocation[1]+1))

        mini.drawMap(self.mapScale, self.currentLocation)


        b1 = Button((int)(self.width/1.2)+40, (int)(self.height/4.09)+50, pygame.image.load("assets/minussign.png").convert_alpha(), 0.35)
        b2 = Button((int)(self.width/1.2)+90, (int)(self.height/4.09)+50, pygame.image.load("assets/plussign.png").convert_alpha(), 0.35)
        ball = Ball(0,0)
        player = Player(15,25) 

        playerGS = pygame.sprite.GroupSingle(player)
        ballGS = pygame.sprite.GroupSingle(ball)
        ScreenShakes = False
        while not self.exit:
            dt = pygame.time.get_ticks() / 10000
            self.screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True
            
            
            # Clear the roomSurface and redraw the room to get rid of the trails -DMM
            roomSurface.fill((0,0,0))
            self.rooms[self.currentLocation[1]][self.currentLocation[0]].drawRoom(room_img_paths) 
            # this is probably not the most performant way to go. I think looking into pygame.display.update() 
            # and/or only clearing the necessary part of the room might be worthwhile if things get laggy. -DMM


            ballGS.update(dt, player.position)
            ballGS.draw(roomSurface)

            playerGS.update(dt)
            playerGS.draw(roomSurface)

            playerGS.update(dt)
            playerGS.draw(roomSurface)
                

            self.screen.fill((0, 0, 0))
            if (b1.draw(self.screen) and self.mapScale < (int)(self.mapSize/2)+1):
                self.mapScale+=1
                print("+ Clicked")
            if (b2.draw(self.screen) and self.mapScale < 4):
                self.mapScale-=1

            mini.drawMap(self.mapScale, self.currentLocation)    
            if not ScreenShakes:
                self.screen.blit(roomSurface, (self.width/12, self.height/5))
            else:
                self.screen.blit(roomSurface, (self.width/12 + random.random()*10, self.height/5+random.random()*10))
            self.screen.blit(mapSurface, (self.width-(self.width/4.6), self.height/20))
        
            pygame.display.flip() # you can call pygame.display.update(list of rectangles) to get more efficiency on drawing
            self.clock.tick(self.ticks)
        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run("1")
#source credit: https://pythonprogramming.altervista.org/buttons-in-pygame/
