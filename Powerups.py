import pygame

from pygame.locals import *
from Asteroids import Asteroid
from PublicVar import *

class OneUp(Asteroid):
        def __init__(self, mainWindow):
                super().__init__(mainWindow, "powerups/1UP.png", 3)


        def collected(self):
                tmpSound = pygame.mixer.Sound("sounds/powerup.mp3")
                tmpSound.set_volume(0.5)
                tmpSound.play()

                self.remove(powerUpGroup)
                self.kill()

        def update(self):
                if pygame.sprite.spritecollideany(self, bulletGroup):
                        bullet = pygame.sprite.spritecollide(self, bulletGroup, False)[-1]
                        if bullet.type == "PlayerBullet" or bullet.type == "PlayerTorpedo":
                                bullet.sender.health = 100
                                self.collected()

                super().update()