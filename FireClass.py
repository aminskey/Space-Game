import pygame
from pygame.locals import *

class Fire(pygame.sprite.Sprite):
        def __init__(self, vulGroup, pos=(0, 0)):
                super().__init__()
                self.image = pygame.image.load("bullets/player_bullet.png")
                self.rect = self.image.get_rect()

                self.rect.center = pos

                self.speed = 10
                self.damage = 0

                self.killVal = 10
                self.mod = 2
                self.cut = (14, 14)

                self.bullet = True
                self.vulGroup = vulGroup
        def update(self):
                self.rect.centery -= self.speed

                if self.image.get_width() <= self.killVal:
                        self.kill()

                if self.rect.centery % self.mod == 0:

                        self.image = pygame.transform.scale(self.image, (self.image.get_width() - self.cut[0], self.image.get_height() - self.cut[1]))
                        if self.bullet:
                                self.rect.centerx += 4


                if pygame.sprite.spritecollideany(self, self.vulGroup):
                        ship = pygame.sprite.spritecollide(self, self.vulGroup, False)
                        ship.health -= self.damage
                        self.kill()
                if self.rect.centery < 0:
                        self.kill()

class Bullet(Fire):
        def __init__(self, vulGroup, pos, bulletImage="bullets/player_bullet.png"):
                super().__init__(vulGroup)
                self.image = pygame.image.load(bulletImage)
                self.speed = 15
                self.damage = 10
        pass

class Torpedo(Fire):
        def __init__(self, vulGroup, pos, torpedoImage="bullets/player_torpedo.png"):
                super().__init__(vulGroup, pos)
                self.image = pygame.image.load(torpedoImage)
                self.speed = 5
                self.damage = 30
                self.mod = 2
                self.killVal = 100
                self.cut = (4, 2)
                self.bullet = False
        pass