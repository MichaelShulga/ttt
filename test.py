# load the winner
import os
import pickle
import neat
import game


# with open('winner', 'rb') as f:
#     c = pickle.load(f)

# print('Loaded genome:')
# print(c)

# local_dir = os.path.dirname(__file__)
# config_path = os.path.join(local_dir, 'config-feedforward')
# config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
#                      neat.DefaultSpeciesSet, neat.DefaultStagnation,
#                      config_path)


# net = neat.nn.FeedForwardNetwork.create(c, config)
# f = game.get_func_from_rate(net.activate)





from train import Genome

# with open('company_data.pkl', 'rb') as inp:
#     company1 = pickle.load(inp)
#     print(company1.fitness)  # -> banana


with open('best_genome', 'rb') as f:
    c = pickle.load(f)
print(c)



# arr = [
#     -1, 0, -1,
#     0, 1, 0,
#     0, 0, 1
#        ]


arr = [
    -1, 0, 1,
    1, 0, 0,
    -1, 0, 1
       ]


# print(f(arr))
print(c.activate(arr))
