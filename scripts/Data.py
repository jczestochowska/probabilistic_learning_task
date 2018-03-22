import glob
import pandas as pd
import os

from scripts.player import RealPlayer


class ExcelData():
    def __init__(self, path):
        self.data = pd.read_excel(path)

    def prepare_data(self):
        data = self.data.drop(['StimulusPair'], axis=1)
        condition_left = [int(i) for i in data.iloc[0][0:90].tolist()]
        condition_right = [int(i) for i in data.iloc[1][0:90].tolist()]
        decisions = [int(i) for i in data.iloc[2][0:90].tolist()]
        rewards = [int(i) for i in data.iloc[4][0:90].tolist()]
        data = {'StimulusLeft': condition_left, 'StimulusRight': condition_right, 'Actions': decisions,
                'Rewards': rewards}
        return data


def save_parameters_to_csv(path):
    all_files = glob.glob(path + "/*.xls")
    names_list = []
    T_list = []
    alpha_list = []
    for file in all_files:
        name = os.path.splitext(os.path.basename(file))[0]
        names_list.append(name[:-8])
        excel_data = ExcelData(file)
        real_data = excel_data.prepare_data()
        rp = RealPlayer(real_data)
        T, alpha = rp.search_parameters()
        T_list.append(T)
        alpha_list.append(alpha)
    data = {'Name': names_list, 'T': T_list, 'alpha': alpha_list}
    df = pd.DataFrame(data=data)
    df.to_csv('parameters_real_player', sep='\t')


if __name__ == '__main__':
    save_parameters_to_csv(path='')
