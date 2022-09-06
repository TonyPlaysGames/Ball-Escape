from pygame.math import Vector2
from math import sin, radians, degrees, copysign, atan
import os
import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, angle = 0.0):
        pygame.sprite.Sprite.__init__(self)
        self.velocity = Vector2(x, y)
        self.position = Vector2(x, y)
        # pygame.sprite.Sprite.rect = self.rect
        self.max_velocity = 1
        self.max_velocityN = -1
        self.angle = angle
        image_path = os.path.join("assets", "player.png")
        player_image = pygame.image.load(image_path).convert_alpha()
        player_image = pygame.transform.scale(player_image, (50,50))
        #rotated = pygame.transform.rotate(ball_image, 0)
        self.image = player_image
        self.rect = self.image.get_rect(topleft = (self.position.x,self.position.y))
        # I believe to get the built-in collision functionality you need to be using the pygame.Rect class for the bounding box of the sprites like above -DMM
        # Read the "Rects are your friends" section here: https://www.pygame.org/docs/tut/newbieguide.html

    def update(self, dt):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_w]:
            self.velocity.y -= 15
        elif pressed[pygame.K_s]:
            self.velocity.y += 15
        else:
            self.velocity.y = 0

        if pressed[pygame.K_a]:
            self.velocity.x -= 15
        elif pressed[pygame.K_d]:
            self.velocity.x += 15
        else:
            self.velocity.x = 0
            

        self.velocity.x = max(self.max_velocityN, min(self.velocity.x, self.max_velocity))
        self.velocity.y = max(self.max_velocityN, min(self.velocity.y, self.max_velocity))
        self.position += self.velocity * dt
        self.rect.x = self.position.x
        self.rect.y = self.position.y
    
    # def draw(self, screen):
    #     playerSurf = pygame.Surface((5, 5))
    #     print('made surface')
    #     playerSurf.blit(self.image, (0,0), (0,0,5,5) )
    #     ppu = 20    
    #     screen.blit(playerSurf, self.position * ppu)

class Ball(pygame.sprite.Sprite):
    def __init__( self, x, y, angle = 0.0):
        pygame.sprite.Sprite.__init__(self)
        self.angle = angle
        self.rect = Vector2(x, y)
        self.velocity = Vector2(0.0, 0.0)
        self.max_velocity = 1.5
        # pygame.sprite.Sprite.rect = self.rect
        image_path = os.path.join("assets", "hairyBall.png")
        player_image = pygame.image.load(image_path).convert_alpha()
        rotated = pygame.transform.scale(player_image, (50,50))
        rotated = pygame.transform.rotate(rotated, self.angle)
        self.image = rotated

    def update(self, dt, playerPosition):
        self.velocity.x += (playerPosition.x-self.rect.x)
        self.velocity.x = max(0, min(self.velocity.x, self.max_velocity))
        self.angle = degrees(atan((playerPosition.y - self.rect.y)/(playerPosition.x - self.rect.x)))
        self.rect += self.velocity.rotate(self.angle) * dt
        # pygame.sprite.Sprite.rect = self.rect

    def draw(self, surface):
        ppu = 20
        #self.image = rotated
        surface.blit(self.image, self.rect * ppu)


