from scipy.optimize import minimize
import numpy as np
import os
import csv

from scripts.models import Qlearning, RescorlaWagner
from scripts.player import Estimator, RealPlayer


def search_optimal_parameters(estimator):
    optimal_alpha = []
    optimal_T = []
    optimal_func_value = []
    alpha_list = np.arange(0.0, 1.0, 0.01)
    T_list = np.arange(1, 10, 0.1)
    for alpha in alpha_list:
        for T in T_list:
            optimal_params = minimize(estimator.log_likelihood_function, x0=np.array([T, alpha]), method='Nelder-Mead',
                                      args=(-1.0,))
            optimal_func_value.append(optimal_params.fun)
            optimal_T.append(optimal_params.x[0])
            optimal_alpha.append(optimal_params.x[1])
    max_index, max_value = max(enumerate(optimal_func_value))
    return optimal_T[max_index], optimal_alpha[max_index]


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
                player_parameters = search_optimal_parameters(estimator)
                row.append(player_name)
                row.extend(player_parameters)
                writer.writerow(row)


def get_header(model):
    if isinstance(model, RescorlaWagner):
        header = ['name', 'T', 'alpha gain', 'alpha lose']
    else:
        header = ['name', 'T', 'alpha']
    return header


if __name__ == '__main__':
    path = 'C:\\Users\\Marlena\\PycharmProjects\\ZPI\\ZPI\\data\\'
    model = Qlearning()
    save_optimal_params(path, model, '{}_real_player_parameters'.format(model))
