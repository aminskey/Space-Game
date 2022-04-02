import pygame

from pygame.locals import *
from PublicVar import *
from random import randint

class Asteroid(pygame.sprite.Sprite):
        def __init__(self, mainWindow, img="objects/asteroid.png"):
                super().__init__()

                self.orgImage = pygame.image.load(img)
                self.image = pygame.transform.scale(self.orgImage, (self.orgImage.get_width()//8, self.orgImage.get_height()//8))
                self.rect = self.image.get_rect()

                self.mainWindow = mainWindow

                self.speed = 0

                self.direction = 1

                self.pos = (0, 0)
                self.itr = 0
        def update(self):
                self.itr += 0.25
                self.pos = (self.rect.center[0], self.rect.center[1] + self.direction)

                if self.rect.centery <= self.mainWindow.get_height() * 3//4 and self.rect.midbottom[1] > 0 and self.image.get_width() < self.orgImage.get_width() * 3:
                        if self.itr % 2 == 0:
                                self.image = pygame.transform.scale(self.orgImage, (self.image.get_width() + 1, self.image.get_height() + 1))
                                self.rect = self.image.get_rect()
                                self.rect.center = self.pos
                        if self.itr % 10 == 0:
                                self.rect.centerx += self.speed
                else:
                        self.kill()