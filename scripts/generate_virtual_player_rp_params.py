import pandas as pd
import os

from scripts.player import VirtualPlayer
from game_session import GameSession
from models import RescorlaWagner, Qlearning


def _create_file_path(filename):
    parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(parent_directory, "data", "virtual_players_rp", filename)


if __name__=='__main__':
    df = pd.read_csv('/Users/karola/PycharmProjects/ZPI/scripts/new_real_player_params_ql.csv')

    for index, row in df.iterrows():
        T = float(row['T'])
        alpha = float(row['alpha'])
        game = GameSession()
        model = Qlearning()
        player = VirtualPlayer(row['T'], row['alpha'], game_skeleton=game.game_skeleton, model=model)
        game.play(player=player)
        game._create_result()
        file = tuple(map(str, row))
        path = _create_file_path(filename="QL"+"_".join(file))
        game.result.to_csv(path, index=False)