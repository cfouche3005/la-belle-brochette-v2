import pygame
import random
from entities.player.player import Player
from game.env import Env
from game.camera import Camera
from menu.menu import Menu
from entities.staticblock import StaticBlock

# Paramètres de l'écran
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))

# Coordonnées fixes des plateformes
plateformes_fixes = [
    (100, 300, 10, 20),
    (250, 500, 150, 20),
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
    (100, 475, "escalier"),
    (500, 475, "porte"),
    (700, 475, "trou"),
    (1000, 475, "escalier"),
    (2000, 475, "trou"),
    (3000, 475, "trou"),
    (4500, 475, "porte"),
    (2000, 475, "escalier"),
    (10000, 475, "crayon"),
]
sol_y = 475


# Classe des plateformes
class Plateforme(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image_path):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))
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
        self.image = pygame.transform.scale(self.image, (75, 75))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

class Porte(ElementAuSol):
    def __init__(self, x, y):
        super().__init__(x, y, "C:/Users/audem/Downloads/PORTE1.png")

class Escalier(ElementAuSol):
    def __init__(self, x, y):
        super().__init__(x, y, "C:/Users/audem/Downloads/ESCALIER1.png")

class Trou(ElementAuSol):
    def __init__(self, x, y):
        super().__init__(x, y,"C:/Users/audem/Downloads/TROU1.png")

class Crayon(ElementAuSol):
    def __init__(self, x, y):
        super().__init__(x, y,"C:/Users/audem/Downloads/crayon_JW.png")


class PU(pygame.sprite.Sprite):
    def __init__(self, x, y_platform, image_path):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (75, 75))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = random.choice([y_platform - self.rect.height, sol_y])


class Pistolet(PU):
    def __init__(self, x, y_platform):
        super().__init__(x, y_platform, "C:/Users/audem/Downloads/PISTOLET_PA.png")
        self.damage = 1


class Kit_Med(PU):
    def __init__(self, x, y_platform):
        super().__init__(x, y_platform, "C:/Users/audem/Downloads/KM_PA.png")

class Piece(PU):
    def __init__(self, x, y_platform):
        super().__init__(x, y_platform, "C:/Users/audem/Downloads/PIECE_PA.png")


# Barre de vie
class BarreDeVie:
    def __init__(self, max_vies=5):
        self.vies = max_vies
        self.max_vies = max_vies
        self.x = 20
        self.y = 20
        self.coeur_image = pygame.image.load("C:/Users/audem/Downloads/COEUR_PA.png").convert_alpha()
        self.coeur_image = pygame.transform.scale(self.coeur_image, (75, 75))

    def perdre_vie(self, damage):
        self.vies -= damage
        if self.vies < 0:
            self.vies = 0

    def draw(self, screen):
        for i in range(self.vies):
            screen.blit(self.coeur_image, (self.x + i * 45, self.y))


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()

        self.image = pygame.Surface((width, height))
        self.rect = pygame.Rect(x, y, width, height)
        self.width = width
        self.height = height
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)  # Positionner le joueur à (x, y)

        self.velocity_x = 0
        self.velocity_y = 0
        self.on_ground = False

        self.has_pistolet = False
        self.has_crayon = False
        self.has_KM = False


        self.on_ground = False

    def ramasser_pu(self, power_ups):
        """
        Permet au joueur de ramasser un PU s'il est proche.
        """
        for pu in power_ups[:]:  # On copie la liste pour éviter les erreurs pendant l'itération
            # Vérifier si le joueur est à proximité (zone de 50 pixels autour du PU)
            if self.rect.colliderect(pu.rect.inflate(50, 50)):  # 50px de détection
                print("Ramassé un PU !")
                power_ups.remove(pu)  # Retirer le PU de la liste
                return True
        return False


class Runtime:
    def __init__(self, window_size):

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

    def init_game_elements(self):
        self.platforms = pygame.sprite.Group()
        self.power_ups = pygame.sprite.Group()  # Correctement initialisé comme groupe de sprites

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
            self.power_ups.add(pu)  # Ajouter à self.power_ups qui est un groupe de sprites

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
        self.env.background = pygame.image.load("C:/Users/audem/Downloads/fond.png").convert_alpha()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.isRunning = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.gameState = "pause" if self.gameState == "game" else "game"
                elif event.key == pygame.K_z:  # Touche Z pour ramasser un PU
                    print("Touche Z pressée")
                    self.player.ramasser_pu(self.power_ups)

    def update(self):
        if self.gameState == "game":
            self.platforms.update()
            self.element_group.update()
            self.power_ups.update()
            self.player.update(self.env, self.camera)

    def run(self):
        while self.isRunning:
            events = pygame.event.get()
            self.handle_events()
            self.update()
            self.screen.fill("black")

            if self.gameState == "menu":
                self.menu.draw()
                self.menu.detect_click(events)

            elif self.gameState == "game":
                self.camera.update(self.player)  # MAJ caméra
                bg_rect = pygame.Rect(self.env.x + self.camera.offset_x, self.env.y, self.env.width, self.env.height)
                self.screen.blit(self.env.background, bg_rect)

                # Affichage du joueur
                self.player.draw(self.screen, self.camera)

                # Affichage des plateformes
                for plateforme in self.platforms:
                    self.screen.blit(plateforme.image, self.camera.apply(plateforme))

                # Affichage des Power-Ups
                for pu in self.power_ups:
                    self.screen.blit(pu.image, self.camera.apply(pu))

                # Affichage des éléments au sol
                for element in self.element_group:
                    self.screen.blit(element.image, self.camera.apply(element))

                # Affichage des blocs statiques
                for block in self.static_blocks:
                    block.draw(self.screen, self.camera)

                # Affichage de la barre de vie
                self.barre_de_vie.draw(self.screen)

            elif self.gameState == "pause":
                self.pauseMenu.draw()
                self.pauseMenu.detect_click(events)

            pygame.display.flip()
            self.dt = self.clock.tick(60) / 1000
