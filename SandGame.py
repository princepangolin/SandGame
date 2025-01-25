# imports
import pygame
from pygame.locals import *
from SpatialPartition import SpatialPartition
from SandParticle import SandParticle
from StaticWall import StaticWall

class App:

    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.width, self.height = 1080, 640
        self.clock = pygame.time.Clock()
        self.clockRate = 60
        
        self.spaceGrid = []
        self.gridSize = 10
        self.particleList = []
        self.spawnTimer = 0
        self.staticList = []
        
        self.gravity = [0, 0.002]


    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True
        
        for i in range(0, self.width, self.gridSize):
            rowI = []
            for j in range(0, self.height, self.gridSize):
                rowI.append(SpatialPartition((i,j), self.gridSize))

            self.spaceGrid.append(rowI)

        staticWall = StaticWall((30, 400), 500, 200)
        self.staticList.append(staticWall)
        for i in range(30, 30+500, self.gridSize):
            for j in range(400, 400+200, self.gridSize):
                self.spaceGrid[int(i//10)][int(j//10)].physicsObjects.append(staticWall)

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False


    def on_loop(self):
        dt = self.clock.tick(self.clockRate)
        self.spawnTimer += dt

        if pygame.mouse.get_pressed()[0] and self.spawnTimer > 5:
            self.spawnTimer = 0
            (x, y) = pygame.mouse.get_pos()
            newParticle = SandParticle(x, y)
            self.particleList.append(newParticle)
            self.spaceGrid[x//10][y//10].physicsObjects.append(newParticle)

        for row in self.spaceGrid:
            for partition in row:
                if partition.physicsObjects:
                    for obj in partition.physicsObjects[:]:
                        if not obj.static:
                            obj.force = [0, 0]
                            obj.updateForce(self.gravity)
                            for otherObj in partition.physicsObjects[:]:
                                #check for collisions
                                #testing my new branch
                                #sdfsdf
                                pass
                            
                            partition.physicsObjects.remove(obj)
                            
                else:
                    pass

        for particle in self.particleList:
            particle.updateVel(dt)

        for idx, particle in enumerate(self.particleList):
            particle.updatePos(dt)
            pos = particle.position
            if pos[0] >= 0 and pos[0] <= self.width and pos[1] >= 0 and pos[1] <= self.height:
                self.spaceGrid[int(pos[0]//10)][int(pos[1]//10)].physicsObjects.append(particle)

            particle.drawSelf(self._display_surf)

            if particle.position[0] > (self.width + 10) or particle.position[0] < (0 - 10) or particle.position[1] > (self.height + 10) or particle.position[1] < (0 - 10):
                partToDelete = self.particleList.pop(idx)
                del partToDelete


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