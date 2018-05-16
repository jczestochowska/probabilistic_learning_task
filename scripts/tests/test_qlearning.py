from unittest import TestCase

import numpy as np

from models import RescorlaWagner, Qlearning
from player import RealPlayer

TEST_DATA_PATH = "/home/jczestochowska/workspace/ZPI/scripts/tests/example_excel_data.xls"


class TestQlearning(TestCase):
    def setUp(self):
        self.real_player = RealPlayer(path=TEST_DATA_PATH, model=None)

    def test_q_table_values_q_learning(self):
        # given
        self.real_player.model = Qlearning()
        parameters = np.array([1, 0.1])
        expected = [-0.1, 0, 0.1, 0, 0.1, 0]
        # when
        self.real_player.log_likelihood_function(params=parameters)
        actual = self.real_player.model.Q_table
        # then
        self.assertEqual(actual, expected)

    def test_q_table_values_rescorla_wagner(self):
        # given
        self.real_player.model = RescorlaWagner()
        parameters = np.array([1, 1, 2])
        expected = [-2, 0, 1, 0, 1, 0]
        # when
        self.real_player.log_likelihood_function(params=parameters)
        actual = self.real_player.model.Q_table
        # then
        self.assertEqual(actual, expected)
