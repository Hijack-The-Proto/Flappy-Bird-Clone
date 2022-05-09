import pygame
from GLOBAL import *
import random

class Pipe:
    def __init__(self):
        random.seed()
        self.pipeMouthRange = (100, HEIGHT-100)
        self.midpoint = (WIDTH+100, random.randint(self.pipeMouthRange[0],self.pipeMouthRange[1]))
        self.position = self.midpoint
        self.pipeGap = 150
        self.positionTop = self.position[1] - int(self.pipeGap/2)
        self.positionBottom = self.position[1] + int(self.pipeGap/2)
        self.goalHit = False
    def draw(self, surface):
        top = pygame.Rect(((self.position[0] - int(100/2), self.position[1]-(int(self.pipeGap/2))-1000), (100,1000)))
        bottom = pygame.Rect(((self.position[0] - int(100/2), self.position[1]+(int(self.pipeGap/2))), (100,1000)))
        if self.goalHit:
            goal = pygame.Rect(((self.position[0], self.position[1]-int(HEIGHT/2)), (1,1)))
        else:    
            goal = pygame.Rect(((self.position[0], self.position[1]-int(HEIGHT/2)), (1,HEIGHT)))
        self.goal = pygame.draw.rect(surface, (255, 255, 255), goal)
        self.topPipe = pygame.draw.rect(surface, (0, 255, 0), top)
        self.bottomPipe = pygame.draw.rect(surface, (0, 255, 0), bottom)
    def move(self):
        self.movementSpeed = 10
        self.position = (self.position[0] - self.movementSpeed, self.position[1])

