from scripts.game_session import GameSession
from scripts.models import Qlearning
from scripts.player import ModelPlayer

if __name__ == '__main__':
    game = GameSession()
    player = ModelPlayer(game.game_skeleton, 0.1, 0.1)
    model = Qlearning()
    print(player.play_game(model))
