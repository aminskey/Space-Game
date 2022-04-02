import pygame

from pygame.locals import *
from TextClass import Text
class Healthbar(pygame.sprite.Sprite):
        def __init__(self, player):
                super().__init__()

                self.states = [
                        pygame.image.load("healthbars/playerHealthbar/bar-0.png"),
                        pygame.image.load("healthbars/playerHealthbar/bar-1.png"),
                        pygame.image.load("healthbars/playerHealthbar/bar-2.png"),
                        pygame.image.load("healthbars/playerHealthbar/bar-3.png")
                ]

                self.image = self.states[0]
                self.rect = self.image.get_rect()
                self.player = player

        def update(self):


                if 100 >= self.player.health > 70:
                        self.image = self.states[0]
                if 70 >= self.player.health > 40:
                        self.image = self.states[1]
                if 40 >= self.player.health > 10:
                        self.image = self.states[2]
                if 10 >= self.player.health > 0:
                        self.image = self.states[3]

