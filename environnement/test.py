import pygame
import random

# Initialisation de Pygame
pygame.init()

# Paramètres de la fenêtre
screen_width = 1500
screen_height = 900
screen = pygame.display.set_mode((screen_width, screen_height))


# Définir la classe des Plateformes
class Plateforme(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

class Trottoir(Plateforme):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, (255, 255, 255))

class Voiture(Plateforme):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, (255, 0, 0))

# Définir la classe des Power-Ups (PU)
class PU(pygame.sprite.Sprite):
    def __init__(self, plateformes):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill((255, 255, 0))  # Jaune
        self.rect = self.image.get_rect()
        self.coordonnees = self.positionner(plateformes)

    def positionner(self, plateformes):
        plateformes_liste = list(plateformes)  # Convertir le groupe en liste
        if random.random() < 0.5 and plateformes_liste:
            # 50% de chance d'être sur une plateforme
            plateforme = random.choice(plateformes_liste)
            self.rect.x = random.randint(plateforme.rect.left, plateforme.rect.right - self.rect.width)
            self.rect.y = plateforme.rect.top - self.rect.height

        else:
            # 50% de chance d'être au sol
            self.rect.x = random.randint(50, screen_width - 50)
            self.rect.y = screen_height - self.rect.height
class Pistolet(PU):
    def __init__(self, plateformes):
        super().__init__(plateformes)
        self.image.fill((255, 0, 0))  # Rouge pour les pistolets

class Kit_Med(PU):
    def __init__(self, plateformes):
        super().__init__(plateformes)
        self.image.fill((0, 255, 0))  # Vert pour les kits médicaux

class Game:
    def __init__(self):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.isRunning = True
        self.plateformes = pygame.sprite.Group()
        self.pu_group = pygame.sprite.Group()

    def apparitions_plateformes(self):
        # Apparition des plateformes aléatoires avec une séparation verticale
        x_pos = random.randint(0, screen_width - 100)
        y_pos = random.randint(200, screen_height - 100)

        # S'assurer que la nouvelle plateforme ne chevauche aucune autre
        while self.is_plateforme_overlapping(x_pos, y_pos):
            y_pos = random.randint(200, screen_height - 100)  # Réessayer avec une autre position y

        # Choisir aléatoirement si la plateforme est un trottoir ou une voiture
        if random.random() < 0.5:  # 50% de chance de générer une voiture
            platform = Voiture(x_pos, y_pos, random.randint(100, 200), 20)
        else:  # Sinon générer un trottoir
            platform = Trottoir(x_pos, y_pos, random.randint(100, 200), 20)

        self.plateformes.add(platform)

    def is_plateforme_overlapping(self, x, y):
        """Vérifie si la nouvelle plateforme chevauche une plateforme existante"""
        for platform in self.plateformes:
            if platform.rect.colliderect(pygame.Rect(x, y, platform.rect.width, platform.rect.height)):
                return True  # Si la nouvelle plateforme touche une autre plateforme, elle est en collision
        return False  # Si aucune collision n'est détectée

    def apparitions_PUs(self):
        # Apparition des Power-Ups
        if random.random() < 0.8:
            if random.random() < 0.5:
                pu = Pistolet(self.plateformes)
            else:
                pu = Kit_Med(self.plateformes)
            self.pu_group.add(pu)

    def run(self):
        # Fonction pour démarrer et gérer le jeu
        background = pygame.Surface((screen_width, screen_height))
        background.fill((0, 0, 255))  # Fond bleu
        self.screen.blit(background, (0, 0))

        compteur = 0  # Compteur pour les apparitions

        while self.isRunning:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.isRunning = False

            # Apparition des plateformes et power-ups
            if compteur % 60 == 0:
                self.apparitions_plateformes()
                self.apparitions_PUs()

            # Afficher les plateformes
            for platform in self.plateformes:
                self.screen.blit(platform.image, platform.rect.topleft)

            # Afficher les power-ups
            for pu in self.pu_group:
                self.screen.blit(pu.image, pu.rect.topleft)

            pygame.display.flip()  # Mise à jour de l'affichage
            self.dt = self.clock.tick(60) / 1000
            compteur += 1


# Créer et démarrer le jeu
game = Game()
game.run()

# Quitter Pygame
pygame.quit()