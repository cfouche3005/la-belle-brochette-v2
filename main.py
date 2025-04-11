from game.runtime import Runtime
from entities.player.player import Player
from game.camera import Camera
from game.env import Env
import pygame

def main():
    game = Runtime((1280, 690))
    game.run()


if __name__ == '__main__':
    main()
