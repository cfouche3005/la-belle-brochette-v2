import math

import pygame


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color=(0, 0, 255), angle=0):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.height = height
        self.angle = angle

    def draw(self, surface, camera):
        self.move()
        rect_camera = camera.apply(self)
        surface.blit(self.image, rect_camera)

    def move(self):
        """
        Calculate a new position for the bullet based on its angle and speed.
        """
        speed = 100
        radians = math.radians(self.angle)
        self.rect.x += speed * math.cos(radians)
        self.rect.y -= speed * math.sin(radians)

