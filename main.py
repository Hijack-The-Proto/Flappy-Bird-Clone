import sys
from turtle import position
 
import pygame
from pygame.locals import *
from bird import Bird
from pipe import Pipe
from GLOBAL import *

def createPipe(pipeSequence):
    p = Pipe()
    pipeSequence.append(p)
    if len(pipeSequence) > 5:
        pipeSequence.pop(0)

def main():
    pygame.init()

    fpsClock = pygame.time.Clock()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    surface.fill((255,255,255))
    myfont = pygame.font.SysFont("monospace", 16)

    bird = Bird()
    pipe = Pipe()
    pipeSequence = [pipe]
    clock = 0
    score = 0


    bird.draw(surface)

    while True:
        game_time = fpsClock.tick(FPS)
        surface.fill((255,255,255))

        clock += game_time

        if clock > 3000:
            createPipe(pipeSequence)
            clock = 0

        # Update.
        bird.handle_keys()
        bird.gravity()
        
        for p in pipeSequence:
            p.move()
            p.draw(surface)
            if pygame.Rect.colliderect(bird.body, p.topPipe) or pygame.Rect.colliderect(bird.body, p.bottomPipe):
                print('Fail')
                bird.reset()
                pipeSequence = []
                score = 0
                clock = 0
                createPipe(pipeSequence)
            if pygame.Rect.colliderect(bird.body, p.goal):
                score+=1
                p.goalHit = True

        if bird.position[1] > HEIGHT + 60 or bird.position[1] < -60:
            print('Fail')
            bird.reset()
            pipeSequence = []
            score = 0
            clock = 0
            createPipe(pipeSequence)
  
        # Draw.
        bird.draw(surface)
        screen.blit(surface, (0,0))
        text = myfont.render('Score {0}'.format(score), 1, (0,0,0))
        screen.blit(text, (5, 10))
  
        pygame.display.flip()
        
        pygame.display.update()

if __name__ == '__main__':
    main()