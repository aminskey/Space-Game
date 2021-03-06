import pygame
import cv2

from PublicVar import *
from pygame.locals import *

class Asteroid(pygame.sprite.Sprite):
        def __init__(self, window, img="backgroundObjects/asteroid-0.png", pos=(0, 0)):
                super().__init__()

                self.image = pygame.image.load(img)
                self.rect = self.image.get_rect()

                self.rect.center = pos
                self.speed = 2
                self.window = window
        def update(self):

                self.rect.centerx += self.speed

                if self.rect.midleft[0] > self.window.get_width():
                        self.rect.midright = (0, self.rect.midleft[1])
                if self.rect.midright[0] < 0:
                        self.rect.midleft = (self.window.get_width(), self.rect.centery)


class Line(pygame.sprite.Sprite):
        def __init__(self, thickness, color, alpha, pos, mainWindow):
                super().__init__()

                self.image = pygame.Surface((mainWindow.get_width(), thickness))
                self.image.fill(color)
                self.image.set_alpha(alpha)

                self.rect = self.image.get_rect()
                self.rect.topleft = pos

def return_frames(window, gif):
        video = cv2.VideoCapture(gif)
        dimensions = video.read()[1].shape[1::-1]

        frames = []

        ret = True
        while ret:
                ret, frame = video.read()

                if not ret:
                        break

                img = pygame.image.frombuffer(frame, dimensions, "BGR")
                img = pygame.transform.scale(img, window.get_size())

                frames.append(img)
        return frames



def scanlineGen(thickness, mainWindow):
        for i in range(mainWindow.get_height()//thickness):
                tmpLine = Line(thickness, (0, 0, 0), 150, (0, i*thickness*2), mainWindow)
                scanlineGroup.add(tmpLine)