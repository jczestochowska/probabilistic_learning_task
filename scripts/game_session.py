import os
import random
import numpy as np
from math import floor

import pandas as pd


class GameSession:
    def __init__(self, cycle_number=10, maximum_blocks=3, training_cycle_length=3):
        self.cycle_number = cycle_number
        self.maximum_blocks = maximum_blocks
        self.training_cycle_length = training_cycle_length
        self.stimulus_history = []
        self.stimulus_history_left = []
        self.stimulus_history_right = []
        self.action_history = []
        self.correct_action_history = []
        self.reward_history = []

    def decide(self):
        return 1

    def play(self):
        for block in range(self.maximum_blocks):
            self.prepare_block(block)
            for attempt in range(self.training_cycle_length * self.cycle_number):
                attempt_rewards = self.RewardsGranted[:, attempt]
                if random.randint(0, 2) == 1:
                    left_stimulus_number = 2 * self.stimulus_history[attempt] - 1
                    right_stimulus_number = 2 * self.stimulus_history[attempt]
                    left_reward_granted = attempt_rewards[0]
                    right_reward_granted = attempt_rewards[1]
                    better_stimulus = 1
                else:
                    left_stimulus_number = 2 * self.stimulus_history[attempt]
                    right_stimulus_number = 2 * self.stimulus_history[attempt] - 1
                    left_reward_granted = attempt_rewards[1]
                    right_reward_granted = attempt_rewards[0]
                    better_stimulus = 0

                action = self.decide()
                self.action_history.append(action)

                if action == better_stimulus:
                    self.correct_action_history.append(1)
                else:
                    self.correct_action_history.append(0)

                if action == 1:
                    reward = left_reward_granted
                elif action == 0:
                    reward = right_reward_granted

                if reward == 0:
                    self.reward_history.append(-1)
                else:
                    self.reward_history.append(reward)

                self.stimulus_history_left.append(left_stimulus_number)
                self.stimulus_history_right.append(right_stimulus_number)

        self.reward_history = list(map(int, self.reward_history))

    def prepare_block(self, block):
        probability_of_reward = [0.8, 0.2, 0.7, 0.3, 0.6, 0.4]
        stimulus_block_history = [0] * (self.training_cycle_length * self.cycle_number)
        for cycle in range(self.cycle_number):
            pairs = list(range(1, self.training_cycle_length + 1))
            random.shuffle(pairs)
            if self.cycle_number > 0:
                while pairs[0] == stimulus_block_history[self.training_cycle_length * (cycle - 1)]:
                    random.shuffle(pairs)
            else:
                if block > 0:
                    while pairs[0] == self.stimulus_history[-1]:
                        random.shuffle(pairs)

            stimulus_block_history.extend(pairs)

        stimulus_block_history = [i for i in stimulus_block_history if i != 0]
        self.stimulus_history.extend(stimulus_block_history)

        RewardsGrantedA = [0] * self.cycle_number
        RewardsGrantedB = [0] * self.cycle_number
        RewardsGrantedC = [0] * self.cycle_number
        RewardsGrantedD = [0] * self.cycle_number
        RewardsGrantedE = [0] * self.cycle_number
        RewardsGrantedF = [0] * self.cycle_number
        RewardsGrantedA[1:floor(self.cycle_number * probability_of_reward[0])] \
            = [1] * floor(self.cycle_number * probability_of_reward[0])
        RewardsGrantedB[1:floor(self.cycle_number * probability_of_reward[1])] \
            = [1] * floor(self.cycle_number * probability_of_reward[1])
        RewardsGrantedC[1:floor(self.cycle_number * probability_of_reward[2])] \
            = [1] * floor(self.cycle_number * probability_of_reward[2])
        RewardsGrantedD[1:floor(self.cycle_number * probability_of_reward[3])] \
            = [1] * floor(self.cycle_number * probability_of_reward[3])
        RewardsGrantedE[1:floor(self.cycle_number * probability_of_reward[4])] \
            = [1] * floor(self.cycle_number * probability_of_reward[4])
        RewardsGrantedF[1:floor(self.cycle_number * probability_of_reward[5])] \
            = [1] * floor(self.cycle_number * probability_of_reward[5])
        RewardsGranted = np.zeros((2, self.training_cycle_length * self.cycle_number))

        for stimulus_set, set_index in enumerate(self.stimulus_history):
            if stimulus_set == 1:
                RewardsGranted[0, set_index] = random.choice(RewardsGrantedA)
                RewardsGranted[1, set_index] = random.choice(RewardsGrantedB)
            elif stimulus_set == 2:
                RewardsGranted[0, set_index] = random.choice(RewardsGrantedC)
                RewardsGranted[1, set_index] = random.choice(RewardsGrantedD)
            elif stimulus_set == 3:
                RewardsGranted[0, set_index] = random.choice(RewardsGrantedE)
                RewardsGranted[1, set_index] = random.choice(RewardsGrantedF)

        for stimulus_set, set_index in enumerate(self.stimulus_history):
            if stimulus_set == 1:
                RewardsGranted[0, set_index] = random.choice(RewardsGrantedA)
                RewardsGranted[1, set_index] = random.choice(RewardsGrantedB)
            elif stimulus_set == 2:
                RewardsGranted[0, set_index] = random.choice(RewardsGrantedC)
                RewardsGranted[1, set_index] = random.choice(RewardsGrantedD)
            elif stimulus_set == 3:
                RewardsGranted[0, set_index] = random.choice(RewardsGrantedE)
                RewardsGranted[1, set_index] = random.choice(RewardsGrantedF)

        self.RewardsGranted = RewardsGranted

    def save_results(self):
        self.create_result()
        self.result.to_csv(self.create_file_path(), index=False)

    @staticmethod
    def create_file_path():
        filename = input("Podaj nazwę pliku (bez rozszerzenia): ")
        filename += ".csv"
        parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(parent_directory, "data", filename)

    def create_result(self):
        game_stats = {'StimulusHistory': self.stimulus_history, 'StimulusLeft': self.stimulus_history_left,
                      'StimulusRight': self.stimulus_history_right,
                      'Action': self.action_history, 'Was the Action Correct?': self.correct_action_history,
                      'Reward': self.reward_history}
        self.result = pd.DataFrame(data=game_stats)

if __name__ == '__main__':
    game = GameSession()
    game.play()
    game.save_results()
