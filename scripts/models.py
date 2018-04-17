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


class RescorlaWagner(Qlearning):
    def update_q_table(self, game_data, params):
        # type (Dict[str, int], List[int]) -> None
        reward = game_data['Reward']
        alpha = self._choose_alpha(params, reward)
        params[-1] = alpha
        super().update_q_table(game_data, params)

    @staticmethod
    def _choose_alpha(params, reward):
        # type (List[int], int) -> int
        alpha_gain = params[1]
        alpha_lose = params[2]
        if reward == 1:
            return alpha_gain
        elif reward == -1:
            return alpha_lose


def probability_A(Q_A, Q_B, T):
    return 1 / (1 + exp(min((Q_B - Q_A) / T, MAX_EXP)))
