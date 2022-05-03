import pygame
import sys

class Bird:
    def __init__(self):
        self.position = (200,200)
        self.size = (20,20) #x, y size of a hitbox
        self.color = (255,0,0) # to be replaced by an image
        self.momentum = 0
    def gravity(self):
        self.downForce = 1 #How fast the bird falls 
        self.momentum +=self.downForce
        self.position = (200, self.position[1] + self.momentum)
    def flap(self):
        self.flapForce = -18
        self.momentum = self.momentum + self.flapForce
    def draw(self, surface): 
        r = pygame.Rect(self.position, self.size)
        self.body = pygame.draw.rect(surface, self.color, r)
    def reset(self):
        self.position = (200,200)
        self.size = (20,20) #x, y size of a hitbox
        self.color = (255,0,0) # to be replaced by an image
        self.momentum = 0
    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.flap()
                
