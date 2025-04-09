import random
import pygame
import pygame as pg
from pygame.sprite import Sprite

class Plateforme:
    def __init__(self, coor, width, height):
        self.coordonnees = coor
        self.rect = pygame.Rect(coor[0], coor[1], 50, 50)  # On crée un rect basé sur coordonnees
        self.image = pygame.Surface((50, 50))  # Surface vide par défaut
        self.image.fill((200, 200, 200))

    def get_coor(self):
        return self.coordonnees

    def deplacement_plateforme(self):
        x1 = self.coordonnees[0]
        x2 = random.randint(-1, 1)
        y1 = self.coordonnees[1]
        y2 = random.randint(-1, 1)
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
        Plateforme.__init__(self, coor, width, height)
        self.image = pygame.image.load("C:/Users/audem/Downloads/VOITURE.jpg")
        # Redimensionner l'image  AVEC GPT
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()  # Recréer le rect avec la nouvelle taille de l'image
        self.rect.topleft = (x, y)

    def get_coor(self):
        return self.rect.topleft

class Trottoir(Plateforme, pygame.sprite.Sprite):
    def __init__(self, coor, x, y, width, height):
        Plateforme.__init__(self, coor, width, height)
        self.image = pygame.image.load("C:/Users/audem/Downloads/TROTTOIR.jpg")
        # Redimensionner l'image  AVEC GPT
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()  # Recréer le rect avec la nouvelle taille de l'image
        self.rect.topleft = (x, y)

    def get_coor(self):
        return self.rect.topleft


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

class Trous(Elt_Sol, pygame.sprite.Sprite):
    def __init__(self, coor, x, y):
        Elt_Sol.__init__(self, coor)
        self.image = pygame.image.load("C:/Users/audem/Downloads/trou.jpg")
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

        if self.image is None:
            print("Erreur : L'image du pistolet n'a pas pu être chargée.")

class Crayon(PU, pygame.sprite.Sprite):
    def __init__(self, trottoirs, voitures, sol):
        PU.__init__(self, trottoirs, voitures, sol)
        self.image = pygame.image.load("C:/Users/audem/Downloads/CRAYON.jpg")
        self.image = pygame.transform.scale(self.image, (50, 50))  # Redimensionner
        self.rect.topleft = self.coordonnees

        if self.image is None:
            print("Erreur : L'image du Crayon n'a pas pu être chargée.")

class Kit_Med(PU, pygame.sprite.Sprite):
    def __init__(self, trottoirs, voitures, sol):
        PU.__init__(self, trottoirs, voitures, sol)
        self.image = pygame.image.load("C:/Users/audem/Downloads/MK.jpg")
        self.image = pygame.transform.scale(self.image, (50, 50))  # Redimensionner
        self.rect.topleft = self.coordonnees

        if self.image is None:
            print("Erreur : L'image du KM n'a pas pu être chargée.")
class Environnement:
    def __init__(self, width, height, n_escaliers, n_portes, n_pistolets, n_crayon, n_KMs, n_voitures, n_trottoirs, n_trous):
        self.width = width
        self.height = height
        self.voitures = []
        self.escaliers = []
        self.portes = []
        self.trottoirs = []
        self.KMs = []
        self.pistolets = []
        self.crayon = []
        self.trous = []

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
        for d in range(n_trous):
            x = (random.randint(0, width - 50))
            y = height - 50
            coor = (x, y)
            self.trous.append(Trous(coor, x, y))

        for e in range(n_crayon):
            self.crayon.append(Crayon(self.trottoirs, self.voitures,self.height))

        for f in range(n_KMs):
            self.KMs.append(Kit_Med(self.trottoirs, self.voitures, self.height))

        for g in range(n_pistolets):
            self.pistolets.append(Pistolet(self.trottoirs,self.voitures, self.height))


class Game:
    def __init__(self, window_size):
        pygame.init()
        self.screen = pygame.display.set_mode(window_size)
        self.clock = pygame.time.Clock()
        self.dt = 0
        self.isRunning = True
        self.offset_x = 0  # Décalage de l'écran
        self.plateformes = []  # Liste des plateformes générées
        self.PUs = []  # Liste des power-ups (PU) générés
        self.apparitions_PUs_Plateformes = 120  # Intervalle entre les apparitions (toutes les 120 itérations)
        self.width, self.height = window_size  # Récupérer la taille de la fenêtre

        self.voitures = []
        self.escaliers = []
        self.portes = []
        self.trottoirs = []
        self.KMs = []
        self.pistolets = []
        self.crayon = []
        self.trous = []

    def setup(self, env):
        self.voitures = env.voitures
        self.escaliers = env.escaliers
        self.portes = env.portes
        self.trottoirs = env.trottoirs
        self.KMs = env.KMs
        self.pistolets = env.pistolets
        self.crayon = env.crayon
        self.trous = env.trous

    def apparitions_plateformes(self):
        # Générer une plateforme à une position y aléatoire et à droite de l'écran
        y_pos = random.randint(300, 600)  # Position aléatoire entre 300 et 600
        platform = Plateforme((self.screen.get_width(), y_pos), self.width,
                              self.height)  # Passer la taille de la fenêtre
        self.plateformes.append(platform)

    def apparitions_PUs(self):
        # Générer un power-up (PU) à une position y aléatoire et à droite de l'écran
        y_pos = random.randint(200, 600)  # Position aléatoire entre 200 et 600
        pu = PU(self.trottoirs, self.voitures, self.screen.get_height())  # On crée un power-up
        self.PUs.append(pu)

    def run(self):
        background = pygame.image.load("C:/Users/audem/Downloads/fond.png")
        bg_width, bg_height = background.get_size()

        self.screen.fill((0, 0, 255))  # Remplir l'écran avec du bleu

        compteur = 0  # Compteur pour gérer les apparitions des objets

        while self.isRunning:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.isRunning = False

            # Déplacer l'écran vers la droite
            self.offset_x += 5  # Vitesse du déplacement vers la droite

            # Réinitialiser l'offset lorsque l'arrière-plan est hors de l'écran (pour créer un effet de boucle)
            if self.offset_x >= self.width:
                self.offset_x = 0

            # Générer des plateformes et des power-ups à intervalles réguliers (toutes les 120 itérations)
            if compteur % self.apparitions_PUs_Plateformes == 0:
                if random.random() < 0.5:  # 50% de chances de générer une plateforme
                    self.apparitions_plateformes()
                else:  # Sinon, générer un power-up
                    self.apparitions_PUs()

            # Déplacer les plateformes vers la gauche
            for platform in self.plateformes:
                platform.deplacement_plateforme()  # Déplacer la plateforme
                self.screen.blit(platform.image, platform.rect.topleft)  # Dessiner la plateforme
                # Supprimer la plateforme si elle sort de l'écran
                if platform.rect.right < 0:
                    self.plateformes.remove(platform)

            # Déplacer les power-ups vers la gauche
            for pu in self.PUs:
                pu.coordonnees = (pu.coordonnees[0] - 5, pu.coordonnees[1])  # Déplacement du PU
                if pu.image is not None:
                    self.screen.blit(pu.image, pu.rect.topleft)  # Dessiner le power-up
                # Supprimer le PU s'il sort de l'écran
                if pu.rect.right < 0:
                    self.PUs.remove(pu)

            pygame.display.flip()
            self.dt = self.clock.tick(60) / 1000
            compteur += 1
if __name__ == "__main__":
    game = Game((1580, 800))
    env = Environnement(1580, 800, 10, 10, 10, 1, 10, 20, 10, 3)
    game.setup(env)
    game.run()
