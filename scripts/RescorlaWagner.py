from scripts.Qlearning import Qlearning


class RescorlaWagner(Qlearning):
    def __init__(self):
        super(RescorlaWagner, self).__init__()

    def choose_alpha(self, params, reward):
        _, alpha_gain, alpha_lose = params
        if reward == 1:
            return alpha_gain
        elif reward == -1:
            return alpha_lose

    def rescorla_wagner_model(self, game_data, params):
        _, _, _, reward = game_data
        alpha = self.choose_alpha(params, reward)
        self.q_learning_model(game_data, (_, alpha))
        return self.Q_table


if __name__ == '__main__':
    rw = RescorlaWagner()
    print(rw.rescorla_wagner_model((1, 2, 1, -1), (0.1, 0.1,0.1)))
