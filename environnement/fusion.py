import pygame, random

from entities.player.player import Player
from game.env import Env
from game.camera import Camera
from menu.menu import Menu
from entities.staticblock import StaticBlock
screen_width = 1450
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
# Coordonnées fixes des plateformes
plateformes_fixes = [
    (100, 500, 150, 20 ),
    (250, 500, 150, 20 ),
    (400, 450, 150, 20),
    (590, 400, 150, 20),
    (1000, 450, 150, 20),
    (1250, 500, 150, 20),
    (1400, 500, 150, 20),
    (1590, 500, 150, 20),
    (3500, 500, 150, 20),
    (4000, 250, 150, 20),
    (4500, 250, 150, 20),
    (5000, 400, 150, 20),
    (5500, 250, 150, 20),
    (6000, 450, 150, 20),
]

# Coordonnées fixes des éléments au sol
elements_sol_fixes = [
    (30, 535, "escalier"),
    (500, 535, "porte"),
    (700, 535, "trou"),
    (1000, 535, "escalier"),
    (2000, 535, "trou"),
    (3000, 535, "trou"),
    (4500, 535, "porte"),
    (2000, 535, "escalier"),
    (10000, 535, "crayon"),
]
sol_y = 535
class Plateforme(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image_path):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

class Trottoir(Plateforme):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "C:/Users/audem/Downloads/GROUND.jpg")

class Voiture(Plateforme):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "C:/Users/audem/Downloads/VOITURE2.png")


class ElementAuSol(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image_path):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

class Porte(ElementAuSol):
    def __init__(self, x, y):
        super().__init__(x, y, 100, 100, "C:/Users/audem/Downloads/PORTE1.png")

class Escalier(ElementAuSol):
    def __init__(self, x, y):
        ElementAuSol.__init__(self, x, y, 50, 50, "C:/Users/audem/Downloads/ESCALIER1.png")

class Trou(ElementAuSol):  # Nouveau type d'élément : Trou
    def __init__(self, x, y):
        ElementAuSol.__init__(self, x, y, 50, 50, "C:/Users/audem/Downloads/TROU1.png")

class Crayon(ElementAuSol):
    def __init__(self, x, y):
        ElementAuSol.__init__(self, x, y, 50, 50, "C:/Users/audem/Downloads/crayon_JW.png")


class PU(pygame.sprite.Sprite):
    def __init__(self, x, y_platform, image_path):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = x

        if random.random() < 0.5:
            self.rect.y = y_platform - self.rect.height
        else:
            self.rect.y = sol_y

class Pistolet(PU):
    def __init__(self, x, y_platform):
        super().__init__(x, y_platform, "C:/Users/audem/Downloads/PISTOLET_PA.png")
        self.damage = 1  # Enlève 1 vie
        self.munitions = 6

class Kit_Med(PU):
    def __init__(self, x, y_platform):
        super().__init__(x, y_platform, "C:/Users/audem/Downloads/KM_PA.png")

class Piece(PU):
    def __init__(self, x, y_platform):
        super().__init__(x, y_platform, "C:/Users/audem/Downloads/PIECE_PA.png")


class BarreDeVie:
    def __init__(self, max_vies=5):
        self.vies = max_vies
        self.max_vies = max_vies
        self.x = 20
        self.y = 20
        self.coeur_image = pygame.image.load("C:/Users/audem/Downloads/COEUR_PA.png").convert_alpha()
        self.coeur_image = pygame.transform.scale(self.coeur_image, (40, 40))

    def perdre_vie(self, damage):
        self.vies -= damage
        if self.vies < 0:
            self.vies = 0

    def draw(self, screen):
        for i in range(self.vies):
            screen.blit(self.coeur_image, (self.x + i * 45, self.y))


#FAIT AVEC GPT => pour éviter que le joueur ramasse plusieurs PUS, il est limité à 1 KM, 1 pistolet et 1 crayon et limitation des balles
class Player:
    def __init__(self):
        self.has_pistolet = False
        self.has_crayon = False
        self.has_KM = False

    def ramasser_pu(self, pu):
        if isinstance(pu, Pistolet) and not self.has_pistolet:
            self.has_pistolet = True
            return True
        elif isinstance(pu, Crayon) and not self.has_crayon:
            self.has_crayon = True
            return True
        elif isinstance(pu, Kit_Med) and not self.has_KM:
            self.has_KM = True
            return True
        return False

    def tirer(self, arme):
        if arme and arme.munitions > 0:
            arme.munitions -= 1
            print(f"Tir effectué ! Balles restantes: {arme.munitions}")
        else:
            print("Plus de munitions !")


class Game:
    def __init__(self):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.isRunning = True
        self.plateformes = pygame.sprite.Group()  # Groupes de plateformes
        self.pu_group = pygame.sprite.Group()  # Groupes de power-ups
        self.element_group = pygame.sprite.Group()  # Groupes des éléments au sol
        self.init_plateformes()  # Appel pour initialiser les plateformes
        self.init_elements_sol()  # Appel pour initialiser les éléments au sol
        self.barre_de_vie = BarreDeVie()
        self.camera_offset = 0  # Exemple d'offset pour la caméra (à ajuster avec la position du joueur)

    def init_plateformes(self):
        for x, y, width, height in plateformes_fixes:
            if random.random() < 0.5:
                plateforme = Voiture(x, y, width, height)
            else:
                plateforme = Trottoir(x, y, width, height)

            self.plateformes.add(plateforme)

    def init_elements_sol(self):
        for x, y, type_element in elements_sol_fixes:
            if type_element == "porte":
                element = Porte(x, sol_y)
            elif type_element == "trou":
                element = Trou(x, sol_y)
            elif type_element == "escalier":
                element = Escalier(x, sol_y)
            elif type_element == "crayon":
                element = Crayon(x, sol_y)
            self.element_group.add(element)

    def apparitions_PUs(self):
        self.pu_group.empty()
        for x, y in [(300, 500),  (1050, 450), (1640, 500), (3550, 535),
                     (3500, 535), (5500, 450), (6050, 450), (9050, 400), (10050, 250), (12050, 400), (13050, 250), (15500, 400),
                     (35000, 535)]:  # X fixe, Y de la plateforme
            pu = random.choice([Pistolet(x, y), Kit_Med(x, y), Piece(x,y)])
            self.pu_group.add(pu)

    def draw_elements(self):
        for plateforme in self.plateformes:
            self.screen.blit(plateforme.image, (plateforme.rect.x - self.camera_offset, plateforme.rect.y))

        for pu in self.pu_group:
            self.screen.blit(pu.image, (pu.rect.x - self.camera_offset, pu.rect.y))

        for element in self.element_group:
            self.screen.blit(element.image, (element.rect.x - self.camera_offset, element.rect.y))

    def run(self):
        background = pygame.image.load("C:/Users/audem/Downloads/fond.png").convert_alpha()
        background = pygame.transform.scale(background, (screen_width, screen_height))

        compteur = 0
        while self.isRunning:
            self.screen.blit(background, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.isRunning = False

            if compteur % 120 == 0:
                self.apparitions_PUs()

            self.draw_elements()

            pygame.display.flip()
            self.clock.tick(30)
            compteur += 1
class Runtime:
    def __init__(self, window_size):
        # Pygame initialization
        # Initialisation de Pygame et autres attributs
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode(window_size)
        self.clock = pygame.time.Clock()
        self.dt = 0
        self.isRunning = True
        self.gameState = "menu"

        self.player = None
        self.platforms = pygame.sprite.Group()
        self.element_group = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.power_ups = pygame.sprite.Group()
        self.env = None
        self.camera = None
        self.menu = None
        self.pauseMenu = None

        self.barre_de_vie = BarreDeVie(max_vies=5)
        self.init_game_elements()
        self.loadMenu()
        self.loadPauseMenu()

    def init_game_elements(self):
        self.platforms = pygame.sprite.Group()

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

        positions_powerups = [(300, 500), (1050, 450), (1640, 500), (3550, 535)]
        powerup_textures = [
            "C:/Users/audem/Downloads/PIECE_PA.png",
            "C:/Users/audem/Downloads/PISTOLET_PA.png",
            "C:/Users/audem/Downloads/KM_PA.png"
        ]

        for x, y in positions_powerups:
            pu = PU(x, y, random.choice(powerup_textures))
            self.power_ups.add(pu)

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()

            pygame.display.flip()
            self.clock.tick(60)

    def draw(self):
        if self.gameState == "menu":
            self.menu.draw()
            self.menu.detect_click(pygame.event.get())
        elif self.gameState == "game":
            # Dessiner l'environnement
            self.env.background = pygame.image.load("C:/Users/audem/Downloads/fond.png").convert_alpha()
            bg_rect = pygame.Rect(self.env.x + self.camera.offset_x, self.env.y, self.env.width, self.env.height)
            self.screen.blit(self.env.background, bg_rect)

            # Dessiner les plateformes, power-ups, éléments au sol, etc.
            self.platforms.draw(self.screen)  # Dessiner toutes les plateformes
            self.power_ups.draw(self.screen)  # Dessiner tous les power-ups
            self.element_group.draw(self.screen)  # Dessiner tous les éléments au sol
            self.player.draw(self.screen, self.camera)  # Dessiner le joueur
            self.barre_de_vie.draw(self.screen)  # Dessiner la barre de vie

        elif self.gameState == "pause":
            self.pauseMenu.draw()
            self.pauseMenu.detect_click(pygame.event.get())

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
            x=100,
            y=100,
            width=200,
            height=50,
            text="Play",
            radius=20,
            fontsize=30,
            inactiveColor=(255, 0, 0),
            hoverColor=(0, 255, 0),
            onClick=lambda: self.changeGameState("game")
        )
        menu.addText(200, 200, "Welcome to the Game!", 30, (255, 255, 255))
        self.menu = menu

    def loadPauseMenu(self):
        menu = Menu(self.screen)
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
            x=100,
            y=200,
            width=200,
            height=50,
            text="Quit",
            radius=20,
            fontsize=30,
            inactiveColor=(255, 0, 0),
            hoverColor=(0, 255, 0),
            onClick=lambda: self.changeGameState("menu")
        )
        self.pauseMenu = menu

    def setup(self, player: Player, env: Env, camera: Camera, power_ups : PU, platforms : Plateforme, elt_group : ElementAuSol ):
        """
        :param player: The player object
        :param env: The environment object
        :param camera: The camera object
        :return:
        """
        self.player = player
        self.env = env
        self.camera = camera
        self.power_ups = power_ups
        self.platforms = platforms
        self.element_group = elt_group
        # Initialisation d'autres éléments comme les ennemis, la barre de vie, etc.
        self.static_blocks = []
        blue_block = StaticBlock(2000, 200, 100, 100)  # Exemple de bloc statique
        self.static_blocks.append(blue_block)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.isRunning = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.gameState = "pause" if self.gameState == "game" else "game"

    def update(self):
        if self.gameState == "game":
            self.platforms.update()
            self.element_group.update()
            self.power_ups.update()
            self.player.update(self.env, self.camera)

    def run(self):
        # Charger l'image de fond comme une Surface
        self.env.background = pygame.image.load("C:/Users/audem/Downloads/fond.png").convert_alpha()


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
            self.handle_events()
            self.update()
            self.draw()

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

                for block in self.static_blocks:
                    block.draw(self.screen, self.camera)
            if self.gameState == "pause":
                self.pauseMenu.draw()
                self.pauseMenu.detect_click(events)

            pygame.display.flip()
            self.dt = self.clock.tick(60) / 1000
            pygame.display.update()

        pygame.quit()