import pygame
import FireClass

from pygame.locals import *
from PublicVar import *
from random import randint
from time import sleep

class Player(pygame.sprite.Sprite):
        def __init__(self, mainWindow, model="quake"):
                super().__init__()

                self.neutral_image = pygame.image.load("ships/player_ships/model_" + model + "/" + model + "-1.png")
                self.destroyed_image = pygame.image.load("ships/player_ships/model_" + model + "/" + model + "-2.png")

                self.image = self.neutral_image
                self.rect = self.image.get_rect()
                self.health = 100

                self.moveSpeed = 6
                self.mainWindow = mainWindow
                self.enemyGroup = None
                self.currAngle = 0
                self.coolDown = 0

        def move(self, keys):
                if keys[K_RIGHT]:
                        if self.rect.midright[0] < self.mainWindow.get_width():
                                self.rect.centerx += self.moveSpeed
                if keys[K_LEFT]:
                        if self.rect.midleft[0] > 0:
                                self.rect.centerx -= self.moveSpeed
                if keys[K_UP]:
                        if self.rect.midtop[1] > self.mainWindow.get_height()//2:
                                self.rect.centery -= self.moveSpeed
                if keys[K_DOWN]:
                        if self.rect.midbottom[1] < self.mainWindow.get_height():
                                self.rect.centery += self.moveSpeed
        def fire(self, keys):
                if self.coolDown <= 0:
                        if keys[K_SPACE]:
                                tmpBullet = FireClass.Bullet(self.enemyGroup, (0, 0))
                                tmpBullet.rect.midbottom = self.rect.midbottom
                                tmpBullet.add(bulletGroup)
                                self.coolDown += 0.5
                        if keys[K_f]:
                                tmpBullet = FireClass.Torpedo(self.enemyGroup, (0, 0))
                                tmpBullet.rect.midbottom = self.rect.midbottom
                                tmpBullet.add(bulletGroup)
                                self.coolDown += 1


        def update(self, moveSpeed, enemyGroup):
                keys = pygame.key.get_pressed()

                if self.coolDown >= -1:
                        self.coolDown -= 0.05

                self.enemyGroup = enemyGroup
                self.moveSpeed = moveSpeed

                if self.health <= 20:
                        self.image = self.destroyed_image

                self.move(keys)
                self.fire(keys)


class EnemyShip(pygame.sprite.Sprite):
        def __init__(self, mainWindow, model="interceptor"):
                super().__init__()

                self.neutral_image = pygame.image.load("ships/enemy_ships/model_" + model + "/" + model + "-1.png")
                self.destoryed_image = pygame.image.load("ships/enemy_ships/model_" + model + "/" + model + "-2.png")

                self.image = pygame.transform.scale(self.neutral_image, (self.neutral_image.get_width()//10, self.neutral_image.get_height()//10))
                self.rect = self.image.get_rect()
                self.health = 50
                self.mainWindow = mainWindow
                self.itr = 0
                self.scorePoints = 20

                self.pos = self.rect.center
        def dead(self):
                tmpSound = pygame.mixer.Sound("sounds/explosion.mp3")
                tmpSound.set_volume(0.5)
                tmpSound.play()

                self.image = self.destoryed_image
                self.kill()

        def update(self):

                self.itr += 0.5

                self.pos = (self.rect.centerx, self.rect.centery + 1)


                if self.image.get_width() <= self.neutral_image.get_width() or self.rect.centery >= self.mainWindow.get_height() * 7//8:
                        if self.itr % 1 == 0:
                                self.image = pygame.transform.scale(self.neutral_image, (self.image.get_width() + 1, self.image.get_height() + 1))
                                self.rect = self.image.get_rect()
                                self.rect.center = self.pos
                else:
                        self.kill()

                if self.health <= 0:
                        self.dead()

                if self.rect.midright[0] < 0:
                        self.kill()


                if self.itr % randint(80, 95) == 0:
                        tmpBullet = FireClass.EnemyFire(playersGroup, window=self.mainWindow)
                        tmpBullet.rect.midtop = self.rect.center
                        bulletGroup.add(tmpBullet)