from scripts.game_session import GameSession
from scripts.models import Qlearning
from scripts.player import VirtualPlayer

if __name__ == '__main__':
    game = GameSession()
    model = Qlearning()
    player = VirtualPlayer(2, 0.1, game_skeleton=game.game_skeleton, model=model)
    game.play(player=player)
    game.save_results()
