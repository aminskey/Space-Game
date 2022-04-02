import pygame
from pygame.locals import *

class Level():
        def __init__(self, displayScreen, image, song, objects):
                self.background = pygame.image.load(image)
                self.background = pygame.transform.scale(self.background, displayScreen.get_size())
                self.bgSong = song
                self.objects = objects