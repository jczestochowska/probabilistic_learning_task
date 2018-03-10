from abc import abstractmethod
from math import exp, log
from random import random

from scripts.Qlearning import Qlearning


class Player(object):
    def __init__(self, **params):
        # params: type --> Dict[str, float]
        # params: alpha, T and so on
        self.Q_learning = Qlearning()
        self.params = params

        @abstractmethod
        def decide(self, game_skeleton):
            pass


class VirtualPlayer(Player):
    pass


class ModelAsPlayer(Player):
    '''uses Q-learning module, holds responsibility for updating max-likelihood function, and optimizing its parameters'''

    def __init__(self):
        super(ModelAsPlayer, self).__init__()
        self.T = 0.5
        self.decisions = []
        self.Q_table = self.Q_learning.Q_table
        # self.Q_table = [0.1, 0.4, 0.3, 0.2, 0.1, 0.4] # przykładowe

    def probability_A(self, Q_A, Q_B):
        p_A = 1 / (1 + exp((Q_A - Q_B) / self.T))
        return p_A

    def decide(self, game_skeleton):
        condition_left = game_skeleton['StimulusLeft']
        condition_right = game_skeleton['StimulusRight']
        for index in range(len(condition_left)):
            p_a = self.probability_A(self.Q_table[condition_left[index] - 1],
                                     self.Q_table[condition_right[index] - 1])
            dec = lambda x: random() < x
            self.decisions.append(int(dec(p_a)))
        return self.decisions

    def max_likelihood_method(self, game_skeleton):
        likelihood = 0
        condition_left = game_skeleton['StimulusLeft']
        condition_right = game_skeleton['StimulusRight']
        for index in range(len(condition_left)):
            p_a = self.probability_A(self.Q_table[condition_left[index] - 1],
                                     self.Q_table[condition_right[index] - 1])
            y = self.decisions[index]
            likelihood += y * log(p_a) + (1 - y) * log(1 - p_a)
        return likelihood

# -----proba---
# game_skeleton = {'StimulusLeft': [1, 2, 3, 5, 2, 1, 3, 5, 2, 1], 'StimulusRight': [2, 1, 4, 6, 1, 2, 4, 6, 1, 2]}
# player1 = ModelAsPlayer()
# actions = player1.decide(game_skeleton)
# ll = player1.max_likelihood_method(game_skeleton)
# print(actions)
# print(ll)
