# from scripts.player import ModelAsPlayer3
# from scripts.game_session import GameSession

class QLearning():

    def __init__(self):
        self.Q_table = [0, 0, 0, 0, 0, 0]
        # self.decisions = self.decide.decisions
        self.decisions = [1, 2, 4, 5, 1]
        # self.reward_history = self._give_rewards.reward_history
        self.reward_history = [1, -1, 1, -1, 1]
        self.alpha = 0.2

    def update_q_table(self):
        for index in range(len(self.decisions)):
            game_skeleton = {'StimulusLeft': [1, 2, 3, 5, 2], 'StimulusRight': [2, 1, 4, 6, 1]}
            condition_left = game_skeleton['StimulusLeft']
            condition_right = game_skeleton['StimulusRight']
            left_card = condition_left[index]
            right_card = condition_right[index]
            current_reward = self.reward_history[index]
            current_decision = self.decisions[index]

            if current_decision == left_card:
                updated_value = self.Q_table[left_card] + self.alpha * (current_reward - self.Q_table[left_card])
                self.Q_table[left_card - 1] = updated_value
            elif current_decision == right_card:
                updated_value = self.Q_table[right_card] + self.alpha * (current_reward - self.Q_table[right_card])
                self.Q_table[right_card - 1] = updated_value

        return self.Q_table


if __name__ == '__main__':
    ql = QLearning()
    print(ql.update_q_table())
