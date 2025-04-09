import pygame, math

from game.camera import Camera
from game.env import Env
from environnement.vie import BarreDeVie

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
        self.vie = BarreDeVie(5)

    def ramasser_pistolet(self, power_ups, distance_threshold=50):
        """
        Fonction pour ramasser le power-up pistolet si le joueur est à une certaine distance.
        Si un PU est ramassé, il est supprimé de la liste des power-ups.
        """
        for pu in power_ups:
            if pu.type == "pistolet":
                distance_x = self.rect.centerx - pu.rect.centerx
                distance_y = self.rect.centery - pu.rect.centery
                distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

                if distance <= distance_threshold:
                    power_ups.remove(pu)
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
                    return

    def monter_escaliers(self, elements_sol, runtime):
        for x, y, type_element in elements_sol:
            # On ne vérifie que les "escaliers"
                if type_element == "escalier":
                    rect_escalier = pygame.Rect(x, y, 50, 50)
                    if self.rect.colliderect(rect_escalier):
                        self.rect.y += 10

    def ouvrir_portes(self, elements_sol):
        for x, y, type_element in elements_sol:
            if type_element == "porte":
                if self.etat == 'fermée':
                    print("porte fermée")
                    self.player.changer_etat_porte(elements_sol)
                    print("porte ouverte")

    def jump_plateformes(self, plateformes_fixes, sol_y = 475):

        plateformes_touchées = pygame.sprite.spritecollide(self, plateformes_fixes, False)

        if plateformes_touchées:
            plateforme = plateformes_touchées[0]
            self.rect.bottom = plateforme.rect.top
            self.rect.centerx = plateforme.rect.centerx
        else:
            # Pas de plateforme touchée, tomber sur le sol
            self.rect.bottom = sol_y

    def chute_plateformes (self):
        if self.chute == 100:
            self.vie.vies -= 1
        elif self.chute == 200:
            self.vie.vies -=2
        elif self.chute == 300:
            self.vie.vies -= 3

    def check_trou_collision(self, elements_sol, runtime):
        for x, y, type_element in elements_sol:
            # On ne vérifie que les "trous"
            if type_element == "trou":
                rect_trou = pygame.Rect(x, y, 50, 50)
                if self.rect.colliderect(rect_trou):
                    self.mourir(runtime)

    def set_game_over_image(self, image):
        self.game_over_image = image

    def afficher_game_over(self, surface):
        if self.game_over_image:
            screen = pygame.display.get_surface()
            screen.blit(self.game_over_image, (150, 150))

    def mourir(self, runtime):
        """
        Fait mourir le joueur, réinitialise sa barre de vie à 0 et affiche un message.
        """
        self.vie.vies = 0  # Réinitialise la barre de vie du joueur à 0
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
        if self.rect.y == 500:
            self.velocity = -self.jump_height

    def draw(self, surface, camera):
        # Dessin de l'entité avec le décalage de la caméra
        rect_camera = camera.apply(self)
        surface.blit(self.image, rect_camera)
