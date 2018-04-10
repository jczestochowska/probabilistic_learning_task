import numpy as np
import random
import os

from player import VirtualPlayer
from game_session import GameSession
from models import RescorlaWagner, Qlearning

def prepare_parameters(number_of_trials, num_of_params):
    parameters = np.zeros((number_of_trials, num_of_params))
    if num_of_params == 3:
        for params in range(parameters.shape[0]):
            parameters[params][0] = random.random()
            parameters[params][1] = random.uniform(-10,10)
            parameters[params][2] = random.uniform(-10,10)
    else:
        for params in range(parameters.shape[0]):
            parameters[params][0] = random.random()
            parameters[params][1] = random.uniform(-10,10)

    return parameters


def _create_file_path(filename):
    parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(parent_directory, "data", filename)


if __name__=='__main__':
    game = GameSession()
    params = prepare_parameters(10,3)
    attempt = params[0,:]
    player = VirtualPlayer(game.game_skeleton, attempt[0], attempt[1], attempt[2])
    model = RescorlaWagner()
    game.play(player=player, model=model)
    game._create_result()
    file = np.array2string(attempt)
    path = _create_file_path(filename="RW"+file)
    game.result.to_csv(path, index=False)
    #print(params[0,:][0])