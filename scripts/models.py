from math import exp

MAX_EXP = 700

class Qlearning:
    def __init__(self, qtable_length=6):
        self.Q_table = qtable_length * [0]

    def q_learning_model(self, game_data, alpha):
        left_card, right_card, decision, current_reward = game_data
        if decision == 1:
            self.Q_table[left_card - 1] = self.Q_table[left_card - 1] + alpha * (
                current_reward - self.Q_table[left_card - 1])
        elif decision == 0:
            self.Q_table[right_card - 1] = self.Q_table[right_card - 1] + alpha * (
                current_reward - self.Q_table[right_card - 1])


class RescorlaWagner(Qlearning):
    def rescorla_wagner_model(self, game_data, params):
        reward = game_data[-1]
        alpha = self._choose_alpha(params, reward)
        self.q_learning_model(game_data, alpha)

    def _choose_alpha(self, params, reward):
        _, alpha_gain, alpha_lose = params
        if reward == 1:
            return alpha_gain
        elif reward == -1:
            return alpha_lose


def probability_A(Q_A, Q_B, T):
    return 1 / (1 + exp(min((Q_B - Q_A) / T, MAX_EXP)))


if __name__ == '__main__':
    ql = Qlearning()
    rw = RescorlaWagner()
    print(rw.rescorla_wagner_model((1, 2, 1, -1), (0.1, 0.1, 0.1)))
