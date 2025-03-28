import random
import pygame
import pygame as pg
from pygame.sprite import Sprite

class Plateforme:
    def __init__(self, coor):
        self.coordonnees = coor

    def get_coor(self):
        return self.coordonnees

    def deplacement_plateforme(self):
        x1 = self.coordonnees[0]
        x2 = random.randint(-1, 1)
        y1 = self.coordonnees[1]
        y2 = random.randint(-1, 1)
        self.coordonnees = (x1 + x2, y1 + y2)

    def set_y(self, y):
        self.coordonnees = (self.coordonnees[0], y)

    def set_x(self, x):
        self.coordonnees = (x, self.coordonnees[1])


class Voitures(Plateforme, pygame.sprite.Sprite):
    def __init__(self, coor, x, y):
        Plateforme.__init__(self, coor)
        self.image = pygame.image.load("C:/Users/audem/Downloads/voiture.jpg")
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        # Redimensionner l'image (par exemple, la redimensionner à 50x60) AVEC GPT
        self.image = pygame.transform.scale(self.image, (70, 60))  # Redimensionner à 50x60 pixels
        self.rect = self.image.get_rect()  # Recréer le rect avec la nouvelle taille de l'image
        self.rect.topleft = (x, y)


class Trottoir(Plateforme, pygame.sprite.Sprite):
    def __init__(self, coor, x, y):
        Plateforme.__init__(self, coor)
        self.image = pygame.image.load("C:/Users/audem/Downloads/trottoir.jpg")
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        # Redimensionner l'image (par exemple, la redimensionner à 50x60) AVEC GPT
        self.image = pygame.transform.scale(self.image, (50, 50))  # Redimensionner à 50x60 pixels
        self.rect = self.image.get_rect()  # Recréer le rect avec la nouvelle taille de l'image
        self.rect.topleft = (x, y)

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


class Escaliers(Elt_Sol):
    def __init__(self, coor):
        Elt_Sol.__init__(self, coor)


class Portes(Elt_Sol):
    def __init__(self, coor):
        Elt_Sol.__init__(self, coor)


class PU:
    def __init__(self, plateformes, sol):
        self.sol = sol
        if plateformes and random.choice([True, False]):
            plateforme = random.choice(plateformes)
            self.coordonnees = plateforme.get_coor()
        else:
            x = random.randint(0, sol - 1)  # sol est ici le sol du jeu
            self.coordonnees = (x, 0)

    def get_coor(self):
        return self.coordonnees


class Pistolet(PU):
    def __init__(self, plateformes, sol):
        PU.__init__(self, plateformes, sol)


class Crayon(PU):
    def __init__(self, plateformes, sol):
        PU.__init__(self, plateformes, sol)


class Kit_Med(PU):
    def __init__(self, plateformes, sol):
        PU.__init__(self, plateformes, sol)


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
            x, y = random.randint(0, width - 1), random.randint(0, height - 1)
            coor = (x, y)
            self.trottoirs.append(Trottoir(coor, x, y))

        for b in range(n_voitures):
            x, y = random.randint(0, width - 1), random.randint(0, height - 1)
            coor = (x, y)
            self.voitures.append(Voitures(coor, x, y))

        for c in range(n_escaliers):
            coor = (random.randint(0, width - 1), random.randint(0, height - 1))
            self.escaliers.append(Escaliers(coor))

        for d in range(n_portes):
            coor = (random.randint(0, width - 1), random.randint(0, height - 1))
            self.portes.append(Portes(coor))

        for e in range(n_crayon):
            coor = (random.randint(0, width - 1), random.randint(0, height - 1))
            self.crayons.append(PU([Trottoir((0, 0), x, y)], 10))  # List of platforms needed

        for f in range(n_KMs):
            coor = (random.randint(0, width - 1), random.randint(0, height - 1))
            self.KMs.append(PU([Trottoir((0, 0), x, y)], 10))  # List of platforms needed

        for g in range(n_pistolets):
            coor = (random.randint(0, width - 1), random.randint(0, height - 1))
            self.pistolets.append(PU([Trottoir((0, 0), x, y)], 10))  # List of platforms needed

    def get_coor_n_trottoirs(self):
        coor = []
        for trottoir in self.trottoirs:
            coor.append(trottoir.get_coor())
        return coor

    def get_coor_n_escaliers(self):
        coor = []
        for escalier in self.escaliers:
            coor.append(escalier.get_coor())
        return coor

    def get_coor_n_portes(self):
        coor = []
        for porte in self.portes:
            coor.append(porte.get_coor())
        return coor

    def get_coor_n_KMs(self):
        coor = []
        for KM in self.KMs:
            coor.append(KM.get_coor())
        return coor

    def get_coor_n_crayon(self):
        coor = []
        for crayon in self.crayons:
            coor.append(crayon.get_coor())
        return coor

    def get_coor_n_pistolets(self):
        coor = []
        for pistolet in self.pistolets:
            coor.append(pistolet.get_coor())
        return coor

    def get_coor_n_voitures(self):
        coor = []
        for voiture in self.voitures:
            coor.append(voiture.get_coor())
        return coor


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

            # Dessiner toutes les voitures à leur position
            for voiture in self.voitures:
                self.screen.blit(voiture.image, voiture.rect.topleft)
            for trottoir in self.trottoirs:
                self.screen.blit(trottoir.image, trottoir.rect.topleft)



            pygame.display.flip()
            self.dt = self.clock.tick(60) / 1000

        pygame.quit()


if __name__ == "__main__":
    game = Game((1380, 800))
    env = Environnement(30, 40, 3, 2, 9, 1, 3, 9, 10)
    game.setup(env)
    game.run()


pygame.quit()
