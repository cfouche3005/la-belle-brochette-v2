import pygame
import random

# Définition des dimensions de l'écran
screen_width = 1280
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))

# Coordonnées fixes des plateformes (X fixe, Y fixe)
plateformes_fixes = [
    (90, 535, 150, 20),
    (300, 500, 150, 20),
    (750, 250, 150, 20),
    (1000, 250, 150, 20),
    (1500, 400, 150, 20),
    (2500, 250, 150, 20),
    (500, 450, 150, 20),

]

# Coordonnées fixes des éléments au sol
elements_sol_fixes = [
    (1000, 535, "escalier"),
    (500, 535, "escalier"),
    (40, 535, "porte"),
    (2000, 535, "escalier"),
    (700, 535, "trou")
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
        super().__init__(x, y, width, height, "C:/Users/audem/Downloads/TROTTOIR.jpg")

class Voiture(Plateforme):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "C:/Users/audem/Downloads/VOITURE.jpg")

class ElementAuSol(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image_path):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

class Porte(ElementAuSol):
    def __init__(self, x, y):
        super().__init__(x, y, 50, 50, "C:/Users/audem/Downloads/PORTE.jpg")

class Escalier(ElementAuSol):
    def __init__(self, x, y):
        super().__init__(x, y, 50, 50, "C:/Users/audem/Downloads/ESCALIER.jpg")

class Trou(ElementAuSol):  # Nouveau type d'élément : Trou
    def __init__(self, x, y):
        # Tu peux choisir une image de ton choix pour le trou, ici on suppose qu'une image "TROU.jpg" existe
        ElementAuSol.__init__(self, x, y, 50, 50, "C:/Users/audem/Downloads/TROU.jpg")

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
        super().__init__(x, y_platform, "C:/Users/audem/Downloads/PISTOLET.jpg")

class Kit_Med(PU):
    def __init__(self, x, y_platform):
        super().__init__(x, y_platform, "C:/Users/audem/Downloads/MK.jpg")


class Game:
    def __init__(self):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.isRunning = True
        self.plateformes = pygame.sprite.Group()
        self.pu_group = pygame.sprite.Group()
        self.element_group = pygame.sprite.Group()
        self.init_plateformes()
        self.init_elements_sol()

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
            self.element_group.add(element)

    def apparitions_PUs(self):
        self.pu_group.empty()
        for x, y in [(1550, 250), (800, 250), (2000, 400), (1050, 250), (800, 250)]:  # X fixe, Y de la plateforme
            pu = random.choice([Pistolet(x, y), Kit_Med(x, y)])
            self.pu_group.add(pu)


    def check_chute_trou(self): #fait avec GPT
        for trou in self.element_group:
            if isinstance(trou, Trou) and self.player.rect.colliderect(trou.rect):
                self.player_dies()  # Le joueur meurt si collision avec le trou

    def player_dies(self): #fait avec GPT
        print("Le joueur est tombé dans un trou et est mort!")
        self.isRunning = False


    def run(self):
        background = pygame.image.load("C:/Users/audem/Downloads/fond.png").convert_alpha()
        background = pygame.transform.scale(background, (screen_width, screen_height))
        self.screen.blit(background, (0, 0))

        compteur = 0
        while self.isRunning:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.isRunning = False

            if compteur % 120 == 0:
                self.apparitions_PUs()

            self.screen.blit(background, (0, 0))

            self.plateformes.draw(self.screen)
            self.pu_group.draw(self.screen)
            self.element_group.draw(self.screen)

            self.check_chute_trou()
            pygame.display.flip()
            self.clock.tick(60)
            compteur += 1

pygame.init()
game = Game()
game.run()
pygame.quit()
