import random, pygame

from pygame.examples.midi import NullKey

screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))

# Coordonnées fixes des plateformes
# Génerer des plateformes de 30px de large et 30px de haut à la suite ( avec des trous aléatoires)

def generate_platforms():
    plateformes_fixes = []
    for i in range(0, 5000, 50):
        if random.random() > 0.2:  # 80% de chance de créer une plateforme
            plateformes_fixes.append((i, 500, 100, 50, "platform"))
    return plateformes_fixes

plateformes_fixes = generate_platforms()
plateformes_fixes.append((40, 400, 50, 50, "escalier") )

# SAVE:
# plateformes_fixes = [
#     (100, 480, 125, 20),
#     (250, 440, 125, 20),
#     (40, 400, None, None, "escalier"),
#     (500, 410, 125, 20),
#     (750, 380, 125, 20),
#     (1000, 480, 125, 20),
#     (1250, 480, 125, 20),
#     (1450, 450, 125, 20),
#     (1590, 350, 125, 20),
#     (3500, 500, 125, 20),
#     (4000, 250, 150, 20),
#     (4500, 250, 150, 20),
#     (5000, 400, 150, 20),
#     (5500, 250, 150, 20),
#     (6000, 450, 150, 20),
# ]


# Coordonnées fixes des éléments au sol
elements_sol_fixes = [
    #(40, 400, "escalier"),
    (100, 520, "trou"),
    (250, 430, "porte"),
    (600, 520, "trou"),
    (900, 470, "porte"),
    (1200, 430, "escalier"),
    (1500, 430, "porte"),
    (1700, 520, "trou"),
    (1900, 430, "escalier"),
    (1000, 430, "crayon"),
]
sol_y = 450

def generate_powerups(plateformes_fixes):
    """ Génère des PUs ("chargeur" ou "km") aléatoirement, soit sur les plateformes fixes
    soit au sol (y = 450).
    Chaque plateforme a une probabilité de 40% de contenir un PU et
    la position x du power-up est légèrement décalée aléatoirement pour varier l'apparition.
    :param plateformes_fixes: Liste de tuples représentant les positions des plateformes (x, y)
    :return: Liste de tuples (x, y, type_powerup) représentant les power-ups générés
    """
    positions_powerups = []
    for plat in plateformes_fixes:
        if random.random() < 0.4:
            power_up_type = random.choice(["chargeur", "km"])
            if random.random() < 0.5:
                power_up_x = plat[0] + random.randint(0, 100)
                power_up_y = plat[1] - 25
            else:
                power_up_x = plat[0] + random.randint(0, 100)
                power_up_y = 450
            positions_powerups.append((power_up_x, power_up_y, power_up_type))
    return positions_powerups

class Plateforme(pygame.sprite.Sprite):
    """Représente une plateforme sur laquelle le joueur peut marcher ou interagir.
    """
    def __init__(self, x, y, width, height, image_path, type_platform: str):
        super().__init__()
        self.width = width
        self.height = height
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 40))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.type = type_platform

class Trottoir(Plateforme):
    """Sous-classe de Plateforme représentant un trottoir spécifique avec une image par défaut"""
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "assets/GROUND.jpg")


class ElementAuSol(pygame.sprite.Sprite):
    """Classe générique pour tous les éléments posés au sol que le joueur peut ramasser ou avec lesquels il peut interagir"""
    def __init__(self, x, y, width, height, image_path, type_element: str):
        super().__init__()
        self.width = width
        self.height = height
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 70 ))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.type = type_element
        self.type = type_element #Aide de GPT qui a indiqué qu'il fallait ajouter le .type dans la fonction
        self.etat = "fermée"

    def ouvrir(self):
        """
        la fonction ouvrir a été placée dans la classe mère car le code renvoyait des erreurs si elle était placée dans la classe Porte.
        J'ai fait des prints pour voir où étaient les erreurs et je me suis aperçue que le code rencontrait des pb à différencier "type_element" lorsque
        la fonction ouvrir était placée dans la classe Porte. Ce problème s'est résolu quand j'ai mis la fonction ouvrir dans la classe mère "ElementAuSol"
        """
        self.etat = "ouverte"
        self.image_ouverte = ("assets/porte_ouverte.jpg")
        self.image = pygame.image.load(self.image_ouverte).convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 70))

class Porte(ElementAuSol):
    """Porte que le joueur peut ouvrir avec la fonction ouvrir située dans la classe mère ElementAuSol"""
    def __init__(self, x, y,  type_element):
        super().__init__(x, y, type_element, "assets/porte_noire.png" )

class Escalier(ElementAuSol):
    """Escalier utilisable par le joueur pour changer de niveau ou de plateforme."""
    def __init__(self, x, y):
        super().__init__(x, y, "assets/escalier_urbain.png")

class Trou(ElementAuSol):
    """Représente un trou dans lequel le joueur peut potentiellement tomber"""
    def __init__(self, x, y):
        super().__init__(x, y, "assets/trou_sol.png")

class Crayon(ElementAuSol):
    """arme apparaissant une fois dans le jeu"""
    def __init__(self, x, y):
        super().__init__(x, y, "assets/crayon.png")


class PU(pygame.sprite.Sprite):
    """Classe de base pour les PUs qui donnent un effet (redonner de la vie) ou objet (munitions) au joueur"""
    def __init__(self, x, y_platform, image_path, type_powerup):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y_platform
        self.type = type_powerup

class Chargeur(PU):
    """Power-up spécifique représentant un chargeur de munitions"""
    def __init__(self, x, y_platform ):
        super().__init__(x, y_platform, "assets/munition.png", "chargeur")

class Kit_Med(PU):
    """Power-up spécifique représentant un kit médical (km)"""
    def __init__(self, x, y_platform):
        super().__init__(x, y_platform, "assets/kit_medical.png", "km")















