from unittest import TestCase

from models import Qlearning
from player import VirtualPlayer
import pandas as pd


class TestVirtualPlayer(TestCase):
    def setUp(self):
        self.virtual_player = VirtualPlayer(1, 0.1, model=Qlearning(),
                                            game_skeleton=pd.DataFrame({'StimulusLeft': [5, 4, 1],
                                                                        'StimulusRight': [6, 3, 2],
                                                                        'LeftReward': [1, -1, 1],
                                                                        'BetterStimulus': [1, 1, 1],
                                                                        'RightReward': [1, 1, -1]}))

    def test_decide(self):
        self.fail()

    def test_simulate_game(self):
        self.fail()

    def test_get_reward(self):
        # given
        expected = 1
        # when
        actual = self.virtual_player.get_reward(1, 1, -1)
        # then
        self.assertEqual(actual, expected)

    def test__check_threshold(self):
        self.fail()

    def test__is_action_correct(self):
        self.fail()
