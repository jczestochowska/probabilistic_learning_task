class Qlearning(object):
    def __init__(self):
        self.Q_table = [0, 0, 0, 0, 0, 0]

    def update_q_table(self, left_card, right_card, decision, current_reward, alpha):
        if decision == 1:
            updated_value = self.Q_table[left_card - 1] + alpha * (current_reward - self.Q_table[left_card - 1])
            self.Q_table[left_card - 1] = updated_value
        elif decision == 0:
            updated_value = self.Q_table[right_card - 1] + alpha * (current_reward - self.Q_table[right_card - 1])
            self.Q_table[right_card - 1] = updated_value
        return self.Q_table


if __name__ == '__main__':
    ql = Qlearning()
    print(ql.update_q_table(1, 2, 1, -1, 0.1))
