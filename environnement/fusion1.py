import pygame
import random
from entities.player.player import Player
from game.env import Env
from game.camera import Camera
from menu.menu import Menu
from entities.staticblock import StaticBlock

# Paramètres de l'écran
screen_width = 1450
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))

# Coordonnées fixes des plateformes
plateformes_fixes = [
    (100, 500, 150, 20),
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


# Classe des plateformes
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
        super().__init__(x, y, 50, 50, "C:/Users/audem/Downloads/ESCALIER1.png")

class Trou(ElementAuSol):
    def __init__(self, x, y):
        super().__init__(x, y, 50, 50, "C:/Users/audem/Downloads/TROU1.png")

class Crayon(ElementAuSol):
    def __init__(self, x, y):
        super().__init__(x, y, 50, 50, "C:/Users/audem/Downloads/crayon_JW.png")


# Classe des Power-Ups
class PU(pygame.sprite.Sprite):
    def __init__(self, x, y_platform, image_path):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = random.choice([y_platform - self.rect.height, sol_y])


class Pistolet(PU):
    def __init__(self, x, y_platform):
        super().__init__(x, y_platform, "C:/Users/audem/Downloads/PISTOLET_PA.png")
        self.damage = 1
        self.munitions = 6

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
        self.coeur_image = pygame.transform.scale(self.coeur_image, (40, 40))

    def perdre_vie(self, damage):
        self.vies -= damage
        if self.vies < 0:
            self.vies = 0

    def draw(self, screen):
        for i in range(self.vies):
            screen.blit(self.coeur_image, (self.x + i * 45, self.y))


import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()

        # Initialisation de l'image et du rectangle
        self.image = pygame.Surface((width, height))
        self.rect = pygame.Rect(x, y, width, height)
        self.width = width
        self.height = height
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)  # Positionner le joueur à (x, y)

        # Attributs pour la physique du joueur
        self.velocity_x = 0
        self.velocity_y = 0
        self.on_ground = False

        # Attributs supplémentaires pour l'inventaire du joueur
        self.has_pistolet = False
        self.has_crayon = False
        self.has_KM = False

    def update(self, platforms, keys, env):
        # Vérifier la largeur de l'environnement pour ne pas sortir de l'écran
        if self.rect.x > env.width - self.width:
            self.rect.x = env.width - self.width
        elif self.rect.x < 0:
            self.rect.x = 0

        # Détecter les collisions avec les plateformes
        self.on_ground = False
        for plateforme in platforms:
            if self.rect.colliderect(plateforme.rect):
                # Si on touche une plateforme, on se place juste au-dessus
                if self.velocity_y > 0 and self.rect.bottom <= plateforme.rect.top:
                    self.rect.bottom = plateforme.rect.top
                    self.on_ground = True
                    # Si on est au sol, on avance selon les touches directionnelles
                    self.velocity_x = 5 if keys[pygame.K_RIGHT] else -5 if keys[pygame.K_LEFT] else self.velocity_x

        # Déplacer le joueur horizontalement en fonction des touches pressées
        if keys[pygame.K_RIGHT]:
            self.velocity_x = 5
        elif keys[pygame.K_LEFT]:
            self.velocity_x = -5
        else:
            self.velocity_x = 0

        # Appliquer la vitesse horizontale
        self.rect.x += self.velocity_x

        # Appliquer la vitesse verticale (gravité)
        self.rect.y += self.velocity_y

    def jump(self):
        # Ne peut sauter que si le joueur est sur le sol
        if self.on_ground:
            self.velocity_y = -15  # La vitesse du saut
            self.on_ground = False

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
            self.screen.fill("black")

            if self.gameState == "menu":
                self.menu.draw()
                self.menu.detect_click(events)

            elif self.gameState == "game":
                self.camera.update(self.player)  # MAJ caméra
                bg_rect = pygame.Rect(self.env.x + self.camera.offset_x, self.env.y, self.env.width, self.env.height)
                self.screen.blit(self.env.background, bg_rect)

                self.player.draw(self.screen, self.camera)

                for plateforme in self.platforms:
                    self.screen.blit(plateforme.image, self.camera.apply(plateforme))

                for pu in self.power_ups:
                    self.screen.blit(pu.image, self.camera.apply(pu))

                for element in self.element_group:
                    self.screen.blit(element.image, self.camera.apply(element))

                for block in self.static_blocks:
                    block.draw(self.screen, self.camera)

                self.barre_de_vie.draw(self.screen)

            elif self.gameState == "pause":
                self.pauseMenu.draw()
                self.pauseMenu.detect_click(events)

            pygame.display.flip()
            self.dt = self.clock.tick(60) / 1000

        pygame.quit()
