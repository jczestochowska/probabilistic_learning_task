from math import exp, log

MAX_EXP = 700
MIN_LOG = 0.01


class Qlearning:
    def __init__(self, qtable_length=6):
        # type (int) -> None
        self.Q_table = qtable_length * [0]

    def update_q_table(self, game_data, params):
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

    def reset_qtable(self):
        return [q * 0 for q in self.Q_table]


class RescorlaWagner(Qlearning):
    def update_q_table(self, game_data, params):
        # type (Dict[str, int], List[int]) -> None
        reward = game_data['Reward']
        T, alpha_gain, alpha_lose = params
        if reward == 1:
            params_to_qtable = (T, alpha_gain)
        elif reward == -1:
            params_to_qtable = (T, alpha_lose)
        super().update_q_table(game_data, params_to_qtable)


def probability_A(Q_A, Q_B, T):
    if T == 0 or (1 + exp(min((Q_B - Q_A) / T, MAX_EXP))) == 0:
        probability = 0
    else:
        probability = 1 / (1 + exp(min((Q_B - Q_A) / T, MAX_EXP)))
    return probability


def AIC(model, max_loglikelihood_value):
    q = parameters_number(model)
    return abs(2 * q - 2 * max_loglikelihood_value)


def pseudoR_squared(max_loglikelihood_value, session_length):
    r = log(0.5) * session_length
    return abs((max_loglikelihood_value - r) / r)


def parameters_number(model):
    if isinstance(model, RescorlaWagner):
        params_number = 3
    else:
        params_number = 2
    return params_number
