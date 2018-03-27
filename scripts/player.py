from math import log
from random import random

import numpy as np
from pandas import read_excel
from scipy.optimize import minimize

from scripts.models import probability_A, RescorlaWagner, Qlearning

MIN_LOG = 0.01


class VirtualPlayer:
    def __init__(self, game_skeleton, **params):
        self.condition_left = game_skeleton['StimulusLeft']
        self.condition_right = game_skeleton['StimulusRight']
        self.left_rewards = game_skeleton['LeftReward']
        self.right_rewards = game_skeleton['RightReward']
        self.better_stimulus = game_skeleton['BetterStimulus']
        self.decisions = []
        self.rewards = []
        self.correct_actions = []
        self.params = params

    def decide(self, model):
        T, alpha = self.params.values()
        for index, condition_left in enumerate(self.condition_left):
            left_reward = self.left_rewards[index]
            right_reward = self.right_rewards[index]
            condition_right = self.condition_right[index]
            Q_A = model.Q_table[condition_left - 1]
            p_a = probability_A(Q_A, 1 - Q_A, T)
            decision = self._check_threshold(p_a)
            self._is_action_correct(decision, index)
            self.decisions.append(decision)
            reward = self.get_reward(decision, left_reward, right_reward)
            self.rewards.append(reward)
            model.q_learning_model((condition_left, condition_right, decision, reward), alpha)
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
    def __init__(self, path, ):
        self.data = self._read_real_player_excel(path)

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

    def search_parameters(self, model, estimator):
        return estimator.max_log_likelihood(model).x


class Estimator:
    def __init__(self, decisions, condition_left, condition_right, rewards, model):
        self.decisions = decisions
        self.rewards = rewards
        self.condition_left = condition_left
        self.condition_right = condition_right
        self.model = model

    def log_likelihood_function(self, params, sign):
        T = params[0]
        log_likelihood = 0
        model_method = self._resolve_model_method()
        for index, decision in enumerate(self.decisions):
            Q_A = self.model.Q_table[self.condition_left[index] - 1]
            p_a = probability_A(Q_A, 1 - Q_A, T)
            game_status = (self.condition_left[index], self.condition_right[index], decision, self.rewards[index])
            model_method(game_status, params)
            log_likelihood += sign * (
                decision * log(max(p_a, MIN_LOG)) + (1 - decision) * log(1 - min(p_a, 1 - MIN_LOG)))
        return log_likelihood

    def max_log_likelihood(self, model):
        return minimize(self.log_likelihood_function, x0=self._get_optimization_start_points(), method='Nelder-Mead',
                        args=(-1.0,))

    def _resolve_model_method(self):
        if isinstance(self.model, RescorlaWagner):
            model_method = self.model.rescorla_wagner_model
        else:
            model_method = self.model.q_learning_model
        return model_method

    def _get_optimization_start_points(self):
        if isinstance(self.model, RescorlaWagner):
            x0 = np.array([0.1, 0.1, 0.1])
        else:
            x0 = np.array([0.1, 0.1])
        return x0


if __name__ == '__main__':
    rp = RealPlayer("C:\\Users\\Marlena\\Desktop\\studia\\6 semestr\\ZPI\\gra ZPI\\wyniki\\EwaDudalearning.xls")
    model = RescorlaWagner()
    estimator = Estimator(decisions=rp.data['Action'].tolist(),
                          condition_left=rp.data['StimulusLeft'].tolist(),
                          condition_right=rp.data['StimulusRight'].tolist(),
                          rewards=rp.data['Reward'].tolist(), model=model)
    print(rp.search_parameters(model, estimator))
