import pygame


class Camera:
    def __init__(self, width, height, world_width):
        self.width = width
        self.height = height
        self.world_width = world_width
        self.offset_x = 0
        self.offset_y = 0

    def apply(self, entity):
        # Retourne la position ajustée de l'entité pour l'affichage
        return pygame.Rect(
            entity.rect.x + self.offset_x,
            entity.rect.y + self.offset_y,
            entity.rect.width,
            entity.rect.height
        )

    def update(self, target):
        # Centre la caméra sur le joueur
        self.offset_x = -target.rect.x + self.width // 2

        # Limites du monde
        if self.offset_x > 0:
            self.offset_x = 0
        if self.offset_x < -(self.world_width - self.width):
            self.offset_x = -(self.world_width - self.width)