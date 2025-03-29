import random
import pygame
import pygame as pg
from pygame.sprite import Sprite

class Plateforme:
    def __init__(self, coor):
        self.coordonnees = coor
        self.rect = pygame.Rect(coor[0], coor[1], 50, 50)  # On crée un rect basé sur coordonnees
    def get_coor(self):
        return self.coordonnees

    def deplacement_plateforme(self):
        x1 = self.coordonnees[0]
        x2 = random.randint(-1, 1)
        y1 = self.coordonnees[1]
        y2 = random.randint(-1, 1)

        #avec GPT pour éviter que les plateformes sortent de la fenêtre
        x1 = max(0, min(x1, self.width - 50))
        y1 = max(0, min(y1, self.height - 50))

        self.coordonnees = (x1 + x2, y1 + y2)
        self.rect.topleft = self.coordonnees

    def set_y(self, y):
        self.coordonnees = (self.coordonnees[0], y)
        self.rect.y = y
    def set_x(self, x):
        self.coordonnees = (x, self.coordonnees[1])
        self.rect.x = x

class Voitures(Plateforme, pygame.sprite.Sprite):
    def __init__(self, coor, x, y, width, height):
        Plateforme.__init__(self, coor)

        # Empêcher de sortir de l'écran
        x = max(0, min(x, width - 50))
        y = max(0, min(y, height - 50))
        self.image = pygame.image.load("C:/Users/audem/Downloads/VOITURE.jpg")
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        # Redimensionner l'image  AVEC GPT
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()  # Recréer le rect avec la nouvelle taille de l'image
        self.rect.topleft = (x, y)

    def get_coor(self):
        return self.rect.topleft

class Trottoir(Plateforme, pygame.sprite.Sprite):
    def __init__(self, coor, x, y, width, height):
        Plateforme.__init__(self, coor)

        # Empêcher de sortir de l'écran
        x = max(0, min(x, width - 50))
        y = max(0, min(y, height - 50))

        self.image = pygame.image.load("C:/Users/audem/Downloads/TROTTOIR.jpg")

        # Redimensionner l'image  AVEC GPT
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()  # Recréer le rect avec la nouvelle taille de l'image
        self.rect.topleft = (x, y)

    def get_coor(self):
        return self.rect.topleft

class Banc(Plateforme):
    def __init__(self, coor):
        Plateforme.__init__(self, coor)


class Elt_Sol:
    def __init__(self, x):
        self.coordonnees = (x, 0)

    def get_coor(self):
        return self.coordonnees

    def apparition_elt_sol(self):
        x1 = self.coordonnees[0]
        x2 = random.randint(-1, 1)
        self.coordonnees = (x1 + x2, 0)

    def set_x(self, x):
        self.coordonnees = (x, 0)


class Escaliers(Elt_Sol, pygame.sprite.Sprite):
    def __init__(self, coor, x, y):
        Elt_Sol.__init__(self, coor)
        self.image = pygame.image.load("C:/Users/audem/Downloads/ESCALIER.jpg")
        # Redimensionner l'image  AVEC GPT
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()  # Recréer le rect avec la nouvelle taille de l'image
        self.rect.topleft = (x, y)

    def get_coor(self):
        return self.rect.topleft

class Portes(Elt_Sol, pygame.sprite.Sprite):
    def __init__(self, coor, x, y):
        Elt_Sol.__init__(self, coor)
        self.image = pygame.image.load("C:/Users/audem/Downloads/PORTE.jpg")

        # Redimensionner l'image  AVEC GPT
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()  # Recréer le rect avec la nouvelle taille de l'image
        self.rect.topleft = (x, y)

    def get_coor(self):
        return self.rect.topleft

class PU:
    def __init__(self, trottoirs, voitures, sol):

        self.coordonnees = (0,0)
        plateformes = trottoirs + voitures
        #les PU seront soit sur les platefomes soit sur le sol, elles seront placées de manière aléatoire fait avec GPT
        if plateformes:
            plateforme = random.choice(plateformes)
            x, y = plateforme.get_coor()
            self.coordonnees = (x, y-50)
        else:
            x = random.randint(0, sol - 50)
            self.coordonnees = (x, sol)


        self.image = None  # Défini pour éviter les erreurs
        self.rect = pygame.Rect(self.coordonnees[0], self.coordonnees[1], 50, 50)  # Crée un rect directement
        self.rect.topleft = self.coordonnees
        print(f"Plateforme choisie: {plateforme.get_coor()} - PU placé à {self.coordonnees}")
    def get_coor(self):
        return self.coordonnees


class Pistolet(PU, pygame.sprite.Sprite):
    def __init__(self, trottoirs, voitures, sol):
        PU.__init__(self, trottoirs, voitures, sol)
        self.image = pygame.image.load("C:/Users/audem/Downloads/PISTOLET.jpg")
        self.image = pygame.transform.scale(self.image, (50, 50))  # Redimensionner
        self.rect.topleft = self.coordonnees


class Crayon(PU, pygame.sprite.Sprite):
    def __init__(self, trottoirs, voitures, sol):
        PU.__init__(self, trottoirs, voitures, sol)
        self.image = pygame.image.load("C:/Users/audem/Downloads/CRAYON.jpg")
        self.image = pygame.transform.scale(self.image, (50, 50))  # Redimensionner
        self.rect.topleft = self.coordonnees


class Kit_Med(PU, pygame.sprite.Sprite):
    def __init__(self, trottoirs, voitures, sol):
        PU.__init__(self, trottoirs, voitures, sol)
        self.image = pygame.image.load("C:/Users/audem/Downloads/MK.jpg")
        self.image = pygame.transform.scale(self.image, (50, 50))  # Redimensionner
        self.rect.topleft = self.coordonnees


class Environnement:
    def __init__(self, width, height, n_escaliers, n_portes, n_pistolets, n_crayon, n_KMs, n_voitures, n_trottoirs):
        self.width = width
        self.height = height
        self.voitures = []
        self.escaliers = []
        self.portes = []
        self.trottoirs = []
        self.KMs = []
        self.pistolets = []
        self.crayons = []

        for a in range(n_trottoirs):
            x, y = random.randint(0, width - 50 ), random.randint(0, height - 50)
            coor = (x, y)
            self.trottoirs.append(Trottoir(coor, x, y, width, height))

        for b in range(n_voitures):
            x, y = random.randint(0, width - 50), random.randint(0, height- 50)
            coor = (x, y)
            self.voitures.append(Voitures(coor, x, y, width, height))

        for c in range(n_escaliers):
            x= (random.randint(0, width - 50) )
            y = height - 50
            coor = (x, y)
            self.escaliers.append(Escaliers(coor, x, y))

        for d in range(n_portes):
            x = (random.randint(0, width - 50))
            y = height - 50
            coor = (x, y)
            self.portes.append(Portes(coor, x, y))

        for e in range(n_crayon):
            self.crayons.append(Crayon(self.trottoirs, self.voitures,self.height))

        for f in range(n_KMs):
            self.KMs.append(Kit_Med(self.trottoirs, self.voitures, self.height))

        for g in range(n_pistolets):
            self.pistolets.append(Pistolet(self.trottoirs,self.voitures, self.height))

class Game:
    def __init__(self, window_size):
        # Pygame initialization
        pygame.init()
        self.screen = pygame.display.set_mode(window_size)
        self.clock = pygame.time.Clock()
        self.dt = 0
        self.isRunning = True

        self.voitures = []
        self.escaliers = []
        self.portes = []
        self.trottoirs = []
        self.KMs = []
        self.pistolets = []
        self.crayons = []

    def setup(self, env):
        self.voitures = env.voitures
        self.escaliers = env.escaliers
        self.portes = env.portes
        self.trottoirs = env.trottoirs
        self.KMs = env.KMs
        self.pistolets = env.pistolets
        self.crayons = env.crayons

    def run(self):
        while self.isRunning:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.isRunning = False

            self.screen.fill("white")

            for voiture in self.voitures:
                self.screen.blit(voiture.image, voiture.rect.topleft)
            for trottoir in self.trottoirs:
                self.screen.blit(trottoir.image, trottoir.rect.topleft)
            for porte in self.portes:
                self.screen.blit(porte.image, porte.rect.topleft)
            for escaliers in self.escaliers:
                self.screen.blit(escaliers.image, escaliers.rect.topleft)
            for pistolet in self.pistolets:
                self.screen.blit(pistolet.image, pistolet.rect.topleft)
            for crayon in self.crayons:
                self.screen.blit(crayon.image, crayon.rect.topleft)
            for KM in self.KMs:
                self.screen.blit(KM.image, KM.rect.topleft)

            pygame.display.flip()
            self.dt = self.clock.tick(60) / 1000

        pygame.quit()


if __name__ == "__main__":
    game = Game((1380, 1000))
    env = Environnement(1380, 1000, 10, 10, 20, 1, 10, 9, 10)
    game.setup(env)
    game.run()


pygame.quit()
