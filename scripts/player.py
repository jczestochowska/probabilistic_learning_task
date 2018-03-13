from abc import abstractmethod
from math import exp, log
from random import random, choice
from scipy.optimize import minimize
import numpy as np

from scripts.Qlearning import Qlearning


class Player(object):
    def __init__(self, **params):
        # params: type --> Dict[str, float]
        # params: alpha, T and so on
        self.Q_learning = Qlearning()
        self.params = params

        # @abstractmethod
        # def decide(self, game_skeleton):
        #     pass


class VirtualPlayer(Player):
    pass


class ModelAsPlayer(Player):
    '''uses Q-learning module, holds responsibility for updating max-likelihood function, and optimizing its parameters'''

    def __init__(self, game_skeleton):
        super(ModelAsPlayer, self).__init__()
        self.condition_left = game_skeleton['StimulusLeft']
        self.condition_right = game_skeleton['StimulusRight']
        self.Q_table = self.Q_learning.Q_table
        self.decisions = []
        self.T = 0.2

    def probability_A(self, Q_A, Q_B, T):
        p_A = 1 / (1 + exp((Q_B - Q_A) / T))
        return p_A

    def decide(self):
        for index, condition_left in enumerate(self.condition_left):
            condition_right = self.condition_right[index]
            Q_A = self.Q_table[condition_left - 1]
            p_a = self.probability_A(Q_A, 1 - Q_A, self.T)
            dec = lambda x: random() < x
            decision = int(dec(p_a))
            self.decisions.append(decision)
            reward = self.reward(decision)
            self.Q_learning.update_q_table(condition_left, condition_right, decision, reward)
        return self.decisions

    # prowizorka póki nie wiemy jak pobierać te nagrody i kary
    @staticmethod
    def reward(decision):
        if decision == 1:
            return choice([1, -1])
        elif decision == 0:
            return choice([1, -1])


class Estimator(ModelAsPlayer):
    def __init__(self):
        super(Estimator, self).__init__(game_skeleton)
        self.player = ModelAsPlayer(game_skeleton)
        self.decisions = self.player.decisions
        self.condition_left = self.player.condition_left
        self.condition_right = self.player.condition_right
        self.Q_table = self.Q_learning.Q_table

    def loglikelihood_function(self, T, sign=1.0):
        loglikelihood = 0
        for decision, index in enumerate(self.decisions):
            Q_A = self.Q_table[self.condition_left[index] - 1]
            p_a = self.probability_A(Q_A, 1 - Q_A, T)
            reward = self.reward(decision)
            self.Q_learning.update_q_table(self.condition_left[index], self.condition_right[index], decision, reward)
            loglikelihood += sign * (decision * log(max(p_a, 0.01)) + (1 - decision) * log(1 - min(p_a, 0.99)))
        return loglikelihood

    def max_LLE(self):
        opt_function = self.loglikelihood_function
        opt_T = minimize(opt_function, np.array([0.1]), args=(-1.0,))
        return opt_T


if __name__ == '__main__':
    game_skeleton = {'StimulusLeft': [1, 2, 3, 5, 2, 1, 3, 5, 2, 1], 'StimulusRight': [2, 1, 4, 6, 1, 2, 4, 6, 1, 2]}
    player1 = ModelAsPlayer(game_skeleton)
    estimator = Estimator()
    print(player1.decide())
    print(player1.Q_table)
    print(estimator.max_LLE())
