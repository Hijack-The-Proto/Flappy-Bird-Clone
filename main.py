import os
import pygame
import neat
from pygame.locals import *
from bird import Bird
from pipe import Pipe
from GLOBAL import *
import math
import argparse

GEN = 0
WIDTH, HEIGHT = 640, 480
FPS = 30
RUN_NEAT = False
CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'config.txt')

def createPipe(pipeSequence):
    p = Pipe()
    pipeSequence.append(p)
    if len(pipeSequence) > 5:
        pipeSequence.pop(0)
        

def runNeat():
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         CONFIG_PATH)

    pop = neat.Population(config)
    pop.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)

    winner = pop.run(neatGame, 50)
    print('\nBest genome:\n{!s}'.format(winner))


def game(): #Play yourself. 
    pygame.init()
    fpsClock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    surface.fill((255,255,255))
    myfont = pygame.font.SysFont("monospace", 16)

    bird = Bird() 
    pipeSequence = [Pipe()]
    clock = 0
    score = 0

    bird.draw(surface)

    while True:
        clock += fpsClock.tick(FPS)
        surface.fill((255,255,255))

        if clock > 3000:
            createPipe(pipeSequence)
            clock = 0

        bird.handle_keys()
        bird.gravity()
        
        for p in pipeSequence:
            p.move()
            p.draw(surface)
            if pygame.Rect.colliderect(bird.body, p.topPipe) or pygame.Rect.colliderect(bird.body, p.bottomPipe) or bird.position[1] > HEIGHT + 60 or bird.position[1] < -60:
                print('Fail')
                bird.reset()
                pipeSequence = []
                score = 0
                clock = 0
                createPipe(pipeSequence)
            if pygame.Rect.colliderect(bird.body, p.goal):
                score+=1
                p.goalHit = True 

        bird.draw(surface)
        screen.blit(surface, (0,0))
        text = myfont.render('Score {0}'.format(score), 1, (0,0,0))
        screen.blit(text, (5, 10))
  
        pygame.display.flip()
        
        pygame.display.update()

def neatGame(genomes, config): #Play with NEAT ML model
    pygame.init()
    fpsClock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    surface.fill((255,255,255))
    myfont = pygame.font.SysFont("monospace", 16)
    global GEN
    GEN += 1

    nets = []
    birds = []
    ge = []
    for genome_id, genome in genomes: #Gets a tuple object, for readability I gave both parts a name but only needed to use the second 
        genome.fitness = 0  # start with fitness level of 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        birds.append(Bird())
        ge.append(genome)

    pipeSequence = [Pipe()]
    targetPipe = 0
    pipePassed = False
    clock = 0
    score = 0

    while True and len(birds) > 0:
        clock += fpsClock.tick(FPS)
        surface.fill((255,255,255))

        if clock > 2000:
            createPipe(pipeSequence)
            clock = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                break

        for x, bird in enumerate(birds): 
            ge[x].fitness += 0.1 # give each bird a fitness of 0.1 for each frame it stays alive
            #ML Stats
            birdYPosition = bird.position[1]
            bottomPipeDistance = math.sqrt((pipeSequence[targetPipe].position[0] - bird.position[0])**2 + ((pipeSequence[targetPipe].position[1] + int(pipeSequence[targetPipe].pipeGap/2)) - bird.position[1])**2)
            topPipeDistance = math.sqrt((pipeSequence[targetPipe].position[0] - bird.position[0])**2 + ((pipeSequence[targetPipe].position[1] - int(pipeSequence[targetPipe].pipeGap/2)) - bird.position[1])**2)
            output = nets[birds.index(bird)].activate((birdYPosition, bottomPipeDistance, topPipeDistance)) #Using just the distance from bird to pipes 

            if output[0] > 0.5:  # we use a tanh activation function so result will be between -1 and 1. if over 0.5 bird will flap.
                bird.flap()
            
            bird.gravity()
            bird.draw(surface)

        for x, p in enumerate(pipeSequence):
            if p.goalHit == False:
                targetPipe = x
                break
        
        for x, p in enumerate(pipeSequence):
            p.move()
            p.draw(surface)
            for bird in birds:
                if pygame.Rect.colliderect(bird.body, p.topPipe) or pygame.Rect.colliderect(bird.body, p.bottomPipe) or bird.position[1] > HEIGHT + 10 or bird.position[1] < -10:
                    ge[birds.index(bird)].fitness -= 5
                    nets.pop(birds.index(bird))
                    ge.pop(birds.index(bird))
                    birds.pop(birds.index(bird))
                    
                if pygame.Rect.colliderect(bird.body, p.goal):
                    pipePassed = True
                    p.goalHit = True 
                    
                if x == targetPipe:
                    pygame.draw.line(surface, (0,0,255), bird.position, (p.position[0], p.position[1] + int(p.pipeGap/2)))
                    pygame.draw.line(surface, (0,0,255), bird.position, (p.position[0], p.position[1] - int(p.pipeGap/2)))
        
        if pipePassed:
            score+=1
            for genome in ge:
                genome.fitness += 5
            pipePassed = False
            if score >= 25: # Kill the run after a score of 25, this is so the game wont go on forever. 
                for bird in birds:
                    ge[birds.index(bird)].fitness += 20
                    nets.pop(birds.index(bird))
                    ge.pop(birds.index(bird))
                    birds.pop(birds.index(bird))
                print("Killing run, Birds could play forever.")

        screen.blit(surface, (0,0))
        text = myfont.render('Score {0} Generation {1} Live Birds {2}'.format(score, GEN, len(birds)), 1, (0,0,0))
        screen.blit(text, (5, 10))
        pygame.display.flip()
        pygame.display.update()


def main():
    parser = argparse.ArgumentParser(description='Flappy Bird. Play yourself, or let a Neural Network do the work!')
    parser.add_argument('--neat', help='Let the NEAT-Python module take over and play this game.', action='store_true', dest='playWithNeat', default=False)
    args = parser.parse_args()
    if args.playWithNeat:
        runNeat()
    else:
        game()

if __name__ == '__main__':
    main()