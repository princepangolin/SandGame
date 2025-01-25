# imports
import pygame
from pygame.locals import *
from SpatialPartition import SpatialPartition
from SandParticle import SandParticle
from StaticWall import StaticWall
import math
import time

class App:

    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.width, self.height = 1080, 640
        self.clock = pygame.time.Clock()
        self.clockRate = 60
        self.simRate = 1.0/60
        
        self.spaceGrid = []
        self.gridSize = 10
        self.particleList = []
        self.spawnTimer = 50000
        self.staticList = []
        
        self.gravity = [0, 50]


    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True
        
        for i in range(0, self.width, self.gridSize):
            rowI = []
            for j in range(0, self.height, self.gridSize):
                rowI.append(SpatialPartition((i,j), self.gridSize))

            self.spaceGrid.append(rowI)

        staticWall = StaticWall((30, 405), 500, 200)
        self.staticList.append(staticWall)
        for i in range(30, 30+500, self.gridSize):
            for j in range(405, 405+200, self.gridSize):
                self.spaceGrid[int(i//10)][int(j//10)].physicsObjects.append(staticWall)

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False


    def on_loop(self):
        dt = self.simRate
        self.spawnTimer += self.clock.tick(self.clockRate)

        if pygame.mouse.get_pressed()[0] and self.spawnTimer > 10:
            self.spawnTimer = 0
            (x, y) = pygame.mouse.get_pos()
            newParticle = SandParticle(x, y, self.spaceGrid[x//10][y//10])
            self.particleList.append(newParticle)
            self.spaceGrid[x//10][y//10].physicsObjects.append(newParticle)
            
        # Set forces to 0, add any new forces, and check for collisions (which will also add a force)
        for particle in self.particleList[:]:
            self.addParticleToPartition(particle)

            particle.force = [0, 0]
            particle.updateForce(self.gravity)

            # Check all partitions particle is a part of
            for space in particle.spaces[:]:
                for obj in space.physicsObjects:
                    # Make sure we're not checking ourself
                    if obj != particle:
                        collision = particle.checkCollision(obj)
                        if collision:
                            particle.velocity = [0,0]
                            particle.force = [0,0]
                            particle.applyCollision(obj)
                            obj.applyCollision(particle)
                        
                # Once we've checked for all possible collisions for this particle, remove this space from the particle and this particle from the space
                particle.spaces.remove(space)
                space.physicsObjects.remove(particle)
                
            particle.updateVel(dt)
            particle.updatePos(dt)

            particle.drawSelf(self._display_surf)

            while len(self.particleList) > 300:
                self.particleList.pop(0)

                
    def addParticleToPartition(self, particle):
        pos = particle.position
        if pos[0] >= 0 and pos[0] <= self.width and pos[1] >= 0 and pos[1] <= self.height:
            self.spaceGrid[int(pos[0]//10)][int(pos[1]//10)].physicsObjects.append(particle)
            particle.spaces.append(self.spaceGrid[int(pos[0]//10)][int(pos[1]//10)])
        else:
            self.particleList.remove(particle)
            return

        # Starting straight up and going clockwise
        pos1 = [pos[0], pos[1] - particle.radius]
        pos2 = [pos[0] + particle.radius, pos[1]]
        pos3 = [pos[0], pos[1] + particle.radius]
        pos4 = [pos[0] - particle.radius, pos[1]]

        # Starting quadrant 1 and going clockwise
        offset = particle.radius/math.sqrt(2)
        pos5 = [pos[0] + offset, pos[1] - offset]
        pos6 = [pos[0] + offset, pos[1] + offset]
        pos7 = [pos[0] - offset, pos[1] + offset]
        pos8 = [pos[0] - offset, pos[1] + offset]
        
        if pos1[0] >= 0 and pos1[0] <= self.width and pos1[1] >= 0 and pos1[1] <= self.height:
            if not particle in self.spaceGrid[int(pos1[0]//10)][int(pos1[1]//10)].physicsObjects:
                self.spaceGrid[int(pos1[0]//10)][int(pos1[1]//10)].physicsObjects.append(particle)
                particle.spaces.append(self.spaceGrid[int(pos1[0]//10)][int(pos1[1]//10)])
                
        if pos2[0] >= 0 and pos2[0] <= self.width and pos2[1] >= 0 and pos2[1] <= self.height:
            if not particle in self.spaceGrid[int(pos2[0]//10)][int(pos2[1]//10)].physicsObjects:
                self.spaceGrid[int(pos2[0]//10)][int(pos2[1]//10)].physicsObjects.append(particle)
                particle.spaces.append(self.spaceGrid[int(pos2[0]//10)][int(pos2[1]//10)])
                
        if pos3[0] >= 0 and pos3[0] <= self.width and pos3[1] >= 0 and pos3[1] <= self.height:
            if not particle in self.spaceGrid[int(pos3[0]//10)][int(pos3[1]//10)].physicsObjects:
                self.spaceGrid[int(pos3[0]//10)][int(pos3[1]//10)].physicsObjects.append(particle)
                particle.spaces.append(self.spaceGrid[int(pos3[0]//10)][int(pos3[1]//10)])
                
        if pos4[0] >= 0 and pos4[0] <= self.width and pos4[1] >= 0 and pos4[1] <= self.height:
            if not particle in self.spaceGrid[int(pos4[0]//10)][int(pos4[1]//10)].physicsObjects:
                self.spaceGrid[int(pos4[0]//10)][int(pos4[1]//10)].physicsObjects.append(particle)
                particle.spaces.append(self.spaceGrid[int(pos4[0]//10)][int(pos4[1]//10)])
        
        if pos5[0] >= 0 and pos5[0] <= self.width and pos5[1] >= 0 and pos5[1] <= self.height:
            if not particle in self.spaceGrid[int(pos5[0]//10)][int(pos5[1]//10)].physicsObjects:
                self.spaceGrid[int(pos5[0]//10)][int(pos5[1]//10)].physicsObjects.append(particle)
                particle.spaces.append(self.spaceGrid[int(pos5[0]//10)][int(pos5[1]//10)])
                
        if pos6[0] >= 0 and pos6[0] <= self.width and pos6[1] >= 0 and pos6[1] <= self.height:
            if not particle in self.spaceGrid[int(pos6[0]//10)][int(pos6[1]//10)].physicsObjects:
                self.spaceGrid[int(pos6[0]//10)][int(pos6[1]//10)].physicsObjects.append(particle)
                particle.spaces.append(self.spaceGrid[int(pos6[0]//10)][int(pos6[1]//10)])
                
        if pos7[0] >= 0 and pos7[0] <= self.width and pos7[1] >= 0 and pos7[1] <= self.height:
            if not particle in self.spaceGrid[int(pos7[0]//10)][int(pos7[1]//10)].physicsObjects:
                self.spaceGrid[int(pos7[0]//10)][int(pos7[1]//10)].physicsObjects.append(particle)
                particle.spaces.append(self.spaceGrid[int(pos7[0]//10)][int(pos7[1]//10)])
                
        if pos8[0] >= 0 and pos8[0] <= self.width and pos8[1] >= 0 and pos8[1] <= self.height:
            if not particle in self.spaceGrid[int(pos8[0]//10)][int(pos8[1]//10)].physicsObjects:
                self.spaceGrid[int(pos8[0]//10)][int(pos8[1]//10)].physicsObjects.append(particle)
                particle.spaces.append(self.spaceGrid[int(pos8[0]//10)][int(pos8[1]//10)])


    def on_render(self):
        for obj in self.staticList:
            obj.drawSelf(self._display_surf)
        pygame.display.update()

    def on_cleanup(self):
        pygame.quit()


    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while(self._running):
            for event in pygame.event.get():
                self.on_event(event)

            self._display_surf.fill((255, 255, 255))

            self.on_loop()
            self.on_render()

        self.on_cleanup()


if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()