# imports
import pygame
from pygame.locals import *
import math
import random


class SandParticle(object):
    r = 255
    rFlag = 0
    g = 0
    gFlag = 1
    b = 0
    bFlag = 0

    def __init__(self, xPos, yPos, initialSpace, mass = 1):
        self.position = [xPos, yPos]
        self.velocity = [0, 0]
        self.velocity[0] = random.uniform(-20.0, 20.0)
        self.velocity[1] = random.uniform(0.0, 5.0)
        self.force = [0, 0]
        self.color = (SandParticle.r, SandParticle.g, SandParticle.b)
        self.radius = 3
        self.mass = mass
        self.spaces = []
        self.spaces.append(initialSpace)
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

    # Base formula: F_d = 0.5 * ρ * v^2 * C_d * A
    # Look into this later, for now just gonna set a max speed
    #def applyAirResistance(self, density, drag):
    #    velMag = math.sqrt( (self.velocity[0]**2) + (self.velocity(1)**2) )
    #    force = -(0.5) * density * (velMag**2) * drag * (math.pi * (self.radius**2))
    

    def updateVel(self, dt):
        # F = m*a -> a = F/m
        # Need to remember higher numbers are down/right.
        a = [self.force[0]/self.mass, self.force[1]/self.mass]
        xVel = self.velocity[0] + (a[0] * dt)
        yVel = self.velocity[1] + (a[1] * dt)

        velCap = 150.0
        velMag = math.sqrt( (xVel**2) + (yVel**2) )
        
        ratio = 1
        if velMag > velCap:
            ratio = velCap/velMag

        self.velocity = [xVel*ratio, yVel*ratio]


    def updatePos(self, dt):
        self.position[0] += self.velocity[0] * dt
        self.position[1] += self.velocity[1] * dt


    def checkCollision(self, otherObject) -> bool:
        # Need to add circle collision
        if otherObject.shape == "circle":
            pass

        # At some point I'll have to update this so that the rectangle is not assumed to be x-y aligned
        elif otherObject.shape == "rectangle":
            xTest = self.position[0]
            yTest = self.position[1]

            if xTest < otherObject.topCorner[0]:
                xTest = otherObject.topCorner[0]
            if xTest > otherObject.topCorner[0] + otherObject.width:
                xTest = otherObject.topCorner[0] + otherObject.width
                
            if yTest < otherObject.topCorner[1]:
                yTest = otherObject.topCorner[1]
            if yTest > otherObject.topCorner[1] + otherObject.height:
                yTest = otherObject.topCorner[1] + otherObject.height

            xDist = self.position[0] - xTest
            yDist = self.position[1] - yTest

            dist = math.sqrt((xDist)**2 + (yDist)**2)

            if dist <= self.radius:
                return True
            else:
                return False

        return False

    def applyCollision(self, otherObject):
        pass


    def drawSelf(self, surface):
        pygame.draw.circle(surface, self.color, (self.position[0], self.position[1]), self.radius, 0)



