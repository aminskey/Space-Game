import pygame

from pygame.locals import *
from SpriteGroups import *

class Asteroid(pygame.sprite.Sprite):
        def __init__(self, mainWindow, img="objects/asteroid.png"):
                super().__init__()

                self.orgImage = pygame.image.load(img)
                self.image = pygame.transform.scale(self.orgImage, (self.orgImage.get_width()//8, self.orgImage.get_height()//8))
                self.rect = self.image.get_rect()

                self.mainWindow = mainWindow

                self.pos = (0, 0)
                self.itr = 0
        def update(self):
                self.itr += 0.25
                self.pos = (self.rect.center[0], self.rect.center[1] + 0.5)

                if self.rect.centery <= self.mainWindow.get_height() * 3//4:
                        if self.itr % 1 == 0:
                                self.image = pygame.transform.scale(self.orgImage, (self.image.get_width() + 1, self.image.get_height() + 1))
                                self.rect.center = self.pos

                else:
                        self.kill()