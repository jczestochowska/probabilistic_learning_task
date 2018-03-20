import pandas as pd


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


if __name__ == '__main__':
    d = ExcelData(path='')
    print(d.prepare_data())
