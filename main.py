import itertools
import os
import pickle
import random

import neat
import game
import visualize

from matplotlib import pyplot as plt
import numpy as np

def is_power_of_two(n):
    return (n != 0) and (n & (n - 1) == 0)


def eval_genomes(genomes, config):
    genomes = [genome for genome_id, genome in genomes]

    print(len(genomes))
    assert is_power_of_two(len(genomes)), len(genomes)

    for genome in genomes:
        genome.fitness = 0
    while len(genomes) > 1:
        qualified_genomes = []
        for genome1, genome2 in zip(genomes[::2], genomes[1::2]):
            net1 = neat.nn.FeedForwardNetwork.create(genome1, config)
            net2 = neat.nn.FeedForwardNetwork.create(genome2, config)

            f1 = game.get_func_from_rate(net1.activate)
            f2 = game.get_func_from_rate(net2.activate)
        
            match game.execute(f1, f2):
                case (1, 0):
                    genome1.fitness += 1
                    qualified_genomes.append(genome1)
                case (0.5, 0.5):
                    genome1.fitness += 0.5
                    genome2.fitness += 0.5
                    qualified_genomes.append(random.choice([genome1, genome2]))
                case (0, 1):
                    genome2.fitness += 1
                    qualified_genomes.append(genome2)
                case _:
                    raise Exception
        genomes = qualified_genomes



def eval_genomes(genomes, config):
    genomes = [genome for genome_id, genome in genomes]

    for genome in genomes:
        genome.fitness = 0
    
    for genome1, genome2 in itertools.combinations(genomes, 2):
        net1 = neat.nn.FeedForwardNetwork.create(genome1, config)
        net2 = neat.nn.FeedForwardNetwork.create(genome2, config)

        f1 = game.get_func_from_rate(net1.activate)
        f2 = game.get_func_from_rate(net2.activate)
    
        match game.execute(f1, f2):
            case (1, 0):
                genome1.fitness += 1 / len(genomes)
            case (0.5, 0.5):
                genome1.fitness += 0.5 / len(genomes)
                genome2.fitness += 0.5 / len(genomes)
            case (0, 1):
                genome2.fitness += 1 / len(genomes)
            case _:
                raise Exception
    
    # x = [genome.fitness for genome in genomes]
    # counts, bins = np.histogram(x, density=1, bins=30)
    # plt.stairs(counts, bins)
    # plt.show()


def run(config_file):
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)
 
    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(5, filename_prefix='checkpoints\\neat-checkpoint-'))

    winner = p.run(eval_genomes, 500)

    # Save the winner.
    with open('winner', 'wb') as f:
        pickle.dump(winner, f)

    visualize.draw_net(config, winner, True)
    # visualize.draw_net(config, winner, True, node_names=node_names, prune_unused=True)
    visualize.plot_stats(stats, ylog=False, view=True)
    # visualize.plot_species(stats, view=True)


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward')
    run(config_path)