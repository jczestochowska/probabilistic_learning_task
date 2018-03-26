from abc import abstractmethod
from math import exp, log
from random import random
from scipy.optimize import minimize
import numpy as np
from pandas import read_excel

from scripts.Qlearning import Qlearning
from scripts.RescorlaWagner import RescorlaWagner

MAX_EXP = 700
MIN_LOG = 0.01


class Player:
    def __init__(self, **params):
        # params: type --> Dict[str, float]
        # params: alpha, T and so on
        self.Q_learning = Qlearning()
        self.Rescorla_Wagner = RescorlaWagner()
        self.params = params

    @abstractmethod
    def decide(self):
        pass

    @staticmethod
    def probability_A(Q_A, Q_B, T):
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


class RealPlayer:
    def __init__(self, path):
        self.data = self._read_real_player_excel(path)
        self.estimator = Estimator(decisions=self.data['Action'].tolist(),
                                   condition_left=self.data['StimulusLeft'].tolist(),
                                   condition_right=self.data['StimulusRight'].tolist(),
                                   rewards=self.data['Reward'].tolist())

    @staticmethod
    def _read_real_player_excel(path):
        data = read_excel(path, header=None)
        data = data.T
        data.columns = data.iloc[0]
        data = data.reindex(data.index.drop(0))
        data.drop(['StimulusPair'], axis=1, inplace=True)
        data.drop(['Response time'], axis=1, inplace=True)
        data = data[0:90]
        return data.astype(int)

    def search_parameters(self, model):
        return self.estimator.max_log_likelihood(model).x


class Estimator(Player):
    def __init__(self, decisions, condition_left, condition_right, rewards):
        super(Estimator, self).__init__()
        self.decisions = decisions
        self.rewards = rewards
        self.condition_left = condition_left
        self.condition_right = condition_right

    def log_likelihood_function(self, params, sign, model):
        T = params[0]
        log_likelihood = 0
        if model == 'Q_learning':
            model_method = self.Q_learning.q_learning_model
        elif model == 'Rescorla-Wagner':
            model_method = self.Rescorla_Wagner.rescorla_wagner_model
        for index, decision in enumerate(self.decisions):
            Q_A = self.Q_learning.Q_table[self.condition_left[index] - 1]
            p_a = self.probability_A(Q_A, 1 - Q_A, T)
            game_status = (self.condition_left[index], self.condition_right[index], decision, self.rewards[index])
            model_method(game_status, params)
            log_likelihood += sign * (
                decision * log(max(p_a, MIN_LOG)) + (1 - decision) * log(1 - min(p_a, 1 - MIN_LOG)))
        return log_likelihood

    def max_log_likelihood(self, model):
        if model == 'Q_learning':
            x0 = np.array([0.1, 0.1])
        elif model == 'Rescorla-Wagner':
            x0 = np.array([0.1, 0.1, 0.1])
        return minimize(self.log_likelihood_function, x0=x0, method='Nelder-Mead', args=(-1.0, model))


if __name__ == '__main__':
    rp = RealPlayer('/home/jczestochowska/workspace/ZPI/data/AniaPiateklearning.xls')
    print(rp.search_parameters('Q_learning'))
    print(rp.search_parameters('Rescorla-Wagner'))
