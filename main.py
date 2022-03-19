import pygame
import TextClass
from pygame.locals import *

pygame.init()

name = "Space Game"

screen = pygame.display.set_mode((1100, 800))
pygame.display.set_caption(name)

FPS = 60
clock = pygame.time.Clock()

textGroup = pygame.sprite.Group()
playersGroup = pygame.sprite.Group()

def startScreen():
        bg = pygame.image.load("backgrounds/bg.png")
        bg = pygame.transform.scale(bg, screen.get_size())

        header = pygame.font.Font("fonts/pixelart.ttf", 75)
        option = pygame.font.Font("fonts/pixelart.ttf", 40)


        title = TextClass.Text(name, header, (255, 255, 255), (screen.get_width()//2, screen.get_height()//3))

        start = TextClass.Text("start", option, (255, 255, 255), (screen.get_width()//2, screen.get_height()//2 + 30))
        quit = TextClass.Text("quit", option, (255, 255, 255))
        cursor = TextClass.Text(">", option, (50, 255, 50))

        quit.rect.midtop = start.rect.midbottom

        textGroup.add(start)
        textGroup.add(quit)
        textGroup.add(cursor)
        textGroup.add(title)

        itr = 0

        options = [start, quit]

        while True:
                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                pygame.quit()
                                exit()
                        if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_DOWN:
                                        itr += 1
                                if event.key == pygame.K_UP:
                                        itr -= 1
                                if event.key == pygame.K_RETURN:
                                        if options[itr] == start:
                                                main()
                                                break
                                        if options[itr] == quit:
                                                exit()

                if itr < 0:
                        itr = len(options) - 1
                if itr > len(options) - 1:
                        itr = 0

                cursor.rect.midright = options[itr].rect.midleft

                screen.blit(bg, (0, 0))
                textGroup.draw(screen)

                pygame.display.update()
                clock.tick(FPS)

def main():
        while True:
                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                pygame.quit()
                                exit()

                screen.fill((0, 0, 0))

                pygame.display.update()
                clock.tick(FPS)

startScreen()