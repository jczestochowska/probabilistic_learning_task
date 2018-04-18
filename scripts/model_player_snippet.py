from scripts.game_session import GameSession
from scripts.models import Qlearning
from scripts.player import ModelPlayer

if __name__ == '__main__':
    game = GameSession()
    model = Qlearning()
    player = ModelPlayer(0.1, 0.1, game_skeleton=game.game_skeleton, model=model)
    game.play(player=player)
    print(player.params)
    game.save_results()
