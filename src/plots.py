from scripts.game_session import GameSession
from scripts.models import Qlearning
from scripts.player import RealPlayer, VirtualPlayer
from scripts.data_utils import make_directory
from scripts.generate_game_sessions import _create_path, _create_file_path

import matplotlib

matplotlib.use('TkAgg')
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

import numpy as np
import os


def make_plot(dir):
    model = Qlearning()
    rp = RealPlayer(dir, model=model)
    game = GameSession()
    player = VirtualPlayer(10, 0.1, game_skeleton=game.game_skeleton, model=model)
    game.play(player=player)
    game._create_result()

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    T = np.arange(-1, 1, 0.1)
    print(T.shape)
    alpha = np.arange(0, 1, 0.05)
    print(alpha.shape)

    X, Y = np.meshgrid(T, alpha)

    zs = np.array([rp.log_likelihood_function(list(x)) for x in zip(np.ravel(X), np.ravel(Y))])
    Z = zs.reshape(X.shape)

    ax.plot_surface(X, Y, Z)

    ax.set_xlabel('T')
    ax.set_ylabel('alpha')
    ax.set_zlabel('log likelihood')


if __name__ == '__main__':
    directory = '/Users/karola/PycharmProjects/ZPI/data/'
    for file in os.listdir(directory):
        if file.endswith('.xls'):
            dir = os.path.join(directory, file)
            path = _create_path(dir='plots')
            print(path)
            make_directory(path)
            make_plot(dir)
            plot_path = os.path.join(path, "".join(file) + ".png")
            print(plot_path)
            plt.savefig(plot_path)
