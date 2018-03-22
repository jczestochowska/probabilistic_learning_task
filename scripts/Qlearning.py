class Qlearning():
    def __init__(self):
        self.Q_table = [0, 0, 0, 0, 0, 0]

    def q_learning_model(self, game_data, params):
        _,alpha = params
        left_card, right_card, decision, current_reward = game_data
        if decision == 1:
            self.Q_table[left_card - 1] = self.Q_table[left_card - 1] + alpha * (current_reward - self.Q_table[left_card - 1])
        elif decision == 0:
            self.Q_table[right_card - 1] = self.Q_table[right_card - 1] + alpha * (current_reward - self.Q_table[right_card - 1])
        return self.Q_table


if __name__ == '__main__':
    ql = Qlearning()
    print(ql.q_learning_model((1, 2, 1, -1), (0.1,0.1)))
