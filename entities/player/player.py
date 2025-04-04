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
        tempX = self.rect.x
        if keys[pygame.K_LEFT]:
            tempX-= self.speed
        if keys[pygame.K_RIGHT]:
            tempX += self.speed
        if keys[pygame.K_UP]:
            self.jump()

        # Apply gravity
        self.velocity += self.gravity
        self.rect.y += self.velocity
        # Check for collision with the ground
        if self.rect.y > 500:
            self.rect.y = 500
            self.velocity = 0
        # Check for collision with the ceiling
        if self.rect.y < 0:
            self.rect.y = 0
            self.velocity = 0
        # Check for collision with the left wall

        if tempX < env.invisibleWidth:
            if(env.moveLeft()):
                tempX = self.rect.x
        if tempX< 0:
            tempX = 0
        if tempX + self.width > env.screenWidth-env.invisibleWidth:
            if(env.moveRight()):
                tempX = self.rect.x
        if tempX + self.width > camera.width:
            tempX = camera.width - self.width
        self.rect.x = tempX

    def jump(self):
        if self.rect.y == 500:
            self.velocity = -self.jump_height

    def draw(self, surface):
        surface.blit(self.image, self.rect)
