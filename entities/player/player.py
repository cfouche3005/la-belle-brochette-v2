import pygame, math

from game.camera import Camera
from game.env import Env
from environnement.vie import BarreDeVie
from environnement.environnement_jeu import Plateforme,Porte, ElementAuSol
from environnement.inventaire import Inventaire

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((255, 44, 102))
        self.rect = self.image.get_rect()
        self.width = width
        self.height = height
        self.rect.x = x
        self.rect.y = y
        self.speed = 5
        self.jump_height = 10
        self.gravity = 0.5
        self.velocity = 0
        self.vie = BarreDeVie(3)
        self.platforms_invisibles = []
        self.inventaire = Inventaire()
        self.coeur_image =  pygame.transform.scale(pygame.image.load("assets/COEUR_PA.png"), (50, 50))
        self.hearts =[]

    #aide de GPT pour le l'utilisation de ".type", mais aussi pour les fonctions monter_escalier pour la plateforme invisible
    # et ouvrir_porte pour le "if isinstance(element, ElementAuSol):"
    def ramasser_chargeur(self, power_ups, distance_threshold=50):
        """
        Fonction pour ramasser le power-up chargeur si le joueur est à une certaine distance.
        Si un PU est ramassé, il est supprimé de la liste des power-ups.
        """
        for pu in power_ups:
            if pu.type == "chargeur":
                distance_x = self.rect.centerx - pu.rect.centerx
                distance_y = self.rect.centery - pu.rect.centery
                distance = math.sqrt(distance_x ** 2 + distance_y ** 2)
                if distance <= distance_threshold:
                    power_ups.remove(pu)
                    self.inventaire.ajouter("chargeur")
                    return

    def ramasser_km(self, power_ups, distance_threshold=50):
        """
        Fonction pour ramasser le power-up KM si le joueur est à une certaine distance.
        Si un PU est ramassé, il est supprimé de la liste des power-ups.
        """
        for pu in power_ups:
            if pu.type == "km":
                distance_x = self.rect.centerx - pu.rect.centerx
                distance_y = self.rect.centery - pu.rect.centery
                distance = math.sqrt(distance_x ** 2 + distance_y ** 2)
                if distance <= distance_threshold:
                    power_ups.remove(pu)
                    self.inventaire.ajouter("km")
                    return

    def ramasser_crayon(self, elements_sol, distance_threshold=50):
        """
        Fonction pour ramasser le crayon si le joueur est à une certaine distance.
        Si un crayon est ramassé, il est supprimé de la liste des éléments au sol.
        """
        for element in elements_sol:
            if element.type == "crayon":
                distance_x = self.rect.centerx - element.rect.centerx
                distance_y = self.rect.centery - element.rect.centery
                distance = math.sqrt(distance_x ** 2 + distance_y ** 2)
                if distance <= distance_threshold:
                    print("Crayon ramassé !")
                    elements_sol.remove(element)
                    self.inventaire.ajouter("crayon")
                    return

    def monter_escaliers(self, elements_sol, distance_threshold=50):
        """
        Permet au joueur de monter les escaliers s'il est à une certaine distance d'un escalier
        et appuie sur la touche Q.
        """
        for element in elements_sol:
            if element.type == "escalier":
                distance_x = self.rect.centerx - element.rect.centerx
                distance_y = self.rect.centery - element.rect.centery
                distance = math.sqrt(distance_x ** 2 + distance_y ** 2)
                if distance <= distance_threshold:
                    plateforme = Plateforme(element.rect.x + 45, 450, element.rect.width, 10, "assets/GROUND.jpg")
                    self.platforms_invisibles.append(plateforme)
                    return
        self.platform_invisible = None

    def ouvrir_portes(self, elements_sol_fixes, distance_threshold=50):
        """
        Permet au joueur d'ouvrir une portee s'il est à une certaine distance de cette dernière
        et pour l'ouvrir il appuie sur la touche E
        """
        for element in elements_sol_fixes:
            if isinstance(element, ElementAuSol):
                if element.type == "porte":
                    distance_x = self.rect.centerx - element.rect.centerx
                    distance_y = self.rect.centery - element.rect.centery
                    distance = math.sqrt(distance_x ** 2 + distance_y ** 2)
                    if distance <= distance_threshold:
                        element.ouvrir()
                        break #utilisation de break pour sortir de la boucle

    def check_trou_collision(self, elements_sol, runtime):
        """
        Permet au joueur d'éviter dans des trous. S'il tombe dedans il meurt instantanément.
        Pour éviter les trous il doit sauter ou aller sur des plateformes
        """
        for x, y, type_element in elements_sol:
            if type_element == "trou":
                rect_trou = pygame.Rect(x, y, 50, 50)
                if self.rect.colliderect(rect_trou):
                    self.mourir(runtime)

    def set_game_over_image(self, image):
        self.game_over_image = image

    def afficher_game_over(self):
        """
        Affiche à l'écran gameover si le joueur est tombé dans un trou
                """
        if self.game_over_image:
            screen = pygame.display.get_surface()
            screen.blit(self.game_over_image, (150, 150))

    def gagner_vie(self):
        if len(self.hearts) < self.vie.vies:
            self.hearts.append(self.coeur_image)

    def mourir(self, runtime):
        """
        Fait mourir le joueur et réinitialise sa barre de vie à 0
        """
        self.vie.vies = 0
        runtime.changeGameState("gameover")

    def update(self, env: Env, camera: Camera):
        keys = pygame.key.get_pressed()

        # Déplacement du joueur dans le monde
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.jump()

        # Appliquer la gravité
        self.velocity += self.gravity
        self.rect.y += self.velocity

        # Ajout d'une plateforme invisible pour permettre au joueur de rester en haut d'un escalier.
        # Lorsqu'il est au sommet de l'escalier, cette plateforme invisible lui permet de marcher ou sauter
        # vers d'autres plateformes sans tomber immédiatement, en le maintenant à une hauteur stable.
        for plateforme in self.platforms_invisibles:
            if self.rect.colliderect(plateforme.rect):
                self.rect.y = plateforme.rect.top
                self.velocity = 0

        # Collisions avec les limites
        if self.rect.y > 500:
            self.rect.y = 500
            self.velocity = 0
        if self.rect.y < 0:
            self.rect.y = 0
            self.velocity = 0
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > env.width - self.width:
            self.rect.x = env.width - self.width

        # Mise à jour de la caméra
        camera.update(self)

    def jump(self):
        if self.rect.y == 500 or self.rect.y == 450:
            # ici 450 fait référence au sommet des escaliers, c'est-à-dire où se situe la plateforme invisible
            self.velocity = -self.jump_height

    def draw(self, surface, camera):
        """
        Ajouter de la vie au personnage s'il a un kit dans son inventaire.
        Reprise de l'affichage des vies utilisé dans la classe BarreDeVie
        Les vies seront ajoutées aux endroits où il y a un vide (aide de GPT pour ceci)
        """
        # Dessin de l'entité avec le décalage de la caméra
        rect_camera = camera.apply(self)
        surface.blit(self.image, rect_camera)

        x_offset = 20
        y_offset = 20
        for i in range(5):
            if i < self.vie.vies:
                surface.blit(self.coeur_image, (x_offset + i * 45, y_offset))
            else:
                empty_heart = pygame.Surface((30, 30), pygame.SRCALPHA) #"couleur transparente"
                surface.blit(empty_heart, (x_offset + i * 45, y_offset))  # Afficher le coeur vide avec la couleur invisible
