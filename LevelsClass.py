import pygame
from pygame.locals import *

class Level():
        def __init__(self, displayScreen, maxEnemies, maxAsteroids, maxAsteroidSize, name, image, song, objects, enemyModels):
                self.background = pygame.image.load(image)
                self.background = pygame.transform.scale(self.background, displayScreen.get_size())
                self.bgSong = song
                self.objects = objects
                self.enemyModels = enemyModels
                self.maxEnemies = maxEnemies
                self.maxAsteroids = maxAsteroids
                self.name = name
                self.maxAsteroidSize = maxAsteroidSize