import pygame
import windowClass
from pygame.locals import *

pygame.init()

screen = pygame.display.set_mode((1100, 800))
pygame.display.set_caption("Space Game")


FPS = 60
clock = pygame.time.Clock()

while True:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

        screen.fill((0, 0, 0))

        pygame.display.update()
        clock.tick(FPS)