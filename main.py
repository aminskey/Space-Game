import pygame

import ShipClass
import TextClass
import random
import ExtraClass

from pygame.locals import *
from ShipClass import Player
from SpriteGroups import *
from Healthbar import Healthbar

pygame.init()

name = "Space Raiders"

screen = pygame.display.set_mode((1100, 800))
pygame.display.set_caption(name)

FPS = 60
clock = pygame.time.Clock()

ExtraClass.scanlineGen(1, screen)

def startScreen():
        pygame.mixer.music.load("songs/prototypes/startups/startup.ogg")
        pygame.mixer.music.play(-1)

        asteroidsGroup1 = pygame.sprite.Group()
        asteroidsGroup2 = pygame.sprite.Group()

        for i in range(10):
                tmpAsteroid = ExtraClass.Asteroid(screen)
                tmpAsteroid.rect.center = (random.randint(0, screen.get_width()), random.randint(0, screen.get_height()))

                if pygame.sprite.spritecollideany(tmpAsteroid, asteroidsGroup1):
                        tmpAsteroid.kill()
                else:
                        tmpAsteroid.add(asteroidsGroup1)

        for i in range(10):
                tmpAsteroid = ExtraClass.Asteroid(screen)
                tmpAsteroid.rect.center = (random.randint(0, screen.get_width()), random.randint(0, screen.get_height()))

                if pygame.sprite.spritecollideany(tmpAsteroid, asteroidsGroup1):
                        tmpAsteroid.kill()
                else:
                        tmpAsteroid.add(asteroidsGroup2)


        bg = pygame.image.load("backgrounds/bg.png")
        bg = pygame.transform.scale(bg, screen.get_size())

        planet = pygame.image.load("backgroundObjects/planet.png")
        planetRect = planet.get_rect()
        planetRect.center = (screen.get_width()//3, screen.get_height()//2)

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
                                                pygame.mixer.music.stop()
                                                pygame.mixer.music.unload()

                                                pygame.mixer.music.load("songs/prototypes/bg.ogg")
                                                pygame.mixer.music.play(-1, 0.5)

                                                main()
                                                break
                                        if options[itr] == quit:
                                                exit()

                if itr < 0:
                        itr = len(options) - 1
                if itr > len(options) - 1:
                        itr = 0

                cursor.rect.midright = options[itr].rect.midleft

                asteroidsGroup2.update()
                asteroidsGroup1.update()

                screen.blit(bg, (0, 0))

                asteroidsGroup1.draw(screen)
                screen.blit(planet, planetRect)
                asteroidsGroup2.draw(screen)

                textGroup.draw(screen)
                scanlineGroup.draw(screen)

                pygame.display.update()
                clock.tick(FPS)
def gameOver():

        logo = pygame.image.load("misc/gameOver.png")
        logoRect = logo.get_rect()
        logoRect.center = (screen.get_width()//2, screen.get_height()//2)
        alphaVal = 0

        for item in healthbarGroup:
                item.remove(healthbarGroup)
                item.kill()

        for item in playersGroup:
                item.remove(playersGroup)
                item.kill()

        for item in enemyGroup:
                item.remove(enemyGroup)
                item.kill()

        while True:
                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                pygame.quit()
                                exit()
                        if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_RETURN:
                                        startScreen()
                                        exit()
                        break

                if alphaVal < 255:
                        alphaVal += 1

                logo.set_alpha(alphaVal)

                screen.blit(logo, logoRect)

                pygame.display.flip()
                clock.tick(30)


def main():

        bg = pygame.image.load("backgrounds/mainbg.png")
        bg = pygame.transform.scale(bg, screen.get_size())

        p1 = Player(screen)
        p1.rect.midbottom = (screen.get_rect().midbottom[0], screen.get_rect().midbottom[1] - 100)

        playersGroup.add(p1)

        p1HealthBar = Healthbar(p1)
        p1HealthBar.rect.bottomleft = (0, screen.get_height())

        p1HealthBar.add(healthbarGroup)

        itr = 0

        while True:
                itr += 1
                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                pygame.quit()
                                exit()

                if itr % 50 == 0:
                        tmpEnemy = ShipClass.EnemyShip(screen)
                        tmpEnemy.rect.center = (random.randint(tmpEnemy.image.get_width(), screen.get_width() - tmpEnemy.image.get_width()), random.randint(screen.get_height()//4, screen.get_height() * 3//4))
                        enemyGroup.add(tmpEnemy)

                if len(enemyGroup.sprites()) > 30:
                        sprite = enemyGroup.sprites()[1]
                        sprite.remove(enemyGroup)
                        sprite.kill()

                if p1.health <= 0:
                        pygame.mixer.music.stop()
                        pygame.mixer.music.unload()

                        gameOver()

                screen.blit(bg, (0, 0))

                enemyGroup.update()
                playersGroup.update(10, enemyGroup)
                bulletGroup.update()
                healthbarGroup.update()


                enemyGroup.draw(screen)
                bulletGroup.draw(screen)
                playersGroup.draw(screen)
                healthbarGroup.draw(screen)
                scanlineGroup.draw(screen)

                pygame.display.update()
                clock.tick(FPS)

startScreen()