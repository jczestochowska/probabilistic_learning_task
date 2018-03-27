import csv
import os

from scripts.player import Estimator, RealPlayer


def save_all_real_players_parameters_to_csv(data_dir_path, new_filename, model):
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
                                      rewards=rp.data['Reward'].tolist())
                name = os.path.splitext(os.path.basename(filename))[0][:-8]
                player_parameters = list(rp.search_parameters(model, estimator))
                row.append(name)
                row.extend(player_parameters)
                writer.writerow(row)


def get_header(model):
    if model == 'Q_learning':
        header = ['name', 'T', 'alpha']
    elif model == 'Rescorla-Wagner':
        header = ['name', 'T', 'alpha gain', 'alpha lose']
    return header


if __name__ == '__main__':
    save_all_real_players_parameters_to_csv("C:\\Users\\Marlena\\Desktop\\studia\\6 semestr\\ZPI\\gra ZPI\\wyniki",
                                            'tes_params', 'Rescorla-Wagner')
