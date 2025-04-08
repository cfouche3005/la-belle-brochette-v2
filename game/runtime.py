import pygame, random
from environnement.environnement_jeu import ElementAuSol, Plateforme, PU
from entities.player.player import Player
from game.env import Env
from game.camera import Camera
from menu.menu import Menu
from entities.staticblock import StaticBlock
from environnement.vie import BarreDeVie
from environnement.environnement_jeu import plateformes_fixes, positions_powerups, elements_sol_fixes


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
        self.platforms = pygame.sprite.Group()
        self.element_group = pygame.sprite.Group()
        self.power_ups = pygame.sprite.Group()
        self.barre_de_vie = BarreDeVie(max_vies=5)
        self.enemies = None   # Liste des ennemis
        self.env = None  # Environ
        self.camera = None    # Camera
        self.menu = None      # Menu
        self.pauseMenu = None # Menu de pause
        self.loadMenu()
        self.loadPauseMenu()
        self.elements_sol = pygame.sprite.Group()
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

    def setup(self, player: Player, env: Env, camera: Camera, power_ups : PU, platforms : Plateforme, elt_group : ElementAuSol):
        """
        :param player: The player object
        :param env: The environment object
        :param camera: The camera object
        :return:
        """
        self.player = player
        self.platforms = []
        self.power_ups = power_ups
        self.platforms = pygame.sprite.Group()
        self.element_group = pygame.sprite.Group()
        self.enemies = ...
        self.env = env
        self.camera = camera
        self.static_blocks = []
        blue_block = StaticBlock(2000, 200, 100, 100)
        self.static_blocks.append(blue_block)

        positions_powerups = [(100, 150), (200, 250), (300, 350)]  # Exemple de positions
        powerup_textures = [
            "C:/Users/audem/Downloads/PIECE.jpg",
            "C:/Users/audem/Downloads/PISTOLET.jpg",
            "C:/Users/audem/Downloads/MK.jpg"
        ]
        for pu in positions_powerups:
            x, y = pu
            random_texture_pu = random.choice(powerup_textures)
            power_up = PU(x, y, random_texture_pu)
            power_ups.add(power_up)

        for x, y, width, height in plateformes_fixes:
            texture = random.choice(["C:/Users/audem/Downloads/VOITURE2.png", "C:/Users/audem/Downloads/TROTTOIR.jpg"])
            plateforme = Plateforme(x, y, width, height, texture)
            self.platforms.add(plateforme)

        for x, y, type_element in elements_sol_fixes:
            textures = {
                "porte": "C:/Users/audem/Downloads/PORTE1.png",
                "escalier": "C:/Users/audem/Downloads/ESCALIER1.png",
                "trou": "C:/Users/audem/Downloads/TROU1.png",
                "crayon": "C:/Users/audem/Downloads/CRAYON_JW.png"
            }
            if type_element in textures:
                element = ElementAuSol(x, y, 50, 50, textures[type_element])
                self.element_group.add(element)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                self.isRunning = False
            elif event.type == pygame.KEYDOWN:
                print(f"Touche pressée : {pygame.key.name(event.key)}")
                if pygame.key.name(event.key).lower() == "w":  # Touche w pour ramasser un PU
                    print("Touche w pressée")
                    self.player.ramasser_pu(self.power_ups)

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
                bg_rect = pygame.Rect(self.env.x + self.camera.offset_x, self.env.y, self.env.width, self.env.height)
                self.screen.blit(self.env.background, bg_rect)
                self.player.draw(self.screen, self.camera)
                self.player.update(self.env, self.camera)
                for plateforme in self.platforms:
                    self.screen.blit(plateforme.image, self.camera.apply(plateforme))

                    # Afficher les éléments au sol
                for element in self.element_group:
                    self.screen.blit(element.image, self.camera.apply(element))

                    # Afficher les power-ups
                for power_up in self.power_ups:
                    self.screen.blit(power_up.image, self.camera.apply(power_up))
                for block in self.static_blocks:
                    block.draw(self.screen, self.camera)

            elif self.gameState == "pause":
                self.pauseMenu.draw()
                self.pauseMenu.detect_click(events)

            pygame.display.flip()
            self.dt = self.clock.tick(60) / 1000
            pygame.display.update()



        pygame.quit()