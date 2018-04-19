import pandas as pd
import os
import itertools
import numpy as np

from scripts.player import VirtualPlayer
from game_session import GameSession
from models import RescorlaWagner, Qlearning
from data_utils import round_number, make_directory


def _create_file_path(filename):
    directory = '/Users/karola/PycharmProjects/ZPI/data/virtual_players'
    return os.path.join(directory, filename)


def prepare_params():
    T = np.arange(-10, 10, 0.5).tolist()
    alpha = np.arange(-1, 1, 0.1).tolist()
    params_ql = itertools.product(T, alpha)
    params_rl = itertools.product(T, alpha, alpha)
    return params_ql, params_rl


def generate_game_sessions_with_real_player_parameters():
    make_directory(directory='/Users/karola/PycharmProjects/ZPI/data/virtual_players')
    df = pd.read_csv('/Users/karola/PycharmProjects/ZPI/scripts/new_real_player_params_ql.csv')
    for index, row in df.iterrows():
        game = GameSession()
        model = Qlearning()
        # model = RescorlaWagner()
        player = VirtualPlayer(row['T'], row['alpha'], game_skeleton=game.game_skeleton, model=model)
        # player = VirtualPlayer(row['T'], row['alpha_gain'], row['alpha_lose'], game_skeleton=game.game_skeleton, model=model)
        game.play(player=player)
        game._create_result()
        file = tuple(map(str, (round_number(row['T']), round_number(row['alpha']), row['name'])))
        # file = tuple(map(str, (round_number(row['T']), round_number(row['alpha_gain'], round_number(row['alpha_lose']), row['name'])))
        path = _create_file_path(filename="QL_" + "_".join(file))
        # path = _create_file_path(filename="RW_"+"_".join(file))
        game.result.to_csv(path, index=False)


def generate_game_sessions_with_all_parameters():
    make_directory(directory='/Users/karola/PycharmProjects/ZPI/data/virtual_players')
    params_ql, params_rl = prepare_params()
    for trial in params_ql:
        game = GameSession()
        model = Qlearning()
        # model = RescorlaWagner()
        player = VirtualPlayer(trial[0], trial[1], game_skeleton=game.game_skeleton, model=model)
        # player = VirtualPlayer(trial[0], trial[1], trial[2], game_skeleton=game.game_skeleton, model=model)
        game.play(player=player)
        game._create_result()
        file = tuple(map(str, round_number(trial[0]), round_number(trial[1])))
        # file = tuple(map(str, round_number(trial[0]), round_number(trial[1]), round_number(trial[2])))
        path = _create_file_path(filename="QL_" + "_".join(file))
        # path = _create_file_path(filename="RW_"+"_".join(file))
        game.result.to_csv(path, index=False)


if __name__ == '__main__':
    generate_game_sessions_with_real_player_parameters()
