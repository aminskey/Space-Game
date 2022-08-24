import pygame
import ShipClass
import TextClass
import random
import ExtraClass
import Powerups

from pygame.locals import *
from ShipClass import Player
from PublicVar import *
from Healthbar import Healthbar
from Asteroids import Asteroid
from LevelsClass import Level
from windowClass import Window
from time import sleep

pygame.init()

name = "Space Raiders"
subtitle = "Alpha 1.5.3"

screen = pygame.display.set_mode((1100, 800), FULLSCREEN | SCALED)
pygame.display.set_caption(name + " - " + subtitle)

load_screen = pygame.transform.scale(pygame.image.load("backgrounds/loading.png"), screen.get_size())

ExtraClass.scanlineGen(1, screen)

screen.blit(load_screen, (0, 0))
scanlineGroup.draw(screen)
pygame.display.update()


FPS = 60
clock = pygame.time.Clock()

levels = [
        Level(screen, 5, 2, 0.25, "Sky High", "backgrounds/bg-3.png", "songs/prototypes/bg-2.ogg", ["backgroundObjects/cloud-1.png", "backgroundObjects/cloud-2.png", "backgroundObjects/airship.png"], ["rocket"]),
        Level(screen, 5, 5, 3, "Ring War", "backgrounds/bg-2.png", "songs/prototypes/bg.ogg", ["backgroundObjects/asteroid-0.png", "backgroundObjects/planet.png", "backgroundObjects/ship-1.png"], ["interceptor", "bomber"]),
	Level(screen, 5, 5, 3, "Alien Planet", "backgrounds/alien_planet.png", "songs/prototypes/alien_planet.ogg", ["backgroundObjects/asteroid-0.png", "backgroundObjects/ship-1.png"], ["interceptor", "bomber", "rocket"]),
        Level(screen, 5, 2, 0.25, "Ocean Planet", "backgrounds/ocean_surface.png", "songs/prototypes/ocean.ogg", ["backgroundObjects/cloud-1.png", "backgroundObjects/cloud-2.png"], ["interceptor", "bomber", "rocket"]),
        Level(screen, 5, 5, 3, "Atmosphere", "backgrounds/earth.png", "songs/prototypes/orbit.ogg", ["backgroundObjects/asteroid-0.png", "backgroundObjects/ship-1.png"], ["interceptor", "rocket"]),
        Level(screen, 5, 5, 3, "Black hole", "backgrounds/black_hole.png", "songs/prototypes/black_hole.ogg", ["backgroundObjects/asteroid-0.png", "backgroundObjects/ship-1.png"], ["interceptor", "bomber", "rocket"]),
        Level(screen, 5, 5, 1, "Nebula", "backgrounds/nebula.png", "songs/prototypes/nebula.ogg", ["backgroundObjects/planet.png", "backgroundObjects/ship-1.png", "backgroundObjects/asteroid-0.png"], ["rocket"]),
        Level(screen, 5, 5, 1, "Wormhole", "backgrounds/wormhole.png", "songs/prototypes/wormhole.ogg", ["backgroundObjects/ship-1.png", "backgroundObjects/ship-0.png", "backgroundObjects/asteroid-0.png"], ["interceptor", "rocket"]),
        Level(screen, 5, 5, 3, "Pluto", "backgrounds/pluto.png", "songs/prototypes/pluto.ogg", ["backgroundObjects/asteroid-0.png", "backgroundObjects/planet.png", "backgroundObjects/ship-1.png"], ["interceptor", "bomber"]),
        Level(screen, 5, 5, 3, "Neptune", "backgrounds/neptune.png", "songs/prototypes/neptune.ogg", ["backgroundObjects/asteroid-0.png", "backgroundObjects/ship-1.png"], ["rocket", "bomber"])
]

player_ship_models = [
        "quake",
        "rocket",
        "hunter"
]

select_screen = ExtraClass.return_frames(screen, "backgrounds/levelSelect.gif")
parade_screen = ExtraClass.return_frames(screen, "backgrounds/new_highscore.gif")
parade_screen2 = ExtraClass.return_frames(screen, "backgrounds/new_highscore-2.gif")

highscore = 60

with open("files/rnd.txt") as f:
        lines = f.readlines()
        f.close()

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

        preview = Window((screen.get_width()//5, screen.get_height()//5))
        preview.rect.center = (screen.get_rect().centerx, screen.get_height()//3)

        prevMission = Window((preview.image.get_width() - 20, preview.image.get_height() - 20))
        nextMission = Window((preview.image.get_width() - 20, preview.image.get_height() - 20))

        prevMission.image.set_alpha(100)
        nextMission.image.set_alpha(100)

        prevMission.rect.centerx = preview.rect.midleft[0] - 50 - screen.get_width()//5
        nextMission.rect.centerx = preview.rect.midright[0] + 50 + screen.get_width()//5

        prevMission.rect.centery = nextMission.rect.centery = screen.get_height()//3

        dscWin = Window((screen.get_width(), screen.get_height()//3))
        dscWin.rect.bottomleft = (0, screen.get_height())


        dscbg = pygame.transform.scale(pygame.image.load("misc/window.png"), dscWin.image.get_size())

        levelFont = pygame.font.Font("fonts/pixelart.ttf", 50)
        prevFont = pygame.font.Font("fonts/pixelart.ttf", 40)
        header = pygame.font.Font("fonts/ka1.ttf", 100)
        description = pygame.font.Font("fonts/vga_437.ttf", 25)

        title = TextClass.Text("Select  Level", header, (100, 150, 100))
        title.rect.midtop = screen.get_rect().midtop

        title2 = TextClass.Text("Select   Ship", header, (100, 150, 100))
        title2.rect.midtop = screen.get_rect().midtop

        levelSelected = False

        mainLevel = None

        textLines = []
        global lines

        for item in lines:
                line = TextClass.Text(item, description, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
                textLines.append(line)

        textLines[0].rect.topleft = (dscWin.image.get_width() * 5//8 - 20, 10)

        messages = [
                TextClass.Text(" * Processing Ship....", description, (255, 255, 255)),
                TextClass.Text(" * Generating Enemies....", description, (255, 255, 255)),
                TextClass.Text(" * Generating bgSong....", description, (255, 255, 255)),
                TextClass.Text(" * Loading Ship with weapons....", description, (255, 255, 255)),
                TextClass.Text(" * Preparing Asteroids....", description, (255, 255, 255)),
                TextClass.Text(" * Your Game Is Now Ready....", description, (255, 255, 255))
        ]

        msgItr = 0
        gifItr = 0
        shipItr = 0

        while not levelSelected:
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
                                        mainLevel = list[itr]
                                        levelSelected = True
                                        break
                if itr < 0:
                        itr = len(list) - 1
                if itr > len(list) - 1:
                        itr = 0

                level = list[itr]

                prevLevel = list[itr - 1]
                if (itr + 1) > len(list) - 1:
                        nextLevel = list[0]
                else:
                        nextLevel = list[itr + 1]

                levelTitle = TextClass.Text(level.name, levelFont, (255, 255, 255))
                levelTitle.rect.midtop = preview.rect.midbottom

                prevTitle = TextClass.Text(prevLevel.name, prevFont, (255, 255, 255))
                prevTitle.rect.midtop = prevMission.rect.midbottom
                prevTitle.image.set_alpha(100)

                nextTitle = TextClass.Text(nextLevel.name, prevFont, (255, 255, 255))
                nextTitle.rect.midtop = nextMission.rect.midbottom
                nextTitle.image.set_alpha(100)

                tmptext = TextClass.Text(" * Current Level: " + level.name + ".....", description, (255, 255, 255))
                tmptext.rect.topleft = (10, 10)

                dscWin.image.blit(dscbg, (0, 0))
                dscWin.image.blit(tmptext.image, tmptext.rect)

                if msgItr > len(messages) - 1:
                        msgItr = 0

                messages[int(msgItr)].rect.topleft = tmptext.rect.bottomleft
                dscWin.image.blit(messages[int(msgItr)].image, messages[int(msgItr)].rect)

                textLines[0].rect.centery -= len(select_screen)//2

                for i in range(len(textLines)):
                        if i == 0:
                                continue
                        textLines[i].rect.topleft = textLines[i - 1].rect.bottomleft

                for item in textLines:
                        dscWin.image.blit(item.image, item.rect)

                currentBG = level.background
                currentBG = pygame.transform.scale(currentBG, preview.image.get_size())
                preview.image.blit(currentBG, (0, 0))

                prevBG = pygame.transform.scale(prevLevel.background, prevMission.image.get_size())
                nextBG = pygame.transform.scale(nextLevel.background, prevMission.image.get_size())

                prevMission.image.blit(prevBG, (0, 0))
                nextMission.image.blit(nextBG, (0, 0))

                if gifItr > len(select_screen) - 1:
                        gifItr = 0

                bg = select_screen[gifItr]

                screen.blit(bg, (0, 0))
                screen.blit(shade.image, shade.rect)
                screen.blit(prevMission.image, prevMission.rect)
                screen.blit(nextMission.image, nextMission.rect)
                screen.blit(preview.image, preview.rect)

                screen.blit(dscWin.image, dscWin.rect)
                screen.blit(levelTitle.image, levelTitle.rect)
                screen.blit(title.image, title.rect)
                screen.blit(prevTitle.image, prevTitle.rect)
                screen.blit(nextTitle.image, nextTitle.rect)

                scanlineGroup.draw(screen)

                pygame.display.update()
                clock.tick(30)

                gifItr += 1
                msgItr += 0.01

        while True:
                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                pygame.quit()
                                exit()
                        if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_LEFT:
                                        shipItr -= 1
                                        break
                                if event.key == pygame.K_RIGHT:
                                        shipItr += 1
                                        break
                                if event.key == pygame.K_RETURN:
                                        main(mainLevel, player_ship_models[shipItr])
                                        break

                if shipItr < 0:
                        shipItr = len(player_ship_models) - 1
                if shipItr > len(player_ship_models) - 1:
                        shipItr = 0

                currentShip = pygame.image.load("ships/player_ships/" + player_ship_models[shipItr] + "/" + player_ship_models[shipItr] + "-1.png")
                shipRect = currentShip.get_rect()
                shipRect.center = screen.get_rect().center

                prevShip = pygame.image.load("ships/player_ships/" + player_ship_models[shipItr - 1] + "/" + player_ship_models[shipItr - 1] + "-1.png")
                prevShip.set_alpha(100)

                prevRect = prevShip.get_rect()
                prevRect.midright = shipRect.midleft



                shipName = TextClass.Text(player_ship_models[shipItr], prevFont, (255, 255, 255))
                shipName.rect.midtop = shipRect.midbottom

                prevName = TextClass.Text(player_ship_models[shipItr - 1], prevFont, (255, 255, 255))
                prevName.image.set_alpha(100)
                prevName.rect.midtop = prevRect.midbottom

                if gifItr > len(select_screen) - 1:
                        gifItr = 0

                bg = select_screen[gifItr]

                screen.blit(bg, (0, 0))
                screen.blit(currentShip, shipRect)
                screen.blit(title2.image, title2.rect)
                screen.blit(shipName.image, shipName.rect)
                screen.blit(prevShip, prevRect)
                screen.blit(prevName.image, prevName.rect)

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
                main_sprite = asteroidGroups[random.randint(0, len(asteroidGroups) - 1)].sprites()[i]
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
def gameOver(playerScore):
        pygame.mixer.music.load("songs/prototypes/gameOver-1.ogg")
        gameOverFile = "misc/gameOver-1.png"

        pygame.mixer.music.play(-1)

        logo = pygame.image.load(gameOverFile)
        logoRect = logo.get_rect()
        logoRect.center = (screen.get_width() // 2, screen.get_height() // 2)
        alphaVal = 0

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

                                        if playerScore >= highscore:
                                                parade(playerScore)

                                        startScreen()
                                        exit()
                        break

                if alphaVal < 255:
                        alphaVal += 1

                logo.set_alpha(alphaVal)
                screen.blit(logo, logoRect)

                pygame.display.flip()
                clock.tick(30)

def parade(playerScore):

        if playerScore >= 1000:
                pygame.mixer.music.load("songs/prototypes/gameOver-2.ogg")
                anim=parade_screen
        else:
                pygame.mixer.music.load("songs/prototypes/gameOver-3.ogg")
                anim=parade_screen2

        color = (150, 150, 255)
        gameOverFile = "misc/gameOver-2.png"

        pygame.mixer.music.play(-1)

        logo = pygame.image.load(gameOverFile)
        logoRect = logo.get_rect()
        logoRect.center = (screen.get_width() // 2, screen.get_height() // 2)
        alphaVal = 0

        scoreFont = pygame.font.Font("fonts/pixelart.ttf", 50)

        scoreText = TextClass.Text("Score: " + str(playerScore), scoreFont, (255, 255, 255))
        recText = TextClass.Text("Highscore: " + str(highscore), scoreFont, (255, 255, 255))

        scoreText.rect.midtop = logoRect.midbottom
        recText.rect.midtop = scoreText.rect.midbottom

        index = 0

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
                screen.fill(color)
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

                index += 1
                if index >= len(anim) - 1:
                        index = 0

                bg = anim[index]
                bg.set_alpha(alphaVal*2)


                if alphaVal < 255:
                        alphaVal += 1

                logo.set_alpha(alphaVal)
                scoreText.image.set_alpha(alphaVal)
                recText.image.set_alpha(alphaVal)

                screen.blit(bg, (0, 0))
                screen.blit(logo, logoRect)
                screen.blit(scoreText.image, scoreText.rect)
                screen.blit(recText.image, recText.rect)

                scanlineGroup.draw(screen)

                pygame.display.flip()
                clock.tick(30)

def main(level, shipModel):

        pygame.mixer.music.stop()
        pygame.mixer.music.unload()

        pygame.mixer.music.load(level.bgSong)
        pygame.mixer.music.play(-1)

        p1 = Player(screen, shipModel)
        p1.rect.midbottom = (screen.get_rect().midbottom[0], screen.get_rect().midbottom[1] - 100)

        playersGroup.add(p1)

        p1HealthBar = Healthbar(p1)
        p1HealthBar.rect.bottomleft = (0, screen.get_height())

        p1HealthBar.add(healthbarGroup)

        playerDistance = 0

        font = pygame.font.Font("fonts/pixelart.ttf", 25)
        scoreFont = pygame.font.Font("fonts/pixelart.ttf", 50)

        playerScore = 0

        itr = 0
        global highscore

        while True:
                itr += 1

                scoreText1 = TextClass.Text(str(playerScore), scoreFont, (255, 255, 255))
                scoreText2 = TextClass.Text("Score: ", scoreFont, (255, 255, 255))

                hs1 = TextClass.Text("Highscore: ", scoreFont, (255, 255, 255))
                hs2 = TextClass.Text(str(highscore), scoreFont, (255, 255, 255))

                distanceText1 = TextClass.Text("Distance: ", scoreFont, (255, 255, 255))
                distanceText2 = TextClass.Text(str(playerDistance), scoreFont, (255, 255, 255))

                scoreText1.rect.bottomright = (screen.get_width(), screen.get_height())
                scoreText2.rect.midright = scoreText1.rect.midleft

                hs1.rect.bottomright = scoreText2.rect.topright
                hs2.rect.bottomright = scoreText1.rect.topright

                distanceText1.rect.topright = (screen.get_width()//2, 0)
                distanceText2.rect.midleft = distanceText1.rect.midright

                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                pygame.quit()
                                exit()
                if playerScore >= highscore:
                        highscore = playerScore


                if itr % 50 == 0:
                        tmpEnemy = ShipClass.EnemyShip(screen, model=level.enemyModels[random.randint(0, len(level.enemyModels) - 1)])
                        tmpEnemy.rect.center = (random.randint(tmpEnemy.image.get_width(), screen.get_width() - tmpEnemy.image.get_width()), random.randint(screen.get_height()//4, screen.get_height()//2))
                        enemyGroup.add(tmpEnemy)

                if itr % 25:
                        speed = 0
                        img = level.objects[0]
                        if len(asteroidsGroup.sprites()) % 10 == 0:
                                img = level.objects[random.randint(1, len(level.objects) - 1)]
                                speed = random.randint(-10, 10)

                        tmpAst = Asteroid(screen, img, level.maxAsteroidSize)
                        tmpAst.speed = speed
                        tmpAst.direction = random.randint(-2, 2)
                        tmpAst.rect.center = (random.randint(tmpAst.image.get_width(), screen.get_width() - tmpAst.image.get_width()), random.randint(0, screen.get_height()//2))
                        asteroidsGroup.add(tmpAst)

                if playerDistance % 1000 == 0 and playerDistance != 0:
                        pUp = Powerups.OneUp(screen)
                        pUp.rect.center = (
                                random.randint(pUp.image.get_width(), screen.get_width() - pUp.image.get_width()),
                                random.randint(0, screen.get_height() // 2)
                        )
                        powerUpGroup.add(pUp)

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

                        gameOver(playerScore)

                playerDistance += asteroidsGroup.sprites()[-1].add

                screen.blit(level.background, (0, 0))

                enemyGroup.update()
                playersGroup.update(10, enemyGroup)
                bulletGroup.update()
                healthbarGroup.update()
                asteroidsGroup.update()
                powerUpGroup.update()

                p1HealthPrcnt = TextClass.Text(str(p1.health) + '%', font, (255, 255, 255))
                p1HealthPrcnt.rect.center = p1HealthBar.rect.center

                asteroidsGroup.draw(screen)
                powerUpGroup.draw(screen)
                enemyGroup.draw(screen)
                bulletGroup.draw(screen)
                playersGroup.draw(screen)
                healthbarGroup.draw(screen)

                screen.blit(p1HealthPrcnt.image, p1HealthPrcnt.rect)
                screen.blit(scoreText1.image, scoreText1.rect)
                screen.blit(scoreText2.image, scoreText2.rect)

                screen.blit(hs1.image, hs1.rect)
                screen.blit(hs2.image, hs2.rect)

                screen.blit(distanceText1.image, distanceText1.rect)
                screen.blit(distanceText2.image, distanceText2.rect)
                scanlineGroup.draw(screen)

                pygame.display.update()
                clock.tick(FPS)

startScreen()
