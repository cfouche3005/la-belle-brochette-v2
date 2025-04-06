from environnement.fusion1 import Runtime
from entities.player.player import Player
from game.camera import Camera
from game.env import Env
import pygame
from environnement.fusion1 import Porte

if __name__ == '__main__':
    # Initialize the game
    game = Runtime((1280, 690))
    # Create a player instance

    env = Env(1280, 720, "assets/bg.png")
    camera = Camera(1280, 720, 1280*2)
    player = Player(10, 535, 50, 50)
    platforms = pygame.sprite.Group()

    keys = pygame.key.get_pressed()
    game.setup(player, env, camera, game.power_ups, game.platforms, game.element_group)
    game.run()

