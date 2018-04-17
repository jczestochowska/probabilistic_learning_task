import itertools
import numpy as np
import os

from player import VirtualPlayer
from game_session import GameSession
from models import RescorlaWagner, Qlearning


def prepare_params():
    T = np.arange(-10, 10, 0.5).tolist()
    alpha = np.arange(-1, 1, 0.1).tolist()
    params_ql = itertools.product(T, alpha)
    params_rl = itertools.product(T, alpha, alpha)
    return params_ql, params_rl


def _create_file_path(filename):
    parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(parent_directory, "data", "virtual_players", filename)


if __name__=='__main__':
    params_ql, params_rl = prepare_params()

    for trial in params_ql:
         game = GameSession()
         player = VirtualPlayer(game.game_skeleton, trial[0], trial[1])
         model = Qlearning()
         game.play(player=player, model=model)
         game._create_result()
         file = tuple(map(str, trial))
         path = _create_file_path(filename="RW"+",".join(file))
         game.result.to_csv(path, index=False)
