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

    def draw(self, surface, camera):
        rect_camera = camera.apply(self)
        surface.blit(self.image, rect_camera)