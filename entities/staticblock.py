import time

import pygame


class StaticBlock(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color=(0, 0, 255)):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.height = height

    def draw(self, surface, camera):
        rect_camera = camera.apply(self)
        surface.blit(self.image, rect_camera)

    def moveLeft(self):
        self.rect.x -= 100
        if self.rect.x < 0:
            self.rect.x = 0
            return False
        return True