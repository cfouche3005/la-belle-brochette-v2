import pygame

from game.camera import Camera
from game.env import Env


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
