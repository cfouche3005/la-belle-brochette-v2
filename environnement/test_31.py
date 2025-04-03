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
    (3000, 535, 150, 20),
    (3500, 500, 150, 20),
    (4000, 250, 150, 20),
    (4500, 250, 150, 20),
    (5000, 400, 150, 20),
    (5500, 250, 150, 20),
    (6000, 450, 150, 20),

]

# Coordonnées fixes des éléments au sol
elements_sol_fixes = [
    (1000, 535, "escalier"),
    (500, 535, "escalier"),
    (40, 535, "porte"),
    (2000, 535, "escalier"),
    (700, 535, "trou"),
    (600, 535, "crayon")

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
        ElementAuSol.__init__(self, x, y, 50, 50, "C:/Users/audem/Downloads/ESCALIER.jpg")

class Trou(ElementAuSol):  # Nouveau type d'élément : Trou
    def __init__(self, x, y):
        ElementAuSol.__init__(self, x, y, 50, 50, "C:/Users/audem/Downloads/TROU.jpg")

class Crayon(ElementAuSol):
    def __init__(self, x, y):
        ElementAuSol.__init__(self, x, y, 50, 50, "C:/Users/audem/Downloads/CRAYON.jpg")


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
        self.damage = 1  # Enlève 1 vie
        self.munitions = 6

class Kit_Med(PU):
    def __init__(self, x, y_platform):
        super().__init__(x, y_platform, "C:/Users/audem/Downloads/MK.jpg")

class Piece(PU):
    def __init__(self, x, y_platform):
        super().__init__(x, y_platform, "C:/Users/audem/Downloads/PIECE.jpg")


class BarreDeVie:
    def __init__(self, max_vies=5):
        self.vies = max_vies
        self.max_vies = max_vies
        self.x = 20
        self.y = 20
        self.coeur_image = pygame.image.load("C:/Users/audem/Downloads/COEUR.jpg").convert_alpha()
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
        self.plateformes = pygame.sprite.Group()
        self.pu_group = pygame.sprite.Group()
        self.element_group = pygame.sprite.Group()
        self.init_plateformes()
        self.init_elements_sol()
        self.barre_de_vie = BarreDeVie()

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
        for x, y in [(1550, 250), (700, 250), (2000, 400), (1050, 250), (800, 250)]:  # X fixe, Y de la plateforme
            pu = random.choice([Pistolet(x, y), Kit_Med(x, y), Piece(x,y)])
            self.pu_group.add(pu)

    #fait avec GPT
    def draw_elements(self):
        # Dessiner tous les éléments en fonction du décalage de la caméra
        for plateforme in self.plateformes:
            self.screen.blit(plateforme.image, (plateforme.rect.x - self.camera_offset, plateforme.rect.y))

        for pu in self.pu_group:
            self.screen.blit(pu.image, (pu.rect.x - self.camera_offset, pu.rect.y))

        for element in self.element_group:
            self.screen.blit(element.image, (element.rect.x - self.camera_offset, element.rect.y))


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
            self.barre_de_vie.draw(self.screen)

            self.draw_elements()

          
            pygame.display.flip()
            self.clock.tick(60)
            compteur += 1

pygame.init()
game = Game()
game.run()
pygame.quit()
