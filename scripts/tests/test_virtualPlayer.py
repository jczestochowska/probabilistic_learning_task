from unittest import TestCase, mock
from unittest.mock import patch, call

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

    @patch('player.VirtualPlayer.simulate_game')
    def test_decide(self, simulate_game_mock):
        # given
        simulate_game_calls = [call(1, 5, 0, self.virtual_player.model),
                               call(1, 4, 1, self.virtual_player.model),
                               call(1, 1, 2, self.virtual_player.model)]
        self.virtual_player.decide()
        simulate_game_mock.assert_has_calls(simulate_game_calls, any_order=False)

    @patch('player.VirtualPlayer._check_threshold')
    def test_simulation_adds_proper_decision(self, threshold_mock):
        # given
        threshold_mock.return_value = 1
        T = 0.2
        condition_left = self.virtual_player.condition_left[0]
        index = 0
        model = self.virtual_player.model
        expected = [1]
        # when
        self.virtual_player.simulate_game(T, condition_left, index, model)
        # then
        self.assertEqual(self.virtual_player.decisions, expected)

    @patch('player.VirtualPlayer._check_threshold')
    def test_simulation_gives_proper_reward(self, threshold_mock):
        # given
        threshold_mock.return_value = 1
        T = 0.2
        condition_left = self.virtual_player.condition_left[0]
        index = 0
        model = self.virtual_player.model
        expected = [1]
        # when
        self.virtual_player.simulate_game(T, condition_left, index, model)
        # then
        self.assertEqual(self.virtual_player.rewards, expected)

    def test_get_left_reward(self):
        # given
        expected = 1
        # when
        actual = self.virtual_player.get_reward(1, 1, 0)
        # then
        self.assertEqual(actual, expected)

    def test_get_right_reward(self):
        # given
        expected = -1
        # when
        actual = self.virtual_player.get_reward(0, 1, 0)
        # then
        self.assertEqual(actual, expected)

    @patch('player.random')
    def test_check_threshold(self, random_mock):
        # given
        random_mock.return_value = 0.5
        p_a = 0.2
        expected = 0
        # when
        actual = self.virtual_player._check_threshold(p_a)
        # then
        self.assertEqual(actual, expected)

    def test_is_left_action_correct(self):
        # given
        decision = 1
        index = 0
        expected = [1]
        # when
        self.virtual_player._is_action_correct(decision, index)
        # then
        actual = self.virtual_player.correct_actions
        self.assertEqual(actual, expected)

    def test_is_right_action_correct(self):
        # given
        decision = 0
        index = 0
        expected = [0]
        # when
        self.virtual_player._is_action_correct(decision, index)
        # then
        actual = self.virtual_player.correct_actions
        self.assertEqual(actual, expected)
