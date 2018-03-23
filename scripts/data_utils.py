import csv
import os

from scripts.player import RealPlayer


def save_all_real_players_parameters_to_csv(data_dir_path, new_filename, model):
    all_filenames = os.listdir(data_dir_path)
    with open('{}.csv'.format(new_filename), 'w') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(get_header(model))
        for filename in all_filenames:
            if filename.endswith('xls'):
                row = []
                rp = RealPlayer(os.path.join(data_dir_path, filename))
                name = os.path.splitext(os.path.basename(filename))[0][:-8]
                player_parameters = list(rp.search_parameters(model))
                row.extend(player_parameters)
                row.append(name)
                writer.writerow(row)


def get_header(model):
    if model == 'Q_learning':
        header = ['T', 'alpha', 'name']
    elif model == 'Rescorla-Wagner':
        header = ['T', 'alpha gain', 'alpha lose', 'name']
    return header


if __name__ == '__main__':
    save_all_real_players_parameters_to_csv("/home/jczestochowska/workspace/ZPI/data", 'tes_params', 'Q_learning')
