from abc import abstractmethod

from scripts.Qlearning import Qlearning

class Player:
    def __init__(self, **params ):
        # params: type --> Dict[str, float]
        # params: alpha, T and so on
        self.Q_learning = Qlearning()
        self.params = params

    @abstractmethod
    def decide(self, game_skeleton):
        pass

class VirtualPlayer(Player):
    pass

class ModelAsPlayer(Player):
    '''uses Q-learning module, holds responsibility for updating max-likelihood function, and optimizing its parameters'''
#     TODO: super init
    def decide(self, game_skeleton):
        return 90 * [1]

