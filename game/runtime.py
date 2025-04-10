import pygame

from entities.player.player import Player
from game.env import Env
from game.camera import Camera
from menu.menu import Menu
from entities.staticblock import StaticBlock
from environnement.vie import BarreDeVie
from environnement.environnement_jeu import Chargeur, Kit_Med
from environnement.environnement_jeu import generate_powerups, generate_platforms

class Runtime():
    def __init__(self, window_size):
        # Initialisation de Pygame
        pygame.init()
        pygame.font.init()

        # Configuration de la fenêtre et des variables principales
        self.screen = pygame.display.set_mode(window_size)
        self.clock = pygame.time.Clock()
        self.dt = 0
        self.isRunning = True
        self.gameState = "menu"  # États possibles : menu, game, pause, gameover

        # Groupes et entités
        self.power_ups = pygame.sprite.Group()
        self.static_blocks = []
        self.trous = pygame.sprite.Group()
        self.barre_de_vie = BarreDeVie(max_vies=5)
        self.element_group = pygame.sprite.Group()
        self.plateformes_fixes = generate_platforms()
        self.generate_and_add_powerups()
        # Plateformes fixes

        # Chargement des ressources
        self.game_over_image = pygame.image.load("assets/fond.png")
        self.game_over_image = pygame.transform.scale(self.game_over_image, window_size)

        # Entités principales
        self.player = None
        self.env = None
        self.camera = None

        # Menus
        self.menu = None
        self.pauseMenu = None

        # Chargement des menus
        self.loadMenu()
        self.loadPauseMenu()

    def changeGameState(self, state: str):
        """
        Change l'état du jeu.
        :param state: menu, game, pause, gameover
        """
        valid_states = ["menu", "game", "pause", "gameover"]
        if state in valid_states:
            if state == "menu":
                self.menu.launchMusic()
            elif state == "game":
                self.menu.stopMusic()

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
            onClick=lambda: self.changeGameState("game")
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

    def loadPauseMenu(self):
        """Initialise le menu de pause."""
        menu = Menu(self.screen)
        middle_x = self.screen.get_width() // 2
        middle_y = self.screen.get_height() // 2
        menu.addButton(
            x=100,
            y=100,
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
        self.pauseMenu = menu

    def setup(self, player: Player, camera: Camera):
        """
        Configure les entités et l'environnement du jeu.
        """
        self.player = player
        self.camera = camera
        self.env = Env(1280, 720, "assets/bg.jpeg", self.screen, camera)
        self.player.set_game_over_image(self.game_over_image)
        self.barre_de_vie = BarreDeVie(5)

        # Ajout d'un bloc statique
        blue_block = StaticBlock(2000, 500, 100, 100)

        # Configuration du joueur
        self.player.set_game_over_image(self.game_over_image)

    def generate_and_add_powerups(self):
        """ Génère des PUs (chargeur ou kit médical) et les placent sur certaines plateformes"""
        positions_powerups = generate_powerups(self.plateformes_fixes)
        for pos in positions_powerups:
            x, y, power_up_type = pos
            if power_up_type == "chargeur":
                self.power_ups.add(Chargeur(x, y))
            elif power_up_type == "km":
                self.power_ups.add(Kit_Med(x, y))

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
                    elif event.key == pygame.K_w:
                        self.player.ramasser_chargeur(self.power_ups)
                        self.player.ramasser_km(self.power_ups)
                        self.player.ramasser_crayon(self.env.element_group)
                    elif event.key == pygame.K_q:
                        self.player.monter_escaliers(self.env.element_group)
                    elif event.key == pygame.K_e:
                        self.player.ouvrir_portes(self.env.element_group)
                    elif event.key == pygame.K_s:
                        if self.player.vie.vies < 5 and self.player.inventaire.possede("km"):
                            self.player.vie.vies += 1
                            self.player.gagner_vie()
                            self.player.inventaire.retirer("km")

            self.screen.fill("white")

            if self.gameState == "menu":
                self.menu.draw()
                self.menu.detect_click(events)
            elif self.gameState == "game":
                self.updateGame()
            elif self.gameState == "pause":
                self.pauseMenu.draw()
                self.pauseMenu.detect_click(events)

            pygame.display.flip()
            self.dt = self.clock.tick(60) / 1000

        pygame.quit()

    def updateGame(self):
        """Met à jour et dessine les éléments du jeu."""
        # Dessin de l'environnement
        self.env.draw()

        # Mise à jour et dessin du joueur
        self.player.update(self.env, self.camera)
        self.player.draw(self.screen, self.camera)
        self.player.check_trou_collision(self.env.element_group, self)
        self.player.inventaire.draw(self.screen)

        # Dessin des power-ups
        for power_up in self.power_ups:
            self.screen.blit(power_up.image, self.camera.apply(power_up))

        # Dessin des blocs statiques
        for block in self.static_blocks:
            block.draw(self.screen, self.camera)
            block.moveLeft()

        # Si la vie est à 0, afficher l'image de Game Over
        if self.player.vie.vies <= 0 and self.gameState == "gameover":
            self.player.afficher_game_over()
            pygame.display.update()
            pygame.time.delay(2000)
            self.changeGameState("menu")