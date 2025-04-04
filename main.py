from game.runtime import Runtime
from entities.player.player import Player
from game.camera import Camera
from game.env import Env

if __name__ == '__main__':
    # Initialize the game
    game = Runtime((1280, 720))
    # Create a player instance

    env = Env(1280, 720, "assets/bg.jpeg")
    camera = Camera(1280, 720)
    player = Player(100, 100, 50, 50)

    game.setup(player, env, camera)
    game.run()