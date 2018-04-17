import csv
import os

from models import RescorlaWagner, Qlearning
from player import Estimator, RealPlayer


def save_all_real_players_parameters_to_csv(data_dir_path, new_filename, model):
    all_filenames = os.listdir(data_dir_path)
    with open('{}.csv'.format(new_filename), 'w') as file:
        writer = csv.writer(file, delimiter=',')
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
                name = os.path.splitext(os.path.basename(filename))[0][:-8]
                player_parameters = list(rp.search_parameters(estimator))
                row.append(name)
                row.extend(player_parameters)
                writer.writerow(row)


def get_header(model):
    if isinstance(model, RescorlaWagner):
        header = ['name', 'T', 'alpha gain', 'alpha lose']
    else:
        header = ['name', 'T', 'alpha']
    return header


if __name__ == '__main__':
    #rl = RescorlaWagner()
    ql = Qlearning()
    save_all_real_players_parameters_to_csv('/Users/karola/PycharmProjects/ZPI/data',
                                            'new_real_player_params_ql', ql)
