import os
from unittest import TestCase
from unittest.mock import Mock, patch

import numpy as np
import pandas as pd
from numpy.testing import assert_array_equal

from models import Qlearning, RescorlaWagner
from player import RealPlayer

TEST_DATA_PATH = TEST_DATA_PATH = os.path.dirname(os.path.abspath(__file__)) + "/example_excel_data.xls"


class TestRealPlayer(TestCase):
    def setUp(self):
        self.real_player = RealPlayer(TEST_DATA_PATH, model=Mock())

    def test_read_real_player_excel(self):
        expected = pd.DataFrame({'StimulusLeft': [5, 4, 1],
                                 'StimulusRight': [6, 3, 2],
                                 'Action': [1, 0, 1],
                                 'Was the Action Correct?': [1, 1, 1],
                                 'Reward': [1, 1, -1]}).sort_index(inplace=True)
        actual = RealPlayer._read_real_player_excel(TEST_DATA_PATH).sort_index(inplace=True)
        self.assertEqual(actual, expected)

    @patch('player.minimize')
    def test_max_log_likelihood(self, mock_minimize):
        # given
        start_points = [3, 0.2]
        self.real_player.model = Qlearning()
        # when
        self.real_player.max_log_likelihood(start_points=start_points)
        # then
        mock_minimize.assert_called_once_with(self.real_player.log_likelihood_function,
                                              x0=start_points,
                                              method='Nelder-Mead')

    @patch('player.minimize')
    def test_max_log_likelihood_with_default_starting_points(self, mock_minimize):
        # given
        default_start_points = np.array([1, 0.1])
        self.real_player.model = Qlearning()
        # when
        self.real_player.max_log_likelihood()
        # then
        mock_minimize.assert_called_once()
        assert_array_equal(mock_minimize.call_args[1]['x0'], default_start_points)

    def test_get_optimized_parameters_for_q_learning(self):
        # given
        self.real_player.model = Qlearning()
        # when
        actual = self.real_player.get_optimized_parameters()
        # then
        self.assertIsInstance(actual, np.ndarray)
        self.assertEqual(len(actual), 2)

    def test_get_optimized_parameters_for_rescorla_wagner(self):
        # given
        self.real_player.model = RescorlaWagner()
        # when
        actual = self.real_player.get_optimized_parameters()
        # then
        self.assertIsInstance(actual, np.ndarray)
        self.assertEqual(len(actual), 3)

    def test_log_likelihood_function_q_learning(self):
        # given
        self.real_player.model = Qlearning()
        parameters = np.array([1, 0.1])
        expected = -1 * (3 * np.log(1 / 2))
        # when
        actual = self.real_player.log_likelihood_function(params=parameters)
        # then
        self.assertEqual(actual, expected)

    def test_log_likelihood_function_rescorla_wagner(self):
        # given
        self.real_player.model = RescorlaWagner()
        parameters = np.array([1, 1, 2])
        expected = -1 * (3 * np.log(1 / 2))
        # when
        actual = self.real_player.log_likelihood_function(params=parameters)
        # then
        self.assertEqual(actual, expected)

    def test_get_default_optimization_start_points_for_Q_learning(self):
        real_player = RealPlayer(TEST_DATA_PATH, model=Qlearning())
        assert_array_equal(real_player.start_points, np.array([1, 0.1]))

    def test_get_default_optimization_start_points_for_rescorla_wagner(self):
        real_player = RealPlayer(TEST_DATA_PATH, model=RescorlaWagner())
        assert_array_equal(real_player.start_points, np.array([1, 0.1, 0.1]))
