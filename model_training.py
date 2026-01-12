import neat
import pygame
from game import draw_window, Bird, Pipe, Base, WIN_WIDTH, WIN_HEIGHT

# Constants
WIN_HEIGHT = 800
WIN_WIDTH = 500
DRAW_LINES = True
GEN = 0

class Model_training:
    def train(genomes, config):
        global GEN
        GEN += 1
        birds = []
        ge = []
        neural_network = []

        # Create new birds and neural networks everytime new generation comes
        for _, g in genomes:
            net = neat.nn.FeedForwardNetwork.create(g, config= config)
            neural_network.append(net)
            birds.append(Bird(230 ,350))
            g.fitness = 0
            ge.append(g)

        pipes = [Pipe(500)] # list of pipe objects
        base_object = Base(630)
        win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        clock = pygame.time.Clock()
        run = True
        score = 0

        while run: # main running loop
            clock.tick(60) # fps
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    quit()

            pipe_ind = 0

            if len(birds) > 0:
                if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].TOP_PIPE.get_width():
                    pipe_ind = 1

            else: # if all the birds are dead then exit the loop
                break

            for x, bird in enumerate(birds):
                bird.move()
                ge[x].fitness += 0.1

                output = neural_network[x].activate(
                    (bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))
                if output[0] > 0.5:
                    bird.jump()

            for pipe in pipes:
                for x, bird in enumerate(birds):
                    # checking if the bird hit the ground, pipe, or the top boundary
                    if pipe.collide(bird) or (bird.y + bird.img.get_height() >= 630 or bird.y < 0):
                        ge[x].fitness -= 1
                        birds.pop(x)
                        ge.pop(x)
                        neural_network.pop(x)
                    if not pipe.passed and bird.x > pipe.x:
                        pipe.passed = True
                        for g in ge:
                            g.fitness += 5
                        score += 1
                        pipes.append(Pipe(500))

                if pipe.x + pipe.TOP_PIPE.get_width() < 0:
                    pipes.remove(pipe)

                pipe.move()
            base_object.move()
            draw_window(win, birds, pipes, base_object, score, GEN, pipe_ind)