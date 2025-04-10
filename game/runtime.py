import pygame, random
from environnement.environnement_jeu import ElementAuSol, Plateforme, PU, Crayon
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

        self.game_over_image = pygame.image.load("assets/fond.png")  # Charger l'image Game Over ici
        self.game_over_image = pygame.transform.scale(self.game_over_image, window_size)

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
        elif state == "gameover":  # Ajouter "gameover" comme état valide
            self.gameState = "gameover"
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
        self.trous = pygame.sprite.Group()
        self.player.set_game_over_image(self.game_over_image)
        self.barre_de_vie = BarreDeVie(3)

        self.env = env
        self.camera = camera
        self.static_blocks = []
        blue_block = StaticBlock(2000, 200, 100, 100)
        self.static_blocks.append(blue_block)

        powerup_textures = {
            "chargeur": "assets/munition.png",
            "km":"assets/kit_medical.png"
        }
        for x, y, type_powerup in positions_powerups:
            if type_powerup in powerup_textures:
                # Crée un power-up en fonction de son type et de la position
                texture = powerup_textures[type_powerup]
                power_up = PU(x, y, texture, type_powerup)  # Crée le PU avec la bonne texture
                self.power_ups.add(power_up)

        for x, y, width, height in plateformes_fixes:
            texture =  "assets/GROUND.jpg"
            plateforme = Plateforme(x, y, width, height, texture)
            self.platforms.add(plateforme)

        for x, y, type_element in elements_sol_fixes:
            textures = {
                "porte": "assets/porte_noire.png",
                "escalier": "assets/escalier_urbain.png",
                "trou": "assets/trou_sol.png",
                "crayon": "assets/crayon.png"
            }
            if type_element in textures:
                element = ElementAuSol(x, y, 50, 50, textures[type_element], type_element)
                self.element_group.add(element)

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
                    elif event.key == pygame.K_w:
                        self.player.ramasser_chargeur(self.power_ups)
                        self.player.ramasser_km(self.power_ups)
                        self.player.ramasser_crayon(self.element_group)
                    elif event.key == pygame.K_q:
                        self.player.monter_escaliers(self.element_group)
                    elif event.key == pygame.K_e:
                        self.player.ouvrir_portes(self.element_group)
                    elif event.key == pygame.K_s:
                        if self.player.vie.vies < 5 and self.player.inventaire.possede("km"):
                            self.player.vie.vies += 1  # Augmente les vies du joueur
                            self.player.gagner_vie()  # Ajoute un coeur
                            self.player.inventaire.retirer("km")  # Retire un KM
                            print("KM utilisé ! Vie restante :", self.player.vie.vies)

            self.screen.fill("black")

            if self.gameState == "menu":
                self.menu.draw()
                self.menu.detect_click(events)
            elif self.gameState == "game":
                bg_rect = pygame.Rect(self.env.x + self.camera.offset_x, self.env.y, self.env.width, self.env.height)
                self.screen.blit(self.env.background, bg_rect)
                self.player.draw(self.screen, self.camera)
                self.player.update(self.env, self.camera)
                self.player.check_trou_collision(elements_sol_fixes, self)
                self.barre_de_vie.draw(self.screen)
                self.player.inventaire.draw(self.screen)
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

                    # Si la vie est à 0, afficher l'image de Game Over
                    if self.player.vie.vies <= 0 and self.gameState == "gameover":
                        self.player.afficher_game_over()
                        pygame.display.update()
                        pygame.time.delay(2000)
                        self.changeGameState("menu")

            elif self.gameState == "pause":
                self.pauseMenu.draw()
                self.pauseMenu.detect_click(events)

            pygame.display.flip()
            self.dt = self.clock.tick(60) / 1000
            pygame.display.update()
        pygame.quit()