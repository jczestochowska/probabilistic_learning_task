import os
import random
import numpy as np
from math import floor

import pandas as pd


def which_stimulus():
    return 1

def play(cycle_number=10, maximum_blocks=3, training_cycle_length=3):

    filename = input("Podaj nazwę pliku (bez rozszerzenia): ")
    filename += ".csv"
    stimulus_history = []
    stimulus_history_left = []
    stimulus_history_right = []
    action_history = []
    correct_action_history = []
    reward_history = []
    probability_of_reward = [0.8, 0.2, 0.7, 0.3, 0.6, 0.4]

    for block in range(maximum_blocks):

        stimulus_block_history = [0] * (training_cycle_length*cycle_number)

        for cycle in range(cycle_number):
            pairs = list(range(1, training_cycle_length+1))
            random.shuffle(pairs)
            if cycle_number > 0:
                while pairs[0] == stimulus_block_history[training_cycle_length*(cycle-1)]:
                    random.shuffle(pairs)
            else:
                if block > 0:
                    while pairs[0] == stimulus_history[-1]:
                        random.shuffle(pairs)

            stimulus_block_history.extend(pairs)

        stimulus_block_history = [i for i in stimulus_block_history if i != 0]
        stimulus_history.extend(stimulus_block_history)

        RewardsGrantedA = [0] * cycle_number
        RewardsGrantedB = [0] * cycle_number
        RewardsGrantedC = [0] * cycle_number
        RewardsGrantedD = [0] * cycle_number
        RewardsGrantedE = [0] * cycle_number
        RewardsGrantedF = [0] * cycle_number
        RewardsGrantedA[1:floor(cycle_number*probability_of_reward[0])] = [1] * floor(cycle_number*probability_of_reward[0])
        RewardsGrantedB[1:floor(cycle_number*probability_of_reward[1])] = [1] * floor(cycle_number*probability_of_reward[1])
        RewardsGrantedC[1:floor(cycle_number*probability_of_reward[2])] = [1] * floor(cycle_number*probability_of_reward[2])
        RewardsGrantedD[1:floor(cycle_number*probability_of_reward[3])] = [1] * floor(cycle_number*probability_of_reward[3])
        RewardsGrantedE[1:floor(cycle_number*probability_of_reward[4])] = [1] * floor(cycle_number*probability_of_reward[4])
        RewardsGrantedF[1:floor(cycle_number*probability_of_reward[5])] = [1] * floor(cycle_number*probability_of_reward[5])
        RewardsGranted = np.zeros((2,training_cycle_length*cycle_number))

        for stimulus_set, set_index in enumerate(stimulus_history):
            if stimulus_set == 1:
                RewardsGranted[0, set_index] = random.choice(RewardsGrantedA)
                RewardsGranted[1, set_index] = random.choice(RewardsGrantedB)
            elif stimulus_set == 2:
                RewardsGranted[0, set_index] = random.choice(RewardsGrantedC)
                RewardsGranted[1, set_index] = random.choice(RewardsGrantedD)
            elif stimulus_set == 3:
                RewardsGranted[0, set_index] = random.choice(RewardsGrantedE)
                RewardsGranted[1, set_index] = random.choice(RewardsGrantedF)

        for attempt in range(training_cycle_length*cycle_number):
            attempt_rewards = RewardsGranted[:, attempt]
            if random.randint(0,2) == 1:
                left_stimulus_number = 2*stimulus_history[attempt]-1
                right_stimulus_number = 2*stimulus_history[attempt]
                left_reward_granted = attempt_rewards[0]
                right_reward_granted = attempt_rewards[1]
                better_stimulus = left_stimulus_number
            else:
                left_stimulus_number = 2*stimulus_history[attempt]
                right_stimulus_number = 2*stimulus_history[attempt]-1
                left_reward_granted = attempt_rewards[1]
                right_reward_granted = attempt_rewards[0]
                better_stimulus = right_stimulus_number

            action = which_stimulus()
            action_history.append(action)

            if action == better_stimulus:
                correct_action_history.append(1)
            else:
                correct_action_history.append(0)

            if action == 1:
                reward = left_reward_granted
            elif action == 0:
                reward = right_reward_granted

            if reward == 0:
                reward_history.append(-1)
            else:
                reward_history.append(reward)

            stimulus_history_left.append(left_stimulus_number)
            stimulus_history_right.append(right_stimulus_number)

    game_stats = {'StimulusHistory': stimulus_history, 'StimulusLeft': stimulus_history_left, 'StimulusRight': stimulus_history_right,
                 'Action': action_history, 'Was the Action Correct?': correct_action_history, 'Reward': reward_history}

    reward_history = list(map(int, reward_history))
    parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_file_path = os.path.join(parent_directory, "data", filename)
    pd.DataFrame(data=game_stats).to_csv(csv_file_path, index=False)

if __name__ == '__main__':
    play()