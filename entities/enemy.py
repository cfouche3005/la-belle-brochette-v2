import pygame
import random


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, width=30, height=30):
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

    def update(self, platforms):
        # Sauvegarde de la position précédente
        old_x = self.rect.x

        # Déplacement horizontal
        self.rect.x += self.speed * self.direction

        # Vérifier si l'ennemi est sur une plateforme
        on_platform = False
        for platform in platforms:
            # Vérifier si l'ennemi est sur cette plateforme
            if (self.rect.bottom == platform.rect.top and
                    self.rect.right > platform.rect.left and
                    self.rect.left < platform.rect.right):
                on_platform = True
                self.current_platform = platform
                break

        # Si aucune plateforme n'est trouvée sous l'ennemi
        if not on_platform:
            # Vérifier s'il y a une plateforme adjacente
            next_platform = self.check_adjacent_platform(platforms)
            if next_platform:
                # Continuer sur la plateforme adjacente
                self.current_platform = next_platform
            else:
                # Inverser la direction s'il n'y a pas de plateforme adjacente
                self.direction *= -1
                self.rect.x = old_x

    def check_adjacent_platform(self, platforms):
        """Vérifie s'il existe une plateforme adjacente dans la direction actuelle"""
        if not self.current_platform:
            return None

        # Définir les coordonnées pour la recherche de plateforme adjacente
        if self.direction > 0:  # Vers la droite
            check_x = self.rect.right + 2
        else:  # Vers la gauche
            check_x = self.rect.left - 2

        # Point de vérification (au niveau des pieds de l'ennemi)
        check_y = self.rect.bottom - 1

        # Chercher une plateforme qui contient ce point
        for platform in platforms:
            if (platform != self.current_platform and
                    platform.rect.left <= check_x <= platform.rect.right and
                    platform.rect.top - 5 <= check_y <= platform.rect.top + 5):
                return platform

        return None

    def draw(self, surface, camera):
        rect_camera = camera.apply(self)
        surface.blit(self.image, rect_camera)