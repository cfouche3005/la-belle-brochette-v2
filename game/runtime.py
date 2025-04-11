import pygame

from entities.player.player import Player
from game.env import Env
from game.camera import Camera
from menu.menu import Menu
from entities.staticblock import StaticBlock
from environnement.vie import BarreDeVie
from environnement.environnement_jeu import Chargeur, Kit_Med, positions_powerups

class Runtime():
    def __init__(self, window_size):
        # Initialisation de Pygame
        pygame.init()
        pygame.font.init()

        # Configuration de la fenêtre et des variables principales
        self.screen = pygame.display.set_mode(window_size)
        self.wi, self.he = window_size
        self.clock = pygame.time.Clock()
        self.dt = 0
        self.isRunning = True
        self.gameState = "menu"  # États possibles : menu, game, pause, gameover

        # Groupes et entités
        self.static_blocks = []
        self.trous = pygame.sprite.Group()
        self.element_group = pygame.sprite.Group()
        # Plateformes fixes

        # Entités principales
        self.player = None
        self.env = None
        self.camera = None

        # Menus
        self.menu = None
        self.pauseMenu = None
        self.game_over_menu = None

        # Chargement des menus
        self.loadMenu()
        self.loadPauseMenu()
        self.loadGameOverMenu()

    def changeGameState(self, state: str):
        """
        Change l'état du jeu.
        :param state: menu, game, pause, gameover
        """
        valid_states = ["menu", "game", "pause", "gameover"]
        if state in valid_states:
            if state == "menu":
                self.menu.launchMusic()
                self.pauseMenu.stopMusic()
                self.game_over_menu.stopMusic()
            elif state == "game":
                self.menu.stopMusic()
                self.pauseMenu.stopMusic()
                self.game_over_menu.stopMusic()
            elif state == "gameover":
                self.menu.stopMusic()
                self.pauseMenu.stopMusic()
                self.game_over_menu.launchMusic()

            self.gameState = state
        else:
            raise ValueError("Invalid game state")

    def loadMenu(self):
        """Initialise le menu principal."""
        menu = Menu(self.screen)
        middle_x = self.screen.get_width() // 2
        middle_y = self.screen.get_height() // 2

        menu.addButton(
            x=middle_x,
            y=middle_y,
            width=300,
            height=50,
            text="Play The Boogeyman",
            radius=20,
            fontsize=30,
            inactiveColor=(80, 80, 80),
            hoverColor=(150, 150, 150),
            onClick=lambda: self.changeToGame()
        )
        menu.addText(
            middle_x,
            middle_y - 100,
            "...He Stole John Wick's Car, Sir, And, Uhhh... Killed His Dog.",
            30,
            (255, 255, 255)
        )
        menu.loadBackground("assets/menu.png")
        menu.attatchMusic("assets/music/Assassins.mp3")
        self.menu = menu

    def changeToGame(self):
        self.setup()
        self.changeGameState("game")

    def loadPauseMenu(self):
        """Initialise le menu de pause."""
        menu = Menu(self.screen)
        middle_x = self.screen.get_width() // 2
        middle_y = self.screen.get_height() // 2
        menu.addButton(
            x=middle_x,
            y=middle_y-100,
            width=200,
            height=50,
            text="Resume",
            radius=20,
            fontsize=30,
            inactiveColor=(255, 0, 0),
            hoverColor=(0, 255, 0),
            onClick=lambda: self.changeGameState("game")
        )
        menu.addButton(
            x=middle_x,
            y=middle_y,
            width=300,
            height=50,
            text="Quit",
            radius=20,
            fontsize=30,
            inactiveColor=(255, 0, 0),
            hoverColor=(0, 255, 0),
            onClick=lambda: self.changeGameState("menu")
        )
        menu.addButton(
            x=middle_x,
            y=middle_y+100,
            width=300,
            height=50,
            text="Reset",
            radius=20,
            fontsize=30,
            inactiveColor=(255, 0, 0),
            hoverColor=(0, 255, 0),
            onClick=lambda: self.reset()
        )
        self.pauseMenu = menu

    def loadGameOverMenu(self):
        """Initialise le menu de fin de jeu."""
        menu = Menu(self.screen)
        menu.loadBackground("assets/game_over.jpg")
        menu.attatchMusic("assets/music/GameOver.mp3")
        middle_x = self.screen.get_width() // 2
        middle_y = self.screen.get_height() // 2

        menu.addButton(
            x=middle_x,
            y=middle_y-100,
            width=200,
            height=50,
            text="Revenir au menu",
            radius=20,
            fontsize=30,
            inactiveColor=(255, 0, 0),
            hoverColor=(0, 255, 0),
            onClick=lambda: self.changeGameState("menu")
        )
        menu.addButton(
            x=middle_x,
            y=middle_y,
            width=300,
            height=50,
            text="Quitter",
            radius=20,
            fontsize=30,
            inactiveColor=(255, 0, 0),
            hoverColor=(0, 255, 0),
            onClick=lambda: pygame.quit()
        )
        menu.addText(
            middle_x,
        middle_y-200,
            "Vous avez perdu !",
            50,
            (255, 255, 255)
        )

        self.game_over_menu = menu

    def setup(self):
        """
        Configure les entités et l'environnement du jeu.
        """
        self.player = Player(100, 150, 50, 50, lambda: self.changeGameState("gameover"))
        self.camera = Camera(self.wi, self.he, self.wi * 2)
        self.env = Env(self.wi, self.he, "assets/bg.jpeg", self.screen, self.camera)
    def reset(self):
        """Réinitialise le jeu."""
        self.setup()

    def run(self):
        """Boucle principale du jeu."""
        self.changeGameState("menu")
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

            self.screen.fill("white")

            if self.gameState == "menu":
                self.menu.draw()
                self.menu.detect_click(events)
            elif self.gameState == "game":
                self.updateGame()
            elif self.gameState == "pause":
                self.pauseMenu.draw()
                self.pauseMenu.detect_click(events)
            elif self.gameState == "gameover":
                self.game_over_menu.draw()
                self.game_over_menu.detect_click(events)

            pygame.display.flip()
            self.dt = self.clock.tick(60) / 1000

        pygame.quit()

    def updateGame(self):
        """Met à jour et dessine les éléments du jeu."""
        # Dessin de l'environnement
        self.env.draw()

        self.env.update(self.player)

        # Mise à jour et dessin du joueur
        self.player.update(self.env, self.camera)
        self.player.draw(self.screen, self.camera)
        self.player.check_trou_collision(self.env.element_group, self)
        self.player.inventaire.draw(self.screen)

        # Dessin des blocs statiques
        for block in self.static_blocks:
            block.draw(self.screen, self.camera)
            block.moveLeft()