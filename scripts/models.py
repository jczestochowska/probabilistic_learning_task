from math import exp, log
from scipy.optimize import minimize
import numpy as np

MAX_EXP = 700
MIN_LOG = 0.01


class Qlearning:
    def __init__(self, qtable_length=6):
        # type (int) -> None
        self.Q_table = qtable_length * [0]

    def q_learning_model(self, game_data, params):
        # type (Dict[str, int], List[int]) -> None
        alpha = params[-1]
        left_card = game_data['StimuliLeft']
        right_card = game_data['StimuliRight']
        decision = game_data['Action']
        current_reward = game_data['Reward']
        if decision == 1:
            self.Q_table[left_card - 1] = self.Q_table[left_card - 1] + alpha * (
                current_reward - self.Q_table[left_card - 1])
        elif decision == 0:
            self.Q_table[right_card - 1] = self.Q_table[right_card - 1] + alpha * (
                current_reward - self.Q_table[right_card - 1])


class RescorlaWagner(Qlearning):
    def rescorla_wagner_model(self, game_data, params):
        # type (Dict[str, int], List[int]) -> None
        reward = game_data['Reward']
        alpha = self._choose_alpha(params, reward)
        params[-1] = alpha
        self.q_learning_model(game_data, params)

    @staticmethod
    def _choose_alpha(params, reward):
        # type (List[int], int) -> int
        alpha_gain = params[1]
        alpha_lose = params[2]
        if reward == 1:
            return alpha_gain
        elif reward == -1:
            return alpha_lose


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
            game_status = {'StimuliLeft': self.condition_left[index],
                           'StimuliRight': self.condition_right[index],
                           'Action': decision,
                           'Reward': self.rewards[index]}
            model_method(game_status, params)
            log_likelihood += sign * (
                decision * log(max(p_a, MIN_LOG)) + (1 - decision) * log(1 - min(p_a, 1 - MIN_LOG)))
        return log_likelihood

    def max_log_likelihood(self):
        return minimize(self.log_likelihood_function, x0=self._get_optimization_start_points(), method='Nelder-Mead',
                        args=(-1.0))

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


def probability_A(Q_A, Q_B, T):
    return 1 / (1 + exp(min((Q_B - Q_A) / T, MAX_EXP)))


if __name__ == '__main__':
    ql = Qlearning()
    rw = RescorlaWagner()
    print(ql.q_learning_model(game_data={'StimuliLeft': 1, 'StimuliRight': 2, 'Action': 1, 'Reward': -1},
                              params=[0.1, 0.1, 0.1]))
