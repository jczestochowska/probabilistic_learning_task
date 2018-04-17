from models import Estimator, Qlearning
from player import RealPlayer

if __name__ == '__main__':
    rp = RealPlayer(path="/home/jczestochowska/workspace/ZPI/data/AniaPiateklearning.xls")
    model = Qlearning()
    estimator = Estimator(decisions=rp.data['Action'].tolist(),
                          condition_left=rp.data['StimulusLeft'].tolist(),
                          condition_right=rp.data['StimulusRight'].tolist(),
                          rewards=rp.data['Reward'].tolist(),
                          model=model)
    print(estimator.max_log_likelihood().x)
