import pygame
import random

# Définition des dimensions de l'écran
screen_width = 1280
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))


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


class PU(pygame.sprite.Sprite):
    def __init__(self, plateformes, x, y, image_path):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()  # Charger l'image
        self.image = pygame.transform.scale(self.image, (50, 50))  # Redimensionner l'image
        self.rect = self.image.get_rect()
        self.coordonnees = self.positionner(plateformes)

    def positionner(self, plateformes):
        plateformes_liste = list(plateformes)  # Convertir le groupe en liste
        if random.random() < 0.5 and plateformes_liste:
            plateforme = random.choice(plateformes_liste)
            # S'assurer que l'intervalle est valide pour random.randint()
            left = plateforme.rect.left
            right = plateforme.rect.right
            if left < right:
                self.rect.x = random.randint(left, right - self.rect.width)
                self.rect.y = plateforme.rect.top - self.rect.height
            else:
                self.rect.x = random.randint(50, screen_width - 50)
                self.rect.y = screen_height - self.rect.height
        else:
            self.rect.x = random.randint(50, screen_width - 50)
            self.rect.y = screen_height - self.rect.height


class Pistolet(PU):
    def __init__(self, plateformes):
        super().__init__(plateformes, 50, 50, "C:/Users/audem/Downloads/PISTOLET.jpg")


class Kit_Med(PU):
    def __init__(self, plateformes):
        super().__init__(plateformes, 50, 50, "C:/Users/audem/Downloads/MK.jpg")


class Game:
    def __init__(self):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.isRunning = True
        self.plateformes = pygame.sprite.Group()
        self.pu_group = pygame.sprite.Group()
        self.element_group = pygame.sprite.Group()  # Initialiser le groupe pour les éléments au sol

    def apparitions_plateformes(self, nombre_plateformes=5):
        self.plateformes.empty()  # Réinitialiser les plateformes existantes

        for _ in range(nombre_plateformes):
            x_pos = random.randint(0, screen_width - 100)
            y_pos = random.randint(400, screen_height - 100)

            while self.is_plateforme_overlapping(x_pos, y_pos):  # Vérifier la superposition
                x_pos = random.randint(0, screen_width - 100)
                y_pos = random.randint(400, screen_height - 100)

            plateforme = Voiture(x_pos, y_pos, random.randint(100, 200), 20) if random.random() < 0.5 else Trottoir(
                x_pos, y_pos, random.randint(100, 200), 20)

            self.plateformes.add(plateforme)

    def is_plateforme_overlapping(self, x, y):
        """Vérifie si la nouvelle plateforme chevauche une autre plateforme."""
        for platform in self.plateformes:
            if platform.rect.colliderect(pygame.Rect(x, y, platform.rect.width, platform.rect.height)):
                return True  # Si la nouvelle plateforme touche une autre plateforme
        return False

    def apparitions_PUs(self, nombre_PU=5):  # Définit un nombre de PU fixe par défaut
        self.pu_group.empty()  # Réinitialise les power-ups existants

        for _ in range(nombre_PU):  # Générer le nombre exact de PU
            pu = random.choice([Pistolet(self.plateformes), Kit_Med(self.plateformes)])

            if not self.is_element_overlapping(pu):
                self.pu_group.add(pu)
    def apparitions_elements_au_sol(self, nombre_elements=3):
        self.element_group.empty()  # Réinitialiser les éléments existants
        for _ in range(nombre_elements):
            x_pos = random.choice((100, 1000))
            y_pos = screen_height - 50  # Toujours au sol

            element = Porte(x_pos, y_pos) if random.random() < 0.5 else Escalier(x_pos, y_pos)

            while self.is_element_overlapping(element):  # Vérifier la superposition fait avec GPT
                x_pos = random.randint(50, screen_width - 50)
                element.rect.x = x_pos  # Mettre à jour la position
            self.element_group.add(element)

    def is_elt_sol_overlapping(self, x, y):
        for ES in self.element_group:
            if ES.rect.colliderect(pygame.Rect(x, y, ES.width, ES.height)):
                return True
        return False


    def is_element_overlapping(self, new_element):
        """Vérifie si un élément est en superposition avec un autre."""
        for pu in self.pu_group:
            if new_element.rect.colliderect(pu.rect):
                return True

        for element in self.element_group:
            if new_element.rect.colliderect(element.rect):
                return True

        for plateforme in self.plateformes:
            if new_element.rect.colliderect(plateforme.rect):
                return True

        return False

    def run(self):
        """Gère le cycle du jeu."""
        background = pygame.image.load("C:/Users/audem/Downloads/fond.png").convert_alpha()
        background = pygame.transform.scale(background, (screen_width, screen_height))  # Redimensionner l'image
        self.screen.blit(background, (0, 0))

        compteur = 0
        while self.isRunning:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.isRunning = False

            if compteur % 60 == 0:
                self.apparitions_plateformes(1)
                self.apparitions_PUs(2)
                self.apparitions_elements_au_sol(1)

            # Dessiner
            for platform in self.plateformes:
                self.screen.blit(platform.image, platform.rect.topleft)

            for pu in self.pu_group:
                self.screen.blit(pu.image, pu.rect.topleft)

            for element in self.element_group:
                self.screen.blit(element.image, element.rect.topleft)

            pygame.display.flip()  # Mise à jour de l'affichage
            self.dt = self.clock.tick(60) / 1000
            compteur += 1

# Créer et démarrer le jeu
pygame.init()
game = Game()
game.run()
pygame.quit()
