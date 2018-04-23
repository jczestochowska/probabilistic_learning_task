import pandas as pd
import os
import itertools
import numpy as np

from scripts.player import VirtualPlayer
from game_session import GameSession
from models import RescorlaWagner, Qlearning
from data_utils import round_number, make_directory


def _create_file_path(filename):
    path = _create_path()
    return os.path.join(path, filename)


def _create_path():
    parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(os.path.join(parent_directory, 'data'), 'virtual_players')
    return path


def prepare_params():
    T = np.arange(-10, 10, 0.5).tolist()
    alpha = np.arange(-1, 1, 0.1).tolist()
    params_ql = itertools.product(T, alpha)
    params_rl = itertools.product(T, alpha, alpha)
    return params_ql, params_rl


def generate_game_sessions_with_real_player_parameters():
    path = _create_path()
    make_directory(directory=path)
    df = pd.read_csv('/Users/karola/PycharmProjects/ZPI/scripts/new_real_player_params_ql.csv')
    for index, row in df.iterrows():
        game = GameSession()
        model = Qlearning()
        player = VirtualPlayer(row['T'], row['alpha'], game_skeleton=game.game_skeleton, model=model)
        game.play(player=player)
        game._create_result()
        file = tuple(map(str, (round_number(row['T']), round_number(row['alpha']), row['name'])))
        path = _create_file_path(filename="QL_" + "_".join(file))
        game.result.to_csv(path, index=False)


def generate_game_sessions_with_all_parameters():
    path = _create_path()
    make_directory(directory=path)
    params_ql, params_rl = prepare_params()
    for trial in params_ql:
        game = GameSession()
        model = Qlearning()
        player = VirtualPlayer(trial[0], trial[1], game_skeleton=game.game_skeleton, model=model)
        game.play(player=player)
        game._create_result()
        file = tuple(map(str, round_number(trial[0]), round_number(trial[1])))
        path = _create_file_path(filename="QL_" + "_".join(file))
        game.result.to_csv(path, index=False)


if __name__ == '__main__':
    generate_game_sessions_with_real_player_parameters()
