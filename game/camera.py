import pygame


class Camera:
    def __init__(self, width, height, world_width):
        """
        Initialize the camera
        :param width: The width of the camera
        :param height: The height of the camera
        :param world_width:  The width of the world
        """
        self.width = width
        self.height = height
        self.world_width = world_width
        self.offset_x = 0
        self.offset_y = 0

    def apply(self, entity):
        """
        Adjust the position of the entity based on the camera offset
        :param entity:  The entity to adjust
        :return:
        """
        # Retourne la position ajustée de l'entité pour l'affichage
        return pygame.Rect(
            entity.rect.x + self.offset_x,
            entity.rect.y + self.offset_y,
            entity.rect.width,
            entity.rect.height
        )

    def update(self, target):
        """
        Update the camera position based on the target entity
        :param target: The target entity to follow
        :return:
        """
        # Centre la caméra sur le joueur
        self.offset_x = -target.rect.x + self.width // 2

        # Limites du monde
        if self.offset_x > 0:
            self.offset_x = 0
        if self.offset_x < -(self.world_width - self.width):
            self.offset_x = -(self.world_width - self.width)