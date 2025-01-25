# imports
import pygame
from pygame.locals import *


class StaticWall(object):
    
    def __init__(self, topCorner: tuple[int, int], width: int, height: int):
        self.topCorner = [topCorner[0], topCorner[1]]
        self.width = width
        self.height = height
        self.center = [topCorner[0] + (width/2), topCorner[1] + (height/2)]
        self.color = (0, 0, 0)
        self.rect = pygame.Rect(self.topCorner[0], self.topCorner[1], self.width, self.height)
        self.static = True
        self.shape = "rectangle"

    def drawSelf(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, 1)


    def applyCollision(self, otherObject):
        pass


