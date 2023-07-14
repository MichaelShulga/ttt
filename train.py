import copy
import itertools
import pickle
import random

from matplotlib import pyplot as plt
import game
import numpy as np


def relu(x):
    return x * (x > 0)


k = 3
def change_random(array):
    for i in range(len(array)):
        array[i] += (random.random() - 0.5) / k
    return array


# class Genome:
#     def __init__(self) -> None:
#         self.l1w = np.random.rand(9, 9) - 0.5
#         self.l2w = np.random.rand(9) - 0.5
#         self.b1 = np.random.rand(9) - 0.5
#         self.b2 = np.random.rand(1)[0] - 0.5

#         self.fitness = None
#         self.epoch = None

#     def mutate(self):
#         self.l1w = change_random(self.l1w.reshape(81)).reshape(9, 9)
#         self.l2w = change_random(self.l2w)
#         self.b1 = change_random(self.b1)
#         self.b2 += (random.random() - 0.5) / k

#     def activate(self, input_layer):
#         hidden = np.array([relu(weights @ input_layer + bias) for bias, weights in zip(self.b1, self.l1w)])
#         output = np.tanh(hidden @ self.l2w + self.b2)

#         return output


class Genome:
    def __init__(self) -> None:
        self.arr = np.random.rand(9 + 1)

        self.fitness = None
        self.epoch = None

    def mutate(self):
        self.arr = change_random(self.arr)

    def activate(self, input_layer):
        return self.arr @ np.append(input_layer, [1])


def eval_genomes(genomes):
    for genome in genomes:
        genome.fitness = 0
    
    for genome1, genome2 in itertools.combinations(genomes, 2):
        f1 = game.move_from_evaluation_function(genome1.activate)
        f2 = game.move_from_evaluation_function(genome2.activate)
        match game.execute(f1, f2):
            case 1:
                genome1.fitness += 1 / len(genomes)
            case 0:
                genome1.fitness += 0.5 / len(genomes)
                genome2.fitness += 0.5 / len(genomes)
            case -1:
                genome2.fitness += 1 / len(genomes)
            case _:
                raise Exception
            

def main():
    genomes = [Genome() for _ in range(50)]
    for genome in genomes:
        genome.epoch = 0
    fitnesses = []

    for epoch in range(1000):
        print('running epoch', epoch)
        eval_genomes(genomes)
        winner = max(genomes, key=lambda x: x.fitness)
        fitnesses.append(winner.fitness)
        print('winner fitness:', winner.fitness, 'epoch', winner.epoch)
        next_genomes = []
        for genome in sorted(genomes, key=lambda x: x.fitness)[25:]:
            next_genomes.append(genome)
            for _ in range(1):
                mutated = copy.deepcopy(genome)
                mutated.mutate()
                next_genomes.append(mutated)
                # genome = Genome()
                # genome.epoch = epoch
                # next_genomes.append(genome)
        genomes = next_genomes
    print('game rate', game.rate(game.move_from_evaluation_function(winner.activate)))

    # Save the winner.
    with open('best_genome', 'wb') as f:
        pickle.dump(winner, f, pickle.HIGHEST_PROTOCOL)

    plt.plot(fitnesses)
    plt.show()


def develop():
    genomes = [Genome() for _ in range(10)]
    rates = [game.rate(game.move_from_evaluation_function(i.activate)) for i in genomes]
    plt.plot(sorted(rates))
    plt.show()


if __name__ == '__main__':
    main()
    # develop()
    