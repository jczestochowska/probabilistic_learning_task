from itertools import product
from scipy.optimize import minimize

import numpy as np
import os
import csv

from scripts.models import Qlearning, RescorlaWagner
from scripts.player import Estimator, RealPlayer


def save_optimal_params(data_dir_path, model, new_filename):
    all_filenames = os.listdir(data_dir_path)
    with open('{}.csv'.format(new_filename), 'w') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(get_header(model))
        for filename in all_filenames:
            if filename.endswith('xls'):
                row = []
                rp = RealPlayer(os.path.join(data_dir_path, filename))
                estimator = Estimator(decisions=rp.data['Action'].tolist(),
                                      condition_left=rp.data['StimulusLeft'].tolist(),
                                      condition_right=rp.data['StimulusRight'].tolist(),
                                      rewards=rp.data['Reward'].tolist(),
                                      model=model)
                player_name = os.path.splitext(os.path.basename(filename))[0][:-8]
                player_parameters = optimal_parameters(estimator, model)
                row.append(player_name)
                row.extend(player_parameters)
                writer.writerow(row)


def optimal_parameters(estimator, model):
    optimal_func_value = []
    optimal_params = []
    for start_points in get_start_points_list(model):
        max_loglikelihood = minimize(estimator.log_likelihood_function, x0=np.array(start_points), method='Nelder-Mead',
                                     args=(-1.0,))
        optimal_func_value.append(max_loglikelihood.fun)
        optimal_params.append(max_loglikelihood.x)
    max_value_index = optimal_func_value.index(max(optimal_func_value))
    return optimal_params[max_value_index]


def get_start_points_list(model):
    T_array = np.arange(1, 10, 1)
    if isinstance(model, RescorlaWagner):
        alpha_gain = np.arange(0.1, 1.0, 0.1)
        alpha_lose = np.arange(0.1, 1.0, 0.1)
        start_points_list = list(product(T_array, alpha_gain, alpha_lose))
    else:
        alpha_array = np.arange(0.1, 1.0, 0.1)
        start_points_list = list(product(T_array, alpha_array))
    return start_points_list


def get_header(model):
    if isinstance(model, RescorlaWagner):
        header = ['name', 'T', 'alpha gain', 'alpha lose']
    else:
        header = ['name', 'T', 'alpha']
    return header


if __name__ == '__main__':
    path = 'C:\\Users\\Marlena\\PycharmProjects\\ZPI\\ZPI\\data\\'
    model = Qlearning()
    save_optimal_params(path, model, 'Qlearning_real_player_parameters')