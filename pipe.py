import pygame
from GLOBAL import *
import math
import random

class Pipe:
    def __init__(self):
        random.seed()
        self.pipeMouthRange = (100, HEIGHT-100)
        self.midpoint = (WIDTH+100, random.randint(self.pipeMouthRange[0],self.pipeMouthRange[1]))
        self.position = self.midpoint
        self.pipeGap = 150
        self.goalHit = False
    def draw(self, surface):
        #center = pygame.Rect((self.midpoint[0] - int(11/2), self.midpoint[1] - int(11/2)), (11,11))
        #center1 = pygame.Rect((self.midpoint[0] - int(50/2), self.midpoint[1] - int(1/2)), (50,1))
        #center2 = pygame.Rect((self.midpoint[0] - int(1/2), self.midpoint[1] - int(50/2)), (1,50))
        top = pygame.Rect(((self.position[0] - int(100/2), self.position[1]-(int(self.pipeGap/2))-500), (100,500)))
        bottom = pygame.Rect(((self.position[0] - int(100/2), self.position[1]+(int(self.pipeGap/2))), (100,500)))
        if self.goalHit:
            goal = pygame.Rect(((self.position[0], self.position[1]-int(HEIGHT/2)), (1,1)))
        else:    
            goal = pygame.Rect(((self.position[0], self.position[1]-int(HEIGHT/2)), (1,HEIGHT)))

        #pygame.draw.rect(surface, (0, 255, 0), center)
        #pygame.draw.rect(surface, (255, 0, 0), center1)
        #pygame.draw.rect(surface, (255, 0, 0), center2)

        self.goal = pygame.draw.rect(surface, (255, 255, 255), goal)
        self.topPipe = pygame.draw.rect(surface, (0, 255, 0), top)
        self.bottomPipe = pygame.draw.rect(surface, (0, 255, 0), bottom)
    def move(self):
        self.movementSpeed = 5
        self.position = (self.position[0] - self.movementSpeed, self.position[1])

