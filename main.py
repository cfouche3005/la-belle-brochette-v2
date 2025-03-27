from game.runtime import Runtime
from entities.player.player import Player

if __name__ == '__main__':
    # Initialize the game
    game = Runtime((1280, 720))
    # Create a player instance
    player = Player(100, 100, 50, 50)
    game.setup(player)
    game.run()