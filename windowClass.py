import pygame
from pygame.locals import *

class Window(pygame.sprite.Sprite):
        def __init__(self, size, pos=(0, 0), image=None):
                super().__init__()
                if not image:
                        self.image = pygame.Surface(size)
                else:
                        self.image = pygame.transform.scale(pygame.image.load(image), size)

                self.rect = self.image.get_rect()
                self.rect.topleft = pos