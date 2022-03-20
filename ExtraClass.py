import pygame

from SpriteGroups import *
from pygame.locals import *

class Line(pygame.sprite.Sprite):
        def __init__(self, thickness, color, alpha, pos, mainWindow):
                super().__init__()

                self.image = pygame.Surface((mainWindow.get_width(), thickness))
                self.image.fill(color)
                self.image.set_alpha(alpha)

                self.rect = self.image.get_rect()
                self.rect.topleft = pos


def scanlineGen(thickness, mainWindow):
        for i in range(mainWindow.get_height()//thickness):
                tmpLine = Line(thickness, (0, 0, 0), 150, (0, i*thickness*2), mainWindow)
                scanlineGroup.add(tmpLine)