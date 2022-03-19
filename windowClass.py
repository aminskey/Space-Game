import pygame
from pygame.locals import *

class Window(pygame.sprite.Sprite):
        def __init__(self, size, pos=(0, 0)):
                super().__init__()
                self.image = pygame.Surface(size)

                self.rect = self.image.get_rect()
                self.rect.center = pos