import pygame

from pygame.locals import *
from SpriteGroups import *

class Fire(pygame.sprite.Sprite):
        def __init__(self, vulGroup, pos=(0, 0)):
                super().__init__()

                self.image = pygame.image.load("bullets/player_bullet.png")
                self.orgBullet = self.image
                self.rect = self.image.get_rect()

                self.rect.center = pos

                self.speed = 10
                self.damage = 0

                self.killVal = 50
                self.mod = 2
                self.cut = (16, 4)

                self.bullet = True
                self.vulGroup = vulGroup
                self.type = None

        def update(self):
                self.rect.centery -= self.speed

                if self.image.get_width() <= self.killVal:
                        self.kill()

                if self.rect.centery % self.mod == 0:

                        self.image = pygame.transform.scale(self.orgBullet, (self.image.get_width() - self.cut[0], self.image.get_height() - self.cut[1]))
                        if self.bullet:
                                self.rect.centerx += 4


                if pygame.sprite.spritecollideany(self, self.vulGroup):
                        if self.image.get_width() <= self.orgBullet.get_width() // 2:
                                ship = pygame.sprite.spritecollide(self, self.vulGroup, False)[-1]
                                ship.health -= self.damage
                                self.kill()
                if self.rect.centery < 0:
                        self.kill()

class EnemyFire(Fire):
        def __init__(self, vulGroup, window, pos=(0, 0), fireImage="bullets/enemy_bullet.png"):
                super().__init__(vulGroup, pos)

                self.orgBullet = pygame.image.load(fireImage)
                self.image = pygame.transform.smoothscale(self.orgBullet, (self.orgBullet.get_width()//10, self.orgBullet.get_height()//10))
                self.speed = 15
                self.damage = 10
                self.window = window
                self.killVal = 400
                self.type = "EnemyFire"

        def update(self):
                self.rect.centery += self.speed

                if self.image.get_width() >= self.killVal:
                        self.kill()

                if self.rect.centery % self.mod == 0:
                        self.image = pygame.transform.scale(self.orgBullet, (self.image.get_width() + self.cut[0], self.image.get_height() + self.cut[1]))
                        if self.bullet:
                                self.rect.centerx += 4


                if pygame.sprite.spritecollideany(self, self.vulGroup):
                        if self.image.get_width() >= self.orgBullet.get_width() // 2:
                                ship = pygame.sprite.spritecollide(self, self.vulGroup, False)[-1]
                                ship.health -= self.damage
                                self.kill()

                if pygame.sprite.spritecollideany(self, bulletGroup):
                        bullet = pygame.sprite.spritecollide(self, bulletGroup, False)[-1]
                        if bullet.type == "PlayerBullet":
                                bullet.remove(bulletGroup)
                                bullet.kill()
                                self.remove(bulletGroup)
                                self.kill()

                if self.rect.centery > self.window.get_height():
                        self.kill()

class Bullet(Fire):
        def __init__(self, vulGroup, pos, bulletImage="bullets/player_bullet.png"):
                super().__init__(vulGroup)
                self.image = pygame.image.load(bulletImage)
                self.speed = 15
                self.damage = 10
                self.type = "PlayerBullet"
        pass

class Torpedo(Fire):
        def __init__(self, vulGroup, pos, torpedoImage="bullets/player_torpedo.png"):
                super().__init__(vulGroup, pos)
                self.image = pygame.image.load(torpedoImage)
                self.orgBullet = self.image
                self.speed = 5
                self.damage = 30
                self.mod = 2
                self.cut = (4, 2)
                self.killVal = 100
                self.bullet = False
                self.type = "PlayerTorpedo"
        pass