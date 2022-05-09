import pygame
import sys

class Bird:
    def __init__(self):
        self.position = (200,200)
        self.size = (21,21) #x, y size of a hitbox
        self.color = (255,0,0) # to be replaced by an image
        self.momentum = 0
        self.height = self.position[1]
        self.vel = 0
        self.tick_count = 0
    def gravity(self):
        self.tick_count += 1
        displacement = self.vel*(self.tick_count) + 0.5*(3)*(self.tick_count)**2  # calculate displacement
        if displacement >= 12: # terminal velocity
            displacement = (displacement/abs(displacement)) * 12

        if displacement < 0:
            displacement -= 2

        self.position = (self.position[0], self.position[1] + displacement)
    def flap(self):
        self.vel = -8
        self.tick_count = 0
        self.height = self.position[1]
    def draw(self, surface): 
        r = pygame.Rect((self.position[0] - int(self.size[0] / 2), self.position[1] - int(self.size[1] / 2)), self.size)
        r_outline = pygame.Rect((self.position[0] - int(self.size[0] / 2)-1, self.position[1] - int(self.size[1] / 2)-1), (self.size[0]+2, self.size[1]+2))
        self.body_outline = pygame.draw.rect(surface, (0,0,0), r_outline)
        self.body = pygame.draw.rect(surface, self.color, r)
    def reset(self):
        self.position = (200,200)
        self.momentum = 0
    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.flap()
                
