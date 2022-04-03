import pygame

import ShipClass
import TextClass
import random
import ExtraClass

from pygame.locals import *
from ShipClass import Player
from PublicVar import *
from Healthbar import Healthbar
from Asteroids import Asteroid
from LevelsClass import Level
from windowClass import Window

pygame.init()

name = "Space Raiders"
subtitle = "Alpha 1.0"

screen = pygame.display.set_mode((1100, 800))
pygame.display.set_caption(name + " - " + subtitle)

FPS = 60
clock = pygame.time.Clock()

ExtraClass.scanlineGen(1, screen)

levels = [
        Level(screen, 5, 3, 1, "Sky High", "backgrounds/bg-3.png", "songs/prototypes/bg-2.ogg", ["backgroundObjects/cloud-1.png", "backgroundObjects/sky_dash.png", "backgroundObjects/sky_dash.png"], ["interceptor", "bomber"]),
        Level(screen, 5, 5, 3, "Ring War", "backgrounds/bg-2.png", "songs/prototypes/bg.ogg", ["backgroundObjects/asteroid-0.png", "backgroundObjects/planet.png", "backgroundObjects/ship-1.png"], ["interceptor", "bomber"])
]

select_screen = ExtraClass.return_frames(screen, "backgrounds/levelSelect.gif")

def levelSelect(list):

        for item in textGroup.sprites():
                item.remove(textGroup)
                item.kill()

        pygame.mixer.music.load("songs/prototypes/levelselect.ogg")
        pygame.mixer.music.play(-1)

        shade = Window(screen.get_size())
        shade.image.fill((0, 0, 0))
        shade.image.set_alpha(150)

        itr = len(list)//2 - 1

        gifItr = 0

        preview = Window((screen.get_width()//5, screen.get_height()//5))
        preview.rect.center = (screen.get_rect().centerx, screen.get_height()//3)

        dscWin = Window ((screen.get_width(), screen.get_height()//3), image="misc/window.png")
        dscWin.rect.bottomleft = (0, screen.get_height())

        levelFont = pygame.font.Font("fonts/pixelart.ttf", 50)
        header = pygame.font.Font("fonts/segaArt.ttf", 100)
        description = pygame.font.Font("fonts/vga_437.ttf", 25)

        title = TextClass.Text("Select  Level", header, (100, 150, 100))
        title.rect.midtop = screen.get_rect().midtop

        tmptext = TextClass.Text(" * No Description.....", description, (255, 255, 255))
        tmptext2 = TextClass.Text(" * More To Come......", description, (255, 255, 255))
        cursor = TextClass.Text("A", description, (255, 255, 255))

        tmptext.rect.topleft = (10, 10)
        tmptext2.rect.topleft = tmptext.rect.bottomleft

        cursor.rect.midleft = tmptext2.rect.midright

        cursor.image.fill((255, 255, 255))

        dscWin.image.blit(tmptext.image, tmptext.rect)
        dscWin.image.blit(tmptext2.image, tmptext2.rect)

        cursorItr = 0
        cursorOn = True
        values = [True, False]
        i = 0

        while True:
                cursorItr += 1
                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                pygame.quit()
                                exit()
                        if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_LEFT:
                                        itr -= 1
                                        break
                                if event.key == pygame.K_RIGHT:
                                        itr += 1
                                        break
                                if event.key == pygame.K_RETURN:
                                        main(list[itr])
                                        break
                if itr < 0:
                        itr = len(list) - 1
                if itr > len(list) - 1:
                        itr = 0

                level = list[itr]

                levelTitle = TextClass.Text(level.name, levelFont, (255, 255, 255))
                levelTitle.rect.midtop = preview.rect.midbottom

                currentBG = level.background
                currentBG = pygame.transform.scale(currentBG, preview.image.get_size())
                preview.image.blit(currentBG, (0, 0))

                if gifItr > len(select_screen) - 1:
                        gifItr = 0

                if cursorItr % 5 == 0:
                        i += 1
                if i > len(values) - 1:
                        i = 0

                if cursorOn:
                        cursor.image.set_alpha(255)
                else:
                        cursor.image.set_alpha(0)


                bg = select_screen[gifItr]

                dscWin.image.blit(cursor.image, cursor.rect)

                screen.blit(bg, (0, 0))
                screen.blit(shade.image, shade.rect)
                screen.blit(preview.image, preview.rect)
                screen.blit(dscWin.image, dscWin.rect)
                screen.blit(levelTitle.image, levelTitle.rect)
                screen.blit(title.image, title.rect)

                scanlineGroup.draw(screen)

                pygame.display.update()
                clock.tick(30)

                gifItr += 1

def startScreen():
        pygame.mixer.music.load("songs/prototypes/startups/startup.ogg")
        pygame.mixer.music.play(-1)

        asteroidsGroup1 = pygame.sprite.Group()
        asteroidsGroup2 = pygame.sprite.Group()

        for i in range(10):
                tmpAsteroid = ExtraClass.Asteroid(screen)
                tmpAsteroid.rect.center = (random.randint(0, screen.get_width()), random.randint(0, screen.get_height()))
                tmpAsteroid.image = pygame.transform.scale(tmpAsteroid.image, (tmpAsteroid.image.get_width() - 30, tmpAsteroid.image.get_height() - 30))

                tmpAsteroid.speed = random.randint(-3, 2)

                if pygame.sprite.spritecollideany(tmpAsteroid, asteroidsGroup1):
                        tmpAsteroid.kill()
                else:
                        tmpAsteroid.add(asteroidsGroup1)

        for i in range(10):
                tmpAsteroid = ExtraClass.Asteroid(screen)
                tmpAsteroid.rect.center = (random.randint(0, screen.get_width()), random.randint(0, screen.get_height()))
                tmpAsteroid.speed = random.randint(2, 4)

                if pygame.sprite.spritecollideany(tmpAsteroid, asteroidsGroup1):
                        tmpAsteroid.kill()
                else:
                        tmpAsteroid.add(asteroidsGroup2)


        asteroidGroups = [asteroidsGroup1, asteroidsGroup2]

        for i in range(5):
                main_sprite = asteroidGroups[random.randint(0, 1)].sprites()[i]
                main_sprite.speed = random.randint(1, 2)
                pos = main_sprite.rect.center

                main_sprite.image = pygame.image.load("backgroundObjects/ship-" + str(random.randint(0, 1)) + ".png")
                main_sprite.rect = main_sprite.image.get_rect()

                main_sprite.rect.center = pos


        bg = pygame.image.load("backgrounds/bg.png")
        bg = pygame.transform.scale(bg, screen.get_size())

        planet = pygame.image.load("backgroundObjects/planet.png")
        planetRect = planet.get_rect()
        planetRect.center = (screen.get_width()//3, screen.get_height()//2)

        header = pygame.font.Font("fonts/pixelart.ttf", 75)
        subFont = pygame.font.Font("fonts/pixelart.ttf", 30)
        option = pygame.font.Font("fonts/pixelart.ttf", 40)



        title = TextClass.Text(name, header, (255, 255, 255), (screen.get_width()//2, screen.get_height()//3))
        sub = TextClass.Text(subtitle, subFont, (255, 255, 255), (0, 0))
        sub.rect.midtop = title.rect.midbottom

        start = TextClass.Text("start", option, (255, 255, 255), (screen.get_width()//2, screen.get_height()//2 + 30))
        indev = TextClass.Text("Indevs", option, (255, 255, 255))
        quit = TextClass.Text("quit", option, (255, 255, 255))
        cursor = TextClass.Text(">", option, (50, 255, 50))

        indev.rect.midtop = start.rect.midbottom
        quit.rect.midtop = indev.rect.midbottom

        textGroup.add(start)
        textGroup.add(quit)
        textGroup.add(cursor)
        textGroup.add(title)
        textGroup.add(sub)
        textGroup.add(indev)

        itr = 0

        options = [start, indev, quit]

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
                                                levelSelect(levels)
                                                break
                                        if options[itr] == indev:
                                                levelSelect(levels)
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

        pygame.mixer.music.load("songs/prototypes/gameOver.ogg")
        pygame.mixer.music.play(-1)

        for item in healthbarGroup.sprites():
                item.remove(healthbarGroup)
                item.kill()

        for item in playersGroup.sprites():
                item.remove(playersGroup)
                item.kill()

        for item in enemyGroup.sprites():
                item.remove(enemyGroup)
                item.kill()

        for item in asteroidsGroup.sprites():
                item.remove(asteroidsGroup)
                item.kill()

        while True:
                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                pygame.quit()
                                exit()
                        if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_RETURN:
                                        pygame.mixer.music.stop()
                                        pygame.mixer.music.unload()

                                        startScreen()
                                        exit()
                        break

                if alphaVal < 255:
                        alphaVal += 1

                logo.set_alpha(alphaVal)

                screen.blit(logo, logoRect)

                pygame.display.flip()
                clock.tick(30)


def main(level):

        pygame.mixer.music.stop()
        pygame.mixer.music.unload()

        pygame.mixer.music.load(level.bgSong)
        pygame.mixer.music.play(-1)

        p1 = Player(screen)
        p1.rect.midbottom = (screen.get_rect().midbottom[0], screen.get_rect().midbottom[1] - 100)

        playersGroup.add(p1)

        p1HealthBar = Healthbar(p1)
        p1HealthBar.rect.bottomleft = (0, screen.get_height())

        p1HealthBar.add(healthbarGroup)

        font = pygame.font.Font("fonts/pixelart.ttf", 25)
        scoreFont = pygame.font.Font("fonts/pixelart.ttf", 50)

        playerScore = 0

        itr = 0

        while True:
                itr += 1

                scoreText1 = TextClass.Text(str(playerScore), scoreFont, (255, 255, 255))
                scoreText2 = TextClass.Text("Score:", scoreFont, (255, 255, 255))

                scoreText1.rect.bottomright = (screen.get_width(), screen.get_height())
                scoreText2.rect.midright = scoreText1.rect.midleft

                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                pygame.quit()
                                exit()

                if itr % 50 == 0:
                        tmpEnemy = ShipClass.EnemyShip(screen, model=level.enemyModels[random.randint(0, 1)])
                        tmpEnemy.rect.center = (random.randint(tmpEnemy.image.get_width(), screen.get_width() - tmpEnemy.image.get_width()), random.randint(screen.get_height()//4, screen.get_height()//2))
                        enemyGroup.add(tmpEnemy)

                if itr % 25:
                        speed = 0
                        img = level.objects[0]
                        if len(asteroidsGroup.sprites()) % 10 == 0:
                                img = level.objects[random.randint(1, 2)]
                                speed = random.randint(1, 3)

                        tmpAst = Asteroid(screen, img, level.maxAsteroidSize)
                        tmpAst.speed = speed
                        tmpAst.direction = random.randint(-2, 2)
                        tmpAst.rect.center = (random.randint(tmpAst.image.get_width(), screen.get_width() - tmpAst.image.get_width()), random.randint(0, screen.get_height()//2))
                        asteroidsGroup.add(tmpAst)

                if len(enemyGroup.sprites()) > level.maxEnemies:
                        sprite = enemyGroup.sprites()[-1]
                        sprite.remove(enemyGroup)
                        sprite.kill()

                if len(asteroidsGroup.sprites()) > level.maxAsteroids:
                        sprite = asteroidsGroup.sprites()[-1]
                        sprite.remove(asteroidsGroup)
                        sprite.kill()

                for enemy in enemyGroup.sprites():
                        if enemy.health <= 0:
                                playerScore += enemy.scorePoints


                if p1.health <= 0:
                        pygame.mixer.music.stop()
                        pygame.mixer.music.unload()

                        gameOver()

                screen.blit(level.background, (0, 0))

                enemyGroup.update()
                playersGroup.update(10, enemyGroup)
                bulletGroup.update()
                healthbarGroup.update()
                asteroidsGroup.update()

                p1HealthPrcnt = TextClass.Text(str(p1.health) + '%', font, (255, 255, 255))
                p1HealthPrcnt.rect.center = p1HealthBar.rect.center

                asteroidsGroup.draw(screen)
                enemyGroup.draw(screen)
                bulletGroup.draw(screen)
                playersGroup.draw(screen)
                healthbarGroup.draw(screen)

                screen.blit(p1HealthPrcnt.image, p1HealthPrcnt.rect)
                screen.blit(scoreText1.image, scoreText1.rect)
                screen.blit(scoreText2.image, scoreText2.rect)

                scanlineGroup.draw(screen)

                pygame.display.update()
                clock.tick(FPS)

startScreen()