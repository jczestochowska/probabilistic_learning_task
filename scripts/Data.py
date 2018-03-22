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


class SavingParameters():
    def __init__(self):
        self.T_list = []
        self.names_list = []
        self.alpha_list = []
        self.alpha_gain_list = []
        self.alpha_loose_list = []
        self.data = []

    def save_parameters_to_csv(self, path, model):
        all_files = glob.glob(path + "/*.xls")
        for file in all_files:
            name = os.path.splitext(os.path.basename(file))[0]
            self.names_list.append(name[:-8])
            excel_data = ExcelData(file)
            real_data = excel_data.prepare_data()
            rp = RealPlayer(real_data)
            params = rp.search_parameters(model)
            if model == 'Q_learning':
                self.data = self.parameters_q_learning(params)
            elif model == 'Rescorla-Wagner':
                self.data = self.parameters_rescorla_wargner(params)
        df = pd.DataFrame(data=self.data)
        df.to_csv(model + '_' + 'parameters_real_player', sep='\t')

    def parameters_q_learning(self, params):
        T, alpha = params
        self.T_list.append(T)
        self.alpha_list.append(alpha)
        parameters = {'Name': self.names_list, 'T': self.T_list, 'alpha': self.alpha_list}
        return parameters

    def parameters_rescorla_wargner(self, params):
        T, alpha_gain, alpha_loose = params
        self.T_list.append(T)
        self.alpha_gain_list.append(alpha_gain)
        self.alpha_loose_list.append(alpha_loose)
        parameters = {'Name': self.names_list, 'T': self.T_list, 'alpha gain': self.alpha_gain_list,
                      'alpha loose': self.alpha_loose_list}
        return parameters


if __name__ == '__main__':
    s = SavingParameters()
    s.save_parameters_to_csv('C:\\Users\\Marlena\\PycharmProjects\\ZPI\\ZPI\\data', 'Rescorla-Wagner')
