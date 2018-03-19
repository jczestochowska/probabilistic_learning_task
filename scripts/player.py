from abc import abstractmethod
from math import exp, log
from random import random, choice
from scipy.optimize import minimize
import numpy as np

from ReadData import Data
from Qlearning import Qlearning


class RealPlayer(object):
    def __init__(self):
        self.d = Data('C:/Users/Marlena/Desktop/studia/6 semestr/ZPI/gra ZPI/wyniki/MarlenaDudalearning.xls')
        self.data = self.d.prepare_data()
        self.condition_left = self.data['StimulusLeft']
        self.condition_right = self.data['StimulusRight']
        self.decisions = self.data['Actions']
        self.rewards = self.data['Rewards']
        self.Estimator = Estimator(self.decisions, self.condition_left, self.condition_right, self.rewards)

    def search_paramethers(self):
        opt_params = self.Estimator.max_LLE()
        T = opt_params['x'][0]
        alpha = opt_params['x'][1]
        return T, alpha


class Player(object):
    def __init__(self, **params):
        # params: type --> Dict[str, float]
        # params: alpha, T and so on
        self.Q_learning = Qlearning()
        self.params = params

        # @abstractmethod
        # def decide(self, game_skeleton):
        #     pass

    def probability_A(self, Q_A, Q_B, T):
        p_A = 1 / (1 + exp(min((Q_B - Q_A) / T, 700)))
        return p_A


class VirtualPlayer(Player):
    pass


class ModelAsPlayer(Player):
    def __init__(self, game_skeleton):
        super(ModelAsPlayer, self).__init__()
        self.condition_left = game_skeleton['StimulusLeft']
        self.condition_right = game_skeleton['StimulusRight']
        self.left_rewards = game_skeleton['LeftReward']
        self.right_rewards = game_skeleton['RightReward']
        self.better_stimulus = game_skeleton['BetterStimulus']
        self.Q_table = self.Q_learning.Q_table
        self.decisions = []
        self.rewards = []
        self.correct_actions = []
        self.T = 0.2
        self.alpha = 0.3

    def decide(self):
        for index, condition_left in enumerate(self.condition_left):
            left_reward = self.left_rewards[index]
            right_reward = self.right_rewards[index]
            condition_right = self.condition_right[index]
            Q_A = self.Q_table[condition_left - 1]
            p_a = self.probability_A(Q_A, 1 - Q_A, self.T)
            dec = lambda x: random() < x
            decision = int(dec(p_a))
            self._is_action_correct(decision, index)
            self.decisions.append(decision)
            reward = self.get_reward(decision, left_reward, right_reward)
            self.rewards.append(reward)
            self.Q_learning.update_q_table(condition_left, condition_right, decision, reward, self.alpha)
        return self.decisions

    def _is_action_correct(self, decision, index):
        if decision == self.better_stimulus[index]:
            self.correct_actions.append(1)
        else:
            self.correct_actions.append(0)

    @staticmethod
    def get_reward(decision, left_reward, right_reward):
        if decision == 1:
            reward = left_reward
        elif decision == 0:
            reward = right_reward
        if reward == 0:
            reward = -1
        return reward


class Estimator(Player):
    def __init__(self, decisions, condition_left, condition_right, rewards):
        super(Estimator, self).__init__()
        self.decisions = decisions
        self.rewards = rewards
        self.condition_left = condition_left
        self.condition_right = condition_right
        self.Q_table = self.Q_learning.Q_table

    def LL_function(self, params, sign=1.0):
        (T, alpha) = params
        loglikelihood = 0
        for index, decision in enumerate(self.decisions):
            Q_A = self.Q_table[self.condition_left[index] - 1]
            p_a = self.probability_A(Q_A, 1 - Q_A, T)
            reward = self.rewards[index]
            self.Q_learning.update_q_table(self.condition_left[index], self.condition_right[index], decision, reward,
                                           alpha)
            loglikelihood += sign * (decision * log(max(p_a, 0.01)) + (1 - decision) * log(1 - min(p_a, 0.99)))
        return loglikelihood

    def max_LLE(self):
        opt_function = self.LL_function
        opt_params = minimize(opt_function, x0=np.array([0.1, 0.1]), method='Nelder-Mead', args=(-1.0,))
        return opt_params


if __name__ == '__main__':
    game_skeleton = {
        'StimulusLeft': [3, 5, 1, 6, 1, 3, 1, 3, 5, 2, 6, 4, 5, 1, 3, 5],
        'StimulusRight': [4, 6, 2, 5, 2, 4, 2, 4, 6, 1, 5, 3, 6, 2, 4, 6]}
    player1 = ModelAsPlayer(game_skeleton)
    print(player1.decide())
    # print(player1.Q_table)
    rp = RealPlayer()
    print(rp.search_paramethers())
