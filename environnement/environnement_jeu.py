import random, pygame

screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))

# Coordonnées fixes des plateformes
# Génerer des plateformes de 30px de large et 30px de haut à la suite ( avec des trous aléatoires)

def generate_platforms():
    plateformes_fixes = []
    for i in range(0, 1280, 50):
        if random.random() > 0.2:  # 80% de chance de créer une plateforme
            plateformes_fixes.append((i, 500, 50, 50))
    return plateformes_fixes


plateformes_fixes = generate_platforms()


# Coordonnées fixes des éléments au sol
elements_sol_fixes = [
    (100, 500, "porte"),
    (500, 500, "escalier"),
    (700, 500, "trou"),
    (1000, 500, "escalier"),
    (1200, 500, "crayon"),
]
sol_y = 500

positions_powerups = [(100, 500, "pistolet"), (400, 500, "pistolet"), (60, 500, "km")]

class Plateforme(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image_path):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

class Trottoir(Plateforme):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "assets/GROUND.jpg")

class Voiture(Plateforme):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "assets/VOITURE2.png")


class ElementAuSol(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image_path, type_element: str):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.type = type_element

class Porte(ElementAuSol):
    def __init__(self, x, y):
        super().__init__(x, y, "assets/PORTE1.png")

class Escalier(ElementAuSol):
    def __init__(self, x, y):
        super().__init__(x, y, "assets/ESCALIER1.png")

class Trou(ElementAuSol):
    def __init__(self, x, y):
        super().__init__(x, y, "assets/TROU1.png")

class Crayon(ElementAuSol):
    def __init__(self, x, y):
        super().__init__(x, y, "assets/crayon_JW.png")


class PU(pygame.sprite.Sprite):
    def __init__(self, x, y_platform, image_path, type_powerup):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = random.choice([y_platform - self.rect.height, 500])
        self.type = type_powerup
class Pistolet(PU):
    def __init__(self, x, y_platform, degats = 2):
        super().__init__(x, y_platform, "assets/PISTOLET_PA.jpg")
        self.degats = degats
class Kit_Med(PU):
    def __init__(self, x, y_platform):
        super().__init__(x, y_platform, "assets/KM_PA.jpg")














