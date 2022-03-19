import pygame
from pygame.locals import *

class Text(pygame.sprite.Sprite):
        def __init__(self, msg, script, color=(0, 0, 0), pos=(0, 0)):
                super().__init__()
                self.image = script.render(msg, None, color)

                self.rect = self.image.get_rect()
                self.rect.center = pos