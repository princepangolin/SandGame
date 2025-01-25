# imports
import pygame
from pygame.locals import *


class SandParticle(object):
    r = 255
    rFlag = 0
    g = 0
    gFlag = 1
    b = 0
    bFlag = 0

    def __init__(self, xPos, yPos, mass = 1):
        self.position = [xPos, yPos]
        self.velocity = [0, 0]
        self.force = [0, 0]
        self.color = (SandParticle.r, SandParticle.g, SandParticle.b)
        self.radius = 3
        self.mass = mass
        self.static = False
        self.shape = "circle"

        SandParticle.r += 5 * SandParticle.rFlag
        SandParticle.g += 5 * SandParticle.gFlag
        SandParticle.b += 5 * SandParticle.bFlag

        if SandParticle.r == 255 and SandParticle.g == 255 and SandParticle.b == 0:
            SandParticle.rFlag = -1
            SandParticle.gFlag = 0
        elif SandParticle.r == 0 and SandParticle.g == 255 and SandParticle.b == 0:
            SandParticle.rFlag = 0
            SandParticle.bFlag = 1
        elif SandParticle.g == 255 and SandParticle.b == 255 and SandParticle.r == 0:
            SandParticle.gFlag = -1
            SandParticle.bFlag = 0
        elif SandParticle.g == 0 and SandParticle.b == 255 and SandParticle.r == 0:
            SandParticle.gFlag = 0
            SandParticle.rFlag = 1
        elif SandParticle.b == 255 and SandParticle.r == 255 and SandParticle.g == 0:
            SandParticle.bFlag = -1
            SandParticle.rFlag = 0
        elif SandParticle.b == 0 and SandParticle.r == 255 and SandParticle.g == 0:
            SandParticle.bFlag = 0
            SandParticle.gFlag = 1
            

    def updateForce(self, force):
        self.force[0] += force[0]
        self.force[1] += force[1]


    def updateVel(self, dt):
        # F = m*a -> a = F/m
        # Need to remember higher numbers are down/right.
        a = [self.force[0]/self.mass, self.force[1]/self.mass]
        self.velocity[0] += a[0] * dt
        self.velocity[1] += a[1] * dt


    def checkCollision(self, otherObject) -> bool:


        return False


    def updatePos(self, dt):
        self.position[0] += self.velocity[0] * dt
        self.position[1] += self.velocity[1] * dt

    def drawSelf(self, surface):
        pygame.draw.circle(surface, self.color, (self.position[0], self.position[1]), self.radius, 0)



