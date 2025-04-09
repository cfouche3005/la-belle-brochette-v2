from game.runtime import Runtime
from entities.player.player import Player
from game.camera import Camera
from game.env import Env
import pygame, random

if __name__ == '__main__':

    game = Runtime((1280, 690))

    camera = Camera(1280, 720, 1280*2)
    player = Player(100, 150, 50, 50)
    pu_group = pygame.sprite.Group()

    game.setup(player, camera)
    game.run()

