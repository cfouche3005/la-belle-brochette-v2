import pygame
import pygame_widgets

from entities.player.player import Player
from game.env import Env
from game.camera import Camera
from menu.menu import Menu
from entities.staticblock import StaticBlock


class Runtime():
    def __init__(self, window_size):
        # Pygame initialization
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode(window_size)
        self.clock = pygame.time.Clock()
        self.dt = 0
        self.isRunning = True
        self.gameState = "menu" # menu, game, pause

        self.player = None    # Joueur
        self.platforms = None # Liste des plateformes
        self.enemies = None   # Liste des ennemis
        self.power_ups = None # Liste des power-ups
        self.env = None       # Environ
        self.camera = None    # Camera
        self.menu = None      # Menu
        self.pauseMenu = None # Menu de pause
        self.loadMenu()
        self.loadPauseMenu()

    def changeGameState(self, state: str):
        """
        Change l'état du jeu
        :param state: menu, game, pause
        """
        if state == "menu":
            self.gameState = "menu"
        elif state == "game":
            self.gameState = "game"
        elif state == "pause":
            self.gameState = "pause"
        else:
            raise ValueError("Invalid game state")

    def loadMenu(self):
        menu = Menu(self.screen)
        menu.addButton(
            x = 100,
            y = 100,
            width = 200,
            height = 50,
            text = "Play",
            radius=20,
            fontsize = 30,
            inactiveColor = (255, 0, 0),
            hoverColor = (0, 255, 0),
            onClick = lambda: self.changeGameState("game")
        )
        menu.addText(200, 200, "Welcome to the Game!", 30, (255, 255, 255))
        self.menu = menu

    def loadPauseMenu(self):
        menu = Menu(self.screen)
        menu.addButton(
            x = 100,
            y = 100,
            width = 200,
            height = 50,
            text = "Resume",
            radius=20,
            fontsize = 30,
            inactiveColor = (255, 0, 0),
            hoverColor = (0, 255, 0),
            onClick = lambda: self.changeGameState("game")
        )
        menu.addButton(
            x = 100,
            y = 200,
            width = 200,
            height = 50,
            text = "Quit",
            radius=20,
            fontsize = 30,
            inactiveColor = (255, 0, 0),
            hoverColor = (0, 255, 0),
            onClick = lambda: self.changeGameState("menu")
        )
        self.pauseMenu = menu

    def setup(self, player: Player, env: Env, camera: Camera):
        """
        :param player: The player object
        :param env: The environment object
        :param camera: The camera object
        :return:
        """
        self.player = player
        self.platforms = ...
        self.enemies = ...
        self.power_ups = ...
        self.env = env
        self.camera = camera
        self.static_blocks = []
        blue_block = StaticBlock(2000, 200, 100, 100)
        self.static_blocks.append(blue_block)

    def run(self):
        while self.isRunning:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.isRunning = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.gameState == "game":
                            self.changeGameState("pause")
                        elif self.gameState == "pause":
                            self.changeGameState("game")

            self.screen.fill("black")

            if self.gameState == "menu":
                self.menu.draw()
                self.menu.detect_click(events)
            elif self.gameState == "game":
                # self.env.draw(self.screen)
                # # Mise à jour et rendu des entités
                #
                # self.player.draw(self.screen)
                bg_rect = pygame.Rect(self.env.x + self.camera.offset_x, self.env.y, self.env.width, self.env.height)
                self.screen.blit(self.env.background, bg_rect)
                self.player.draw(self.screen, self.camera)

                self.player.update(self.env, self.camera)
                for block in self.static_blocks:
                    block.draw(self.screen, self.camera)
            if self.gameState == "pause":
                self.pauseMenu.draw()
                self.pauseMenu.detect_click(events)

            pygame.display.flip()
            self.dt = self.clock.tick(60) / 1000
            pygame.display.update()



        pygame.quit()