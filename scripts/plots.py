from scripts.player import RealPlayer
from scripts.models import Qlearning, Estimator
import matplotlib.pyplot as plt


def log_likelihood_table(estimator):
    estimator.max_log_likelihood()
    return estimator.log_likelihood_table

def display_likelihood(estimator):
    likelihood_table = log_likelihood_table(estimator)
    plt.plot(likelihood_table)
    plt.grid()
    plt.show()


if __name__=='__main__':
    rp = RealPlayer('C:\\Users\\Marlena\\PycharmProjects\\ZPI\\ZPI\\data\\MarlenaDudalearning.xls')
    model = Qlearning()
    estimator = Estimator(decisions=rp.data['Action'].tolist(),
                          condition_left=rp.data['StimulusLeft'].tolist(),
                          condition_right=rp.data['StimulusRight'].tolist(),
                          rewards=rp.data['Reward'].tolist(), model=model)
    display_likelihood(estimator)
