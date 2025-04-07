from game.runtime import Runtime
from entities.player.player import Player

from environnement.environnement_jeu import Plateforme, ElementAuSol, PU
from environnement.environnement_jeu import plateformes_fixes, positions_powerups, elements_sol_fixes

from game.camera import Camera
from game.env import Env
import pygame, random

if __name__ == '__main__':
    # Initialize the game
    game = Runtime((1280, 690))
    # Create a player instance

    env = Env(1280, 720, "assets/bg.png")
    camera = Camera(1280, 720, 1280*2)
    player = Player(10, 535, 50, 50)
    pu_group = pygame.sprite.Group()

    game.setup(player, env, camera, game.power_ups, game.platforms, game.element_group)
    game.run()

