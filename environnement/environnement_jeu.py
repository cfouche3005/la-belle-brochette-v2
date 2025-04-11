import random, pygame

from pygame.examples.midi import NullKey

screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))


def generer_niveau_coherent(largeur_totale=1280*2):  # 1280 * 2 = largeur par défaut
    """
    Génère un niveau de jeu avec des plateformes, des éléments au sol et des power-ups.
    :param largeur_totale: Largeur totale du niveau
    :return:
    """
    # Listes pour stocker les éléments du niveau
    plateformes = []
    elements_sol = []

    # Paramètres du niveau
    hauteur_sol = 500  # Y du premier étage (sol)
    hauteur_etage2 = 350  # Y du deuxième étage
    largeur_plateforme = 100
    hauteur_plateforme = 50

    # Génération du sol (premier étage) avec des trous
    x_courant = 0
    while x_courant < largeur_totale:
        # Ajout d'une plateforme au sol
        longueur_section = random.randint(3, 6) * largeur_plateforme  # Sections sol plus courtes

        for i in range(0, longueur_section, largeur_plateforme):
            if x_courant + i < largeur_totale:
                plateformes.append((x_courant + i, hauteur_sol, largeur_plateforme, hauteur_plateforme, "platform"))

        # Décision d'ajouter un trou ou une section de deuxième étage
        if random.random() < 0.6:  # 60% de chance d'avoir un trou (au lieu de 70%)
            taille_trou = random.randint(1, 2) * largeur_plateforme  # Trous plus petits
            # Ajout d'un trou dans les éléments au sol pour la collision
            elements_sol.append((x_courant + longueur_section // 2, hauteur_sol + 20, "trou"))
            x_courant += longueur_section + taille_trou
        else:
            # Pas de trou, mais ajout d'une section de deuxième étage
            x_courant += longueur_section

    # Génération du deuxième étage avec des escaliers au début
    x_courant = 100  # Commencer plus tôt
    while x_courant < largeur_totale - 300:  # Aller plus loin
        # Décider si on ajoute une section de deuxième étage
        if random.random() < 0.7:  # 70% de chance d'avoir une section (au lieu de 50%)
            # Ajouter un escalier au début de la section
            plateformes.append((x_courant, hauteur_etage2, largeur_plateforme,  hauteur_plateforme, "escalier"))

            # Longueur de la section de deuxième étage
            longueur_section = random.randint(4, 8) * largeur_plateforme  # Sections plus longues

            x_courant2 = x_courant + largeur_plateforme  # Commencer après l'escalier
            # Ajouter les plateformes du deuxième étage
            for i in range(0, longueur_section, largeur_plateforme):
                plateformes.append((x_courant2 + i, hauteur_etage2, largeur_plateforme, hauteur_plateforme, "platform"))

            # Parfois ajouter une porte ou un autre élément sur le deuxième étage
            if random.random() < 0.4:  # Plus de chance d'avoir des éléments
                element_type = random.choice(["porte", "crayon"])
                elements_sol.append((x_courant + longueur_section // 2, hauteur_etage2 - 20, element_type))

            x_courant += longueur_section + random.randint(1, 3) * largeur_plateforme  # Espacement plus court
        else:
            x_courant += random.randint(2, 4) * largeur_plateforme  # Espacement plus court

    # Ajouter quelques power-ups sur les plateformes
    positions_powerups = []
    for plat in plateformes:
        rand = random.random()
        print(rand)
        if rand < 0.5:
            power_up_type = random.choice(["chargeur", "km"])
            power_up_x = plat[0] + random.randint(10, 90)
            power_up_y = plat[1] - 30
            positions_powerups.append((power_up_x, power_up_y, power_up_type))

    return plateformes, elements_sol, positions_powerups

# Remplacer la génération actuelle par notre nouvelle fonction
plateformes_fixes, elements_sol_fixes, positions_powerups = generer_niveau_coherent()
sol_y = 500

class Plateforme(pygame.sprite.Sprite):
    """Représente une plateforme sur laquelle le joueur peut marcher ou interagir.
    """
    def __init__(self, x, y, width, height, image_path, type_platform: str):
        """
        Initialise la plateforme avec une image, une position et un type.
        :param x: Position x de la plateforme
        :param y: Position y de la plateforme
        :param width: Largeur de la plateforme
        :param height: Hauteur de la plateforme
        :param image_path: Chemin de l'image de la plateforme
        :param type_platform: Type de la plateforme (escalier, sol, etc.)
        """
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
        """
        Initialise l'élément au sol avec une image, une position et un type.
        :param x: Position x de l'élément
        :param y: Position y de l'élément
        :param width: Largeur de l'élément
        :param height: Hauteur de l'élément
        :param image_path: Chemin de l'image de l'élément
        :param type_element: Type de l'élément (porte, escalier, etc.)
        """
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















