import pygame

from entities.player.player import Player


class Runtime():
    def __init__(self, window_size):
        # Pygame initialization
        pygame.init()
        self.screen = pygame.display.set_mode(window_size)
        self.clock = pygame.time.Clock()
        self.dt = 0
        self.isRunning = True

        self.player = None    # Joueur
        self.platforms = None # Liste des plateformes
        self.enemies = None   # Liste des ennemis
        self.power_ups = None # Liste des power-ups

    def setup(self, player: Player):
        self.player = player
        self.platforms = ...
        self.enemies = ...
        self.power_ups = ...

    def run(self):
        while self.isRunning:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.isRunning = False

            self.screen.fill("white")

            # Mise à jour et rendu des entités

            self.player.draw(self.screen)

            pygame.display.flip()
            self.dt = self.clock.tick(60) / 1000

            self.player.update()

        pygame.quit()