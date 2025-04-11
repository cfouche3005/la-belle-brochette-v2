import math

import pygame
import random


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, width=30, height=30, screen=None, camera=None):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((0, 0, 255))  # Carré bleu
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y - height  # Position sur la plateforme
        self.width = width
        self.height = height
        self.speed = 2
        self.direction = -1  # -1 pour gauche, 1 pour droite
        self.current_platform = None
        self.falling = False
        self.screen = screen
        self.camera = camera
        self.projectiles = []
        self.detection_radius = 300  # Distance de détection du joueur
        self.cooldown = 0
        self.cooldown_max = 60

    def update(self, platforms, player=None, env=None):
        # Trouver la plateforme actuelle
        self.current_platform = self.get_current_platform(platforms)

        # Si aucune plateforme actuelle, appliquer la gravité
        if not self.current_platform:
            self.falling = True
            self.rect.y += 5  # Chute
            return  # Ne pas continuer si en chute
        else:
            self.falling = False
            # Aligner avec le haut de la plateforme
            self.rect.bottom = self.current_platform.rect.top

            # Vérifier la plateforme suivante
            next_platform = self.check_adjacent_platform(platforms)

            # Si bord de plateforme ou escalier, changer de direction
            if next_platform is None:
                self.direction *= -1

            # Déplacement horizontal
            self.rect.x += self.speed * self.direction

        if player and env and not self.falling:
            # Décrémentation du cooldown
            if self.cooldown > 0:
                self.cooldown -= 1

            # Détection du joueur
            if self.player_in_range(player) and self.cooldown == 0:
                self.shoot(player, env)
                self.cooldown = self.cooldown_max

        # Mise à jour des projectiles
        for projectile in self.projectiles[:]:
            if projectile in self.projectiles:  # Vérification pour éviter les erreurs
                if player and projectile.rect.colliderect(player.hitbox):
                    player.vie.perdre_vie(1)
                    self.delete_projectile(projectile)

    def player_in_range(self, player):
        """Vérifie si le joueur est à portée de tir"""
        distance_x = self.rect.centerx - player.hitbox.centerx
        distance_y = self.rect.centery - player.hitbox.centery
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)
        return distance <= self.detection_radius

    def shoot(self, player, env):
        """Tire une balle en direction du joueur"""
        # Calcul de l'angle vers le joueur

        from entities.bullet import Bullet
        dx = player.hitbox.centerx - self.rect.centerx
        dy = player.hitbox.centery - self.rect.centery
        angle = math.degrees(math.atan2(-dy, dx))  # Angle en degrés

        # Création de la balle (rouge pour l'ennemi)
        bullet = Bullet(
            self.rect.centerx,
            self.rect.centery,
            8, 8,
            (255, 0, 0),  # Rouge pour les balles ennemies
            angle,
            env,
            lambda: self.delete_projectile(bullet),
            50
        )
        self.projectiles.append(bullet)

    def delete_projectile(self, projectile):
        """Supprime un projectile de la liste"""
        if projectile in self.projectiles:
            self.projectiles.remove(projectile)
            projectile.kill()
    def get_current_platform(self, platforms):
        """Déterminer sur quelle plateforme se trouve l'ennemi"""
        for platform in platforms:
            # Utiliser une tolérance verticale de quelques pixels
            if (abs(self.rect.bottom - platform.rect.top) <= 5 and
                    self.rect.right > platform.rect.left and
                    self.rect.left < platform.rect.right):
                return platform
        return None

    def check_adjacent_platform(self, platforms):
        """Vérifie s'il existe une plateforme adjacente dans la direction actuelle"""
        if not self.current_platform:
            return None

        # Distance de vérification plus grande
        check_distance = 5

        if self.direction > 0:  # Vers la droite
            check_x = self.rect.right + check_distance
            # Vérifier si on atteint le bord de la plateforme actuelle
            if check_x > self.current_platform.rect.right:
                # Point de vérification en dessous du niveau
                check_y = self.rect.bottom + 5

                # Chercher une plateforme à ce niveau
                for platform in platforms:
                    if (platform != self.current_platform and
                            platform.rect.left <= check_x <= platform.rect.right and
                            abs(platform.rect.top - check_y) <= 10):

                        # Éviter les escaliers
                        if hasattr(platform, 'type') and platform.type == "escalier":
                            return None

                        return platform
                return None  # Pas de plateforme trouvée
        else:  # Vers la gauche (même logique)
            check_x = self.rect.left - check_distance
            if check_x < self.current_platform.rect.left:
                check_y = self.rect.bottom + 5

                for platform in platforms:
                    if (platform != self.current_platform and
                            platform.rect.left <= check_x <= platform.rect.right and
                            abs(platform.rect.top - check_y) <= 10):

                        if hasattr(platform, 'type') and platform.type == "escalier":
                            return None

                        return platform
                return None

        return self.current_platform  # L'ennemi est toujours sur la même plateforme

    def draw(self):
        rect_camera = self.camera.apply(self)
        self.screen.blit(self.image, rect_camera)
        for projectile in self.projectiles:
            projectile.draw(self.screen, self.camera)