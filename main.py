import pygame

import ShipClass
import TextClass
import random
import ExtraClass

from pygame.locals import *
from ShipClass import Player
from SpriteGroups import *

pygame.init()

name = "Space Raiders"

screen = pygame.display.set_mode((1100, 800))
pygame.display.set_caption(name)

FPS = 60
clock = pygame.time.Clock()

ExtraClass.scanlineGen(1, screen)

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
                                        for item in textGroup:
                                                item.remove(textGroup)
                                                item.kill()

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
                scanlineGroup.draw(screen)

                pygame.display.update()
                clock.tick(FPS)

def main():

        bg = pygame.image.load("backgrounds/mainbg.png")
        bg = pygame.transform.scale(bg, screen.get_size())

        p1 = Player(screen)
        p1.rect.midbottom = (screen.get_rect().midbottom[0], screen.get_rect().midbottom[1] - 50)

        playersGroup.add(p1)

        itr = 0

        while True:
                itr += 1
                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                pygame.quit()
                                exit()

                if itr % 50 == 0:
                        tmpEnemy = ShipClass.EnemyShip(screen)
                        tmpEnemy.rect.center = (random.randint(0, screen.get_width()), random.randint(screen.get_height()//4, screen.get_height() * 3//4))
                        enemyGroup.add(tmpEnemy)

                if len(enemyGroup.sprites()) > 30:
                        sprite = enemyGroup.sprites()[1]
                        sprite.remove(enemyGroup)
                        sprite.kill()

                if p1.health <= 0:
                        startScreen()

                screen.blit(bg, (0, 0))

                enemyGroup.update()
                playersGroup.update(10, enemyGroup)
                bulletGroup.update()


                enemyGroup.draw(screen)
                bulletGroup.draw(screen)
                playersGroup.draw(screen)
                scanlineGroup.draw(screen)

                pygame.display.update()
                clock.tick(FPS)

startScreen()