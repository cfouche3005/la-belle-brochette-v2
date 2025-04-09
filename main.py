from game.runtime import Runtime
from entities.player.player import Player
from game.camera import Camera
from game.env import Env
import pygame

if __name__ == '__main__':
    game = Runtime((1280, 690))
    env = Env(1280, 720, "assets/bg.jpeg")
    camera = Camera(1280, 720, 1280*2)
    player = Player(10, 535, 50, 50)
    pu_group = pygame.sprite.Group()
    game.setup(player, env, camera, game.power_ups, game.platforms, game.element_group)
    game.run()

