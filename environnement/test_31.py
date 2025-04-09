import pygame
import random
from game.camera import Camera
# Définition des dimensions de l'écran
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
    (4500, 535, "porte "),
    (2000, 535, "escalier"),
    (10000, 535, "crayon"),

]

sol_y = 535  # Hauteur fixe pour les éléments au sol et les PU

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

        # Initialisation de la caméra
        self.camera = Camera(screen_width, screen_height, 20000)  # Exemple, largeur du monde 20000 px
        self.player = Player()  # Créer un joueur (ajoute le joueur dans le jeu)

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
        # Dessiner tous les éléments en fonction du décalage de la caméra
        for plateforme in self.plateformes:
            self.screen.blit(plateforme.image, self.camera.apply(plateforme))

        for pu in self.pu_group:
            self.screen.blit(pu.image, self.camera.apply(pu))

        for element in self.element_group:
            self.screen.blit(element.image, self.camera.apply(element))

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

            # Dessiner les éléments sans la caméra pour tester
            self.draw_elements()

            self.barre_de_vie.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(30)
            compteur += 1
            self.platforms.add(Plateforme(600, 400, 150, 20, "C:/Users/audem/Downloads/TROTTOIR.jpg"))