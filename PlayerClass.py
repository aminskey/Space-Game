import pygame
import FireClass

from pygame.locals import *
from SpriteGroups import *

class Player(pygame.sprite.Sprite):
        def __init__(self, mainWindow, model="quake"):
                super().__init__()

                self.neutral_image = pygame.image.load("ships/model_" + model + "/" + model + "-1.png")
                self.destroyed_image = pygame.image.load("ships/model_" + model + "/" + model + "-2.png")

                self.image = self.neutral_image
                self.rect = self.image.get_rect()
                self.health = 100

                self.moveSpeed = 6
                self.mainWindow = mainWindow
                self.enemyGroup = None

        def move(self, keys):
                if keys[K_RIGHT]:
                        if self.rect.midright[0] < self.mainWindow.get_width():
                                self.rect.centerx += self.moveSpeed
                if keys[K_LEFT]:
                        if self.rect.midleft[0] > 0:
                                self.rect.centerx -= self.moveSpeed

        def fire(self, keys):
                if keys[K_SPACE]:
                        tmpBullet = FireClass.Bullet(self.enemyGroup, (0, 0))
                        tmpBullet.rect.midbottom = self.rect.midtop
                        tmpBullet.add(bulletGroup)
                if keys[K_f]:
                        tmpBullet = FireClass.Torpedo(self.enemyGroup, (0, 0))
                        tmpBullet.rect.midbottom = self.rect.midtop
                        tmpBullet.add(bulletGroup)


        def update(self, moveSpeed, enemyGroup):
                keys = pygame.key.get_pressed()

                self.enemyGroup = enemyGroup
                self.moveSpeed = moveSpeed

                self.move(keys)
                self.fire(keys)