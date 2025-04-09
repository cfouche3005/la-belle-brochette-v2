import pygame, math

from entities.bullet import Bullet
from game.camera import Camera
from game.env import Env
from environnement.vie import BarreDeVie

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.projectile = []
        self.cooldown = 0

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
        self.on_ground = True

    def shoot(self, angle):
        print("shoot")
        print("angle", angle)
        # Implémentation de la logique de tir
        bullet = Bullet(self.rect.x, self.rect.y, 10, 10, (0,0,0) , angle)
        self.projectile.append(bullet)
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


    def check_trou_collision(self, elements_sol, runtime):
        for element in elements_sol:
            if element.type == "trou":
                rect_trou = pygame.Rect(element.rect.x, element.rect.y, 50, 50)
                if self.rect.colliderect(rect_trou):
                    self.mourir(runtime)
                    return

    def set_game_over_image(self, image):
        self.game_over_image = image

    def afficher_game_over(self, surface):
        if self.game_over_image:
            screen = pygame.display.get_surface()
            screen.blit(self.game_over_image, (150, 150))

    def check_platform_collisions_horizontal(self, env):
        """Vérifie et gère les collisions horizontales avec les plateformes"""
        for platform in env.platforms:  # On suppose que les plateformes sont accessibles via env.game.platforms
            if self.rect.colliderect(platform.rect):
                # Si collision, annuler le mouvement horizontal
                if self.rect.right > platform.rect.left and self.rect.left < platform.rect.left:
                    self.rect.right = platform.rect.left
                elif self.rect.left < platform.rect.right and self.rect.right > platform.rect.right:
                    self.rect.left = platform.rect.right

    def check_platform_collisions_vertical(self, env):
        """Vérifie et gère les collisions verticales avec les plateformes"""
        self.on_ground = False  # Pour savoir si le joueur est sur le sol ou une plateforme

        for platform in env.platforms:  # On suppose que les plateformes sont accessibles via env.game.platforms
            if self.rect.colliderect(platform.rect):
                # Collision par le haut (le joueur est sur la plateforme)
                if self.velocity > 0 and self.rect.bottom > platform.rect.top and self.rect.top < platform.rect.top:
                    self.rect.bottom = platform.rect.top
                    self.velocity = 0
                    self.on_ground = True
                # Collision par le bas (le joueur heurte une plateforme en sautant)
                elif self.velocity < 0 and self.rect.top < platform.rect.bottom and self.rect.bottom > platform.rect.bottom:
                    self.rect.top = platform.rect.bottom
                    self.velocity = 0

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
        if keys[pygame.K_f]:
            if self.cooldown == 0:
                self.shoot(45)
                self.cooldown = 5

        self.check_platform_collisions_horizontal(env)

        # Appliquer la gravité
        self.velocity += self.gravity
        self.rect.y += self.velocity

        self.check_platform_collisions_vertical(env)

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
        if self.cooldown > 0:
            self.cooldown -= 1

    def jump(self):
        if self.rect.y == 500 or self.on_ground:
            self.velocity = -self.jump_height

    def draw(self, surface, camera):
        # Dessin de l'entité avec le décalage de la caméra
        rect_camera = camera.apply(self)
        surface.blit(self.image, rect_camera)
        for bullet in self.projectile:
            bullet.draw(surface, camera)
