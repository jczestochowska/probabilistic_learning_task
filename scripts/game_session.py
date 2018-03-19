import os
import random
import numpy as np
from math import floor

import pandas as pd

from player import Player, ModelAsPlayer


class GameSession:
    def __init__(self, player, cycle_number=10, maximum_blocks=3, training_cycle_length=3):
        self.probability_of_reward = [0.8, 0.2, 0.7, 0.3, 0.6, 0.4]
        self.cycle_number = cycle_number
        self.maximum_blocks = maximum_blocks
        self.training_cycle_length = training_cycle_length
        self.stimulus_history = []
        self.stimulus_history_left = []
        self.stimulus_history_right = []
        self.action_history = []
        self.correct_action_history = []
        self.reward_history = []
        self.better_stimulus = []
        self.RewardsGranted = np.zeros(shape=(2, 90))
        self._create_game_skeleton()
        self.player = player(self.game_skeleton)

    def play(self):
        self.player.decide()
        self.action_history = self.player.decisions
        self.reward_history = self.player.rewards
        self.correct_action_history = self.player.correct_actions

    def _create_game_skeleton(self):
        for block in range(self.maximum_blocks):
            self._prepare_block(block)
            for attempt in range(self.training_cycle_length * self.cycle_number):
                if random.randint(0, 2) == 1:
                    left_stimulus_number = 2 * self.stimulus_history[attempt] - 1
                    right_stimulus_number = 2 * self.stimulus_history[attempt]
                    better_stimulus = 1
                else:
                    left_stimulus_number = 2 * self.stimulus_history[attempt]
                    right_stimulus_number = 2 * self.stimulus_history[attempt] - 1
                    better_stimulus = 0

                self.stimulus_history_left.append(left_stimulus_number)
                self.stimulus_history_right.append(right_stimulus_number)
                self.better_stimulus.append(better_stimulus)
        left_rewards, right_rewards = self._create_rewards_skeleton()

        game_skeleton = {'StimulusHistory': self.stimulus_history, 'StimulusLeft': self.stimulus_history_left,
                         'StimulusRight': self.stimulus_history_right, 'BetterStimulus': self.better_stimulus,
                         'LeftReward': left_rewards, 'RightReward': right_rewards}
        self.game_skeleton = pd.DataFrame(data=game_skeleton)

    def _prepare_block(self, block):
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

        stimulus_block_history = list(filter(lambda x: x != 0, stimulus_block_history))
        self.stimulus_history.extend(stimulus_block_history)

    def _create_rewards_skeleton(self):
        left_rewards = []
        right_rewards = []
        for block in range(self.maximum_blocks):
            RewardsGrantedA = [0] * self.cycle_number
            RewardsGrantedB = [0] * self.cycle_number
            RewardsGrantedC = [0] * self.cycle_number
            RewardsGrantedD = [0] * self.cycle_number
            RewardsGrantedE = [0] * self.cycle_number
            RewardsGrantedF = [0] * self.cycle_number
            RewardsGrantedA[1:floor(self.cycle_number * self.probability_of_reward[0])] \
                = [1] * (floor(self.cycle_number * self.probability_of_reward[0]) - 1)
            RewardsGrantedB[1:floor(self.cycle_number * self.probability_of_reward[1])] \
                = [1] * (floor(self.cycle_number * self.probability_of_reward[1]) - 1)
            RewardsGrantedC[1:floor(self.cycle_number * self.probability_of_reward[2])] \
                = [1] * (floor(self.cycle_number * self.probability_of_reward[2]) - 1)
            RewardsGrantedD[1:floor(self.cycle_number * self.probability_of_reward[3])] \
                = [1] * (floor(self.cycle_number * self.probability_of_reward[3]) - 1)
            RewardsGrantedE[1:floor(self.cycle_number * self.probability_of_reward[4])] \
                = [1] * (floor(self.cycle_number * self.probability_of_reward[4]) - 1)
            RewardsGrantedF[1:floor(self.cycle_number * self.probability_of_reward[5])] \
                = [1] * (floor(self.cycle_number * self.probability_of_reward[5]) - 1)
            RewardsGranted = np.zeros((2, self.training_cycle_length * self.cycle_number))
            stimulus_block_history = self.stimulus_history[30 * block: 30 * (block + 1)]

            RewardsGrantedA = np.reshape(np.array(RewardsGrantedA), (1, len(RewardsGrantedA)))
            RewardsGrantedB = np.reshape(np.array(RewardsGrantedB), (1, len(RewardsGrantedB)))
            RewardsGrantedC = np.reshape(np.array(RewardsGrantedC), (1, len(RewardsGrantedC)))
            RewardsGrantedD = np.reshape(np.array(RewardsGrantedD), (1, len(RewardsGrantedD)))
            RewardsGrantedE = np.reshape(np.array(RewardsGrantedE), (1, len(RewardsGrantedE)))
            RewardsGrantedF = np.reshape(np.array(RewardsGrantedF), (1, len(RewardsGrantedF)))

            for stimulus_set in stimulus_block_history:
                idx = np.array(
                    [index for index, value in enumerate(stimulus_block_history) if value == stimulus_set])
                random_indexes = np.random.choice(self.cycle_number, (1, self.cycle_number), False)
                random_indexes = random_indexes[0]
                if stimulus_set == 1:
                    RewardsGranted[0, idx] = RewardsGrantedA[0, random_indexes]
                    RewardsGranted[1, idx] = RewardsGrantedB[0, random_indexes]
                elif stimulus_set == 2:
                    RewardsGranted[0, idx] = RewardsGrantedC[0, random_indexes]
                    RewardsGranted[1, idx] = RewardsGrantedD[0, random_indexes]
                elif stimulus_set == 3:
                    RewardsGranted[0, idx] = RewardsGrantedE[0, random_indexes]
                    RewardsGranted[1, idx] = RewardsGrantedF[0, random_indexes]

            self.RewardsGranted[:, 30 * block: 30 * (block + 1)] = RewardsGranted

        for index, better_stimuli in enumerate(self.better_stimulus):
            if better_stimuli == 1:
                left_rewards.append(self.RewardsGranted[0, index])
                right_rewards.append(self.RewardsGranted[1, index])
            elif better_stimuli == 0:
                left_rewards.append(self.RewardsGranted[1, index])
                right_rewards.append(self.RewardsGranted[0, index])

        return left_rewards, right_rewards

    def save_results(self):
        self._create_result()
        self.result.to_csv(self._create_file_path(), index=False)

    def _create_result(self):
        self.reward_history = list(map(int, self.reward_history))
        game_stats = {'StimulusHistory': self.stimulus_history, 'StimulusLeft': self.stimulus_history_left,
                      'StimulusRight': self.stimulus_history_right,
                      'Action': self.action_history, 'Was the Action Correct?': self.correct_action_history,
                      'Reward': self.reward_history}
        self.result = pd.DataFrame(data=game_stats)

    @staticmethod
    def _create_file_path():
        filename = input("Podaj nazwę pliku (bez rozszerzenia): ")
        filename += ".csv"
        parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(parent_directory, "data", filename)


if __name__ == '__main__':
    game = GameSession(player=ModelAsPlayer)
    game.play()
    game.save_results()
