from abc import abstractmethod
from math import exp, log
from random import random
from scipy.optimize import minimize
import numpy as np

from scripts.Data import ExcelData
from scripts.Qlearning import Qlearning
from scripts.RescorlaWagner import RescorlaWagner

MAX_EXP = 700
MIN_LOG = 0.01


class Player():
    def __init__(self, **params):
        # params: type --> Dict[str, float]
        # params: alpha, T and so on
        self.Q_learning = Qlearning()
        self.Rescola_Wagner = RescorlaWagner()
        self.params = params

    @abstractmethod
    def decide(self):
        pass

    def probability_A(self, Q_A, Q_B, T):
        return 1 / (1 + exp(min((Q_B - Q_A) / T, MAX_EXP)))


class VirtualPlayer(Player):
    def __init__(self, game_skeleton, **params):
        super(VirtualPlayer, self).__init__()
        self.condition_left = game_skeleton['StimulusLeft']
        self.condition_right = game_skeleton['StimulusRight']
        self.left_rewards = game_skeleton['LeftReward']
        self.right_rewards = game_skeleton['RightReward']
        self.better_stimulus = game_skeleton['BetterStimulus']
        self.decisions = []
        self.rewards = []
        self.correct_actions = []
        self.params = params

    def decide(self):
        T, alpha = self.params.values()
        Q_table = self.Q_learning.Q_table
        for index, condition_left in enumerate(self.condition_left):
            left_reward = self.left_rewards[index]
            right_reward = self.right_rewards[index]
            condition_right = self.condition_right[index]
            Q_A = Q_table[condition_left - 1]
            p_a = self.probability_A(Q_A, 1 - Q_A, T)
            decision = self._check_threshold(p_a)
            self._is_action_correct(decision, index)
            self.decisions.append(decision)
            reward = self.get_reward(decision, left_reward, right_reward)
            self.rewards.append(reward)
            self.Q_learning.q_learning_model((condition_left, condition_right, decision, reward), alpha)
        return self.decisions

    @staticmethod
    def get_reward(decision, left_reward, right_reward):
        if decision == 1:
            reward = left_reward
        elif decision == 0:
            reward = right_reward
        if reward == 0:
            reward = -1
        return reward

    @staticmethod
    def _check_threshold(p_a):
        return int(random() < p_a)

    def _is_action_correct(self, decision, index):
        if decision == self.better_stimulus[index]:
            self.correct_actions.append(1)
        else:
            self.correct_actions.append(0)


class RealPlayer():
    def __init__(self, data):
        self.data = data
        self.condition_left = self.data['StimulusLeft']
        self.condition_right = self.data['StimulusRight']
        self.decisions = self.data['Actions']
        self.rewards = self.data['Rewards']
        self.Estimator = Estimator(self.decisions, self.condition_left, self.condition_right, self.rewards)

    def search_parameters(self, model):
        return self.Estimator.max_log_likelihood(model).x


class Estimator(Player):
    def __init__(self, decisions, condition_left, condition_right, rewards):
        super(Estimator, self).__init__()
        self.decisions = decisions
        self.rewards = rewards
        self.condition_left = condition_left
        self.condition_right = condition_right
        self.Q_table = self.Q_learning.Q_table

    def log_likelihood_function(self, params, sign=1.0, model=None):
        T = params[0]
        method = None
        log_likelihood = 0
        for index, decision in enumerate(self.decisions):
            Q_A = self.Q_table[self.condition_left[index] - 1]
            p_a = self.probability_A(Q_A, 1 - Q_A, T)
            reward = self.rewards[index]
            game_data = (self.condition_left[index], self.condition_right[index], decision, reward)
            if model == 'Q_learning':
                method = self.Q_learning.q_learning_model
            elif model == 'Rescorla-Wagner':
                method = self.Rescola_Wagner.rescorla_wagner_model
            method(game_data, params)
            log_likelihood += sign * (
                decision * log(max(p_a, MIN_LOG)) + (1 - decision) * log(1 - min(p_a, 1 - MIN_LOG)))
        return log_likelihood

    def max_log_likelihood(self, model):
        x0 = np.array([])
        if model == 'Q_learning':
            x0 = np.array([0.1, 0.1])
        elif model == 'Rescorla-Wagner':
            x0 = np.array([0.1, 0.1, 0.1])
        return minimize(self.log_likelihood_function, x0=x0, method='Nelder-Mead', args=(-1.0, model))


if __name__ == '__main__':
    # game_skeleton = {
    #     'StimulusLeft': [3, 5, 1, 6, 1, 3, 1, 3, 5, 2, 6, 4, 5, 1, 3, 5],
    #     'StimulusRight': [4, 6, 2, 5, 2, 4, 2, 4, 6, 1, 5, 3, 6, 2, 4, 6]}
    # player1 = VirtualPlayer(game_skeleton)
    # print(player1.decide())
    excel_data = ExcelData('C:\\Users\\Marlena\\PycharmProjects\\ZPI\\ZPI\\data\\MarlenaDudalearning.xls')
    real_data = excel_data.prepare_data()
    rp = RealPlayer(real_data)
    print(rp.search_parameters('Q_learning'))
    print(rp.search_parameters('Rescorla-Wagner'))
