from game_session import GameSession
from models import Qlearning
from player import ModelPlayer

if __name__ == '__main__':
    game = GameSession()
    model = Qlearning()
    player = ModelPlayer(game.game_skeleton, model, 0.1, 0.1)
    player.play_game()
    print(player.params)
