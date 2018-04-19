from math import log
from random import random

import numpy as np
from pandas import read_excel
from scipy.optimize import minimize

from scripts.models import probability_A, AIC, pseudoR_squared, RescorlaWagner

MAX_EXP = 700
MIN_LOG = 0.01


class RealPlayer:
    def __init__(self, path, model):
        data = self._read_real_player_excel(path)
        self.decisions = data['Action'].tolist()
        self.condition_left = data['StimulusLeft'].tolist()
        self.condition_right = data['StimulusRight'].tolist()
        self.rewards = data['Reward'].tolist()
        self.model = model
        self.start_points = self._get_default_optimization_start_points()

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

    def max_log_likelihood(self, start_points=None):
        if not start_points:
            start_points = self._get_default_optimization_start_points()
        return minimize(self.log_likelihood_function, x0=start_points, method='Nelder-Mead')

    def get_optimized_parameters(self):
        return self.max_log_likelihood().x

    def log_likelihood_function(self, params, sign=-1):
        self.model.Q_table = self.model.reset_qtable()
        T = params[0]
        log_likelihood = 0
        for index, decision in enumerate(self.decisions):
            Q_A = self.model.Q_table[self.condition_left[index] - 1]
            Q_B = self.model.Q_table[self.condition_right[index] - 1]
            p_a = probability_A(Q_A, Q_B, T)
            game_status = {'StimuliLeft': self.condition_left[index],
                           'StimuliRight': self.condition_right[index],
                           'Action': decision,
                           'Reward': self.rewards[index]}
            self.model.update_q_table(game_status, params)
            log_likelihood += sign * (
                decision * log(max(p_a, MIN_LOG)) + (1 - decision) * log(1 - min(p_a, 1 - MIN_LOG)))
        return log_likelihood

    def _get_default_optimization_start_points(self):
        if isinstance(self.model, RescorlaWagner):
            x0 = np.array([1, 0.1, 0.1])
        else:
            x0 = np.array([1, 0.1])
        return x0

    def model_selection(self):
        loglikelihood_value = self.max_log_likelihood().fun * (-1)
        AIC_value = AIC(model=self.model, max_loglikelihood_value=loglikelihood_value)
        pR2 = pseudoR_squared(max_loglikelihood_value=loglikelihood_value, session_length=len(self.decisions),
                              likelihood_null=self.loglikelihood_null())
        return {'LogLikelihood': loglikelihood_value, 'AIC': AIC_value, 'pseudoR-quadratic': pR2}

    def loglikelihood_null(self):
        p_a = self.probability_A_null()
        return log(p_a ** sum(self.decisions) * (1 - p_a) ** (len(self.decisions) - sum(self.decisions)))

    def probability_A_null(self):
        return sum(self.decisions) / len(self.decisions)


class VirtualPlayer(RealPlayer):
    def __init__(self, *params, model, game_skeleton):
        # type (DataFrame, Tuple[float|int]) -> None
        self.condition_left = game_skeleton['StimulusLeft']
        self.condition_right = game_skeleton['StimulusRight']
        self.left_rewards = game_skeleton['LeftReward']
        self.right_rewards = game_skeleton['RightReward']
        self.better_stimulus = game_skeleton['BetterStimulus']
        self.decisions = []
        self.rewards = []
        self.correct_actions = []
        self.params = list(params)
        self.model = model

    def decide(self, ):
        T = self.params[0]
        for index, condition_left in enumerate(self.condition_left):
            self.simulate_game(T, condition_left, index, self.model)

    def simulate_game(self, T, condition_left, index, model):
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
        game_status = {'StimuliLeft': condition_left, 'StimuliRight': condition_right,
                       'Action': decision, 'Reward': reward}
        model.update_q_table(game_status, self.params)

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


class ModelPlayer(VirtualPlayer):
    def decide(self):
        T = self.params[0]
        for index, condition_left in enumerate(self.condition_left):
            self.simulate_game(T, condition_left, index, self.model)
            self.get_optimized_parameters()
            self.params = self.get_optimized_parameters()
