from random import random

from pandas import read_excel

from models import Estimator, probability_A, Qlearning, RescorlaWagner


class VirtualPlayer:
    def __init__(self, game_skeleton, *params):
        # type (DataFrame, Tuple[float|int]) -> None
        self.condition_left = game_skeleton['StimulusLeft']
        self.condition_right = game_skeleton['StimulusRight']
        self.left_rewards = game_skeleton['LeftReward']
        self.right_rewards = game_skeleton['RightReward']
        self.better_stimulus = game_skeleton['BetterStimulus']
        self.decisions = []
        self.rewards = []
        self.correct_actions = []
        self.params = list(params)

    def decide(self, model):
        T = self.params[0]
        for index, condition_left in enumerate(self.condition_left):
            left_reward = self.left_rewards[index]
            right_reward = self.right_rewards[index]
            condition_right = self.condition_right[index]
            Q_A = model.Q_table[condition_left - 1]
            p_a = probability_A(Q_A, 1 - Q_A, T)
            decision = self._check_threshold(p_a)
            self._is_action_correct(decision, index)
            self.decisions.append(decision)
            reward = self.get_reward(decision, left_reward, right_reward)
            self.rewards.append(reward)
            game_status = {'StimuliLeft': condition_left, 'StimuliRight': condition_right,
                           'Action': decision, 'Reward': reward}
            model.update_q_table(game_status, self.params)
        return self.decisions

    @staticmethod
    def get_reward(decision, left_reward, right_reward):
        if decision == 1:
            reward = left_reward
        elif decision == 0:
            reward = right_reward
        if reward == 0:
            reward = -1
        return reward

    @staticmethod
    def _check_threshold(p_a):
        return int(random() < p_a)

    def _is_action_correct(self, decision, index):
        if decision == self.better_stimulus[index]:
            self.correct_actions.append(1)
        else:
            self.correct_actions.append(0)


class RealPlayer:
    def __init__(self, path, ):
        self.data = self._read_real_player_excel(path)

    @staticmethod
    def _read_real_player_excel(path):
        data = read_excel(path, header=None)
        data = data.T
        data.columns = data.iloc[0]
        data = data.reindex(data.index.drop(0))
        data.drop(['StimulusPair'], axis=1, inplace=True)
        data.drop(['Response time'], axis=1, inplace=True)
        data = data[0:90]
        return data.astype(int)

    def search_parameters(self, estimator):
        return estimator.max_log_likelihood().x


if __name__ == '__main__':
    rp = RealPlayer("/home/jczestochowska/workspace/ZPI/data/AniaPiateklearning.xls")
    model = Qlearning()
    estimator = Estimator(decisions=rp.data['Action'].tolist(),
                          condition_left=rp.data['StimulusLeft'].tolist(),
                          condition_right=rp.data['StimulusRight'].tolist(),
                          rewards=rp.data['Reward'].tolist(), model=model)
    print(rp.search_parameters(estimator))
