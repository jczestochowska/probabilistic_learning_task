from scripts.models import Qlearning, RescorlaWagner
from scripts.player import RealPlayer

if __name__ == '__main__':
    model = RescorlaWagner()
    rp = RealPlayer(path="C:\\Users\\Marlena\\PycharmProjects\\ZPI\\ZPI\\data\\MarlenaDudalearning.xls", model=model)
    print(rp.get_optimized_parameters())
    print(rp.model_selection())
