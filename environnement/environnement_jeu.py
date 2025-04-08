import random, pygame

screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))

# Coordonnées fixes des plateformes
plateformes_fixes = [
    (100, 200, 10, 20),
    (250, 200, 150, 20),
    (400, 200, 150, 20),
    (590, 200, 150, 20),
    (1000, 200, 150, 20),
    (1250, 300, 150, 20),
    (1400, 300, 150, 20),
    (1590, 300, 150, 20),
    (3500, 500, 150, 20),
    (4000, 250, 150, 20),
    (4500, 250, 150, 20),
    (5000, 400, 150, 20),
    (5500, 250, 150, 20),
    (6000, 450, 150, 20),
]

# Coordonnées fixes des éléments au sol
elements_sol_fixes = [
    (100, 500, "porte"),
    (500, 500, "escalier"),
]
sol_y = 475

positions_powerups = [(300, 600), (1050, 550), (1640, 475), (3550, 400)]
# Classe des plateformes
class Plateforme(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image_path):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
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
        self.image = pygame.transform.scale(self.image, (50, 50))
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
        super().__init__(x, y, "C:/Users/audem/Downloads/TROU1.png")


class Crayon(ElementAuSol):
    def __init__(self, x, y):
        super().__init__(x, y, "C:/Users/audem/Downloads/crayon_JW.png")


class PU(pygame.sprite.Sprite):
    def __init__(self, x, y_platform, image_path):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = random.choice([y_platform - self.rect.height, 475])
        print(f"PU créé à : {self.rect}")


class Pistolet(PU):
    def __init__(self, x, y_platform):
        super().__init__(x, y_platform, "C:/Users/audem/Downloads/PISTOLET.jpg")
        self.damage = 1


class Kit_Med(PU):
    def __init__(self, x, y_platform):
        super().__init__(x, y_platform, "C:/Users/audem/Downloads/MK.jpg")


class Piece(PU):
    def __init__(self, x, y_platform):
        super().__init__(x, y_platform, "C:/Users/audem/Downloads/PIECE.jpg")

    def init_game_elements(self):
        self.platforms = pygame.sprite.Group()
        self.power_ups = pygame.sprite.Group()
        self.element_group = pygame.sprite.Group()














