from scripts.models import Qlearning
from scripts.player import RealPlayer

if __name__ == '__main__':
    model = Qlearning()
    rp = RealPlayer(path="/home/jczestochowska/workspace/ZPI/data/AniaPiateklearning.xls", model=model)
    print(rp.get_optimized_parameters())
