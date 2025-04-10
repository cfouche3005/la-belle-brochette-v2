import math

import pygame

from game.env import Env


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color=(0, 0, 255), angle=0, env: Env = None, Callback=None):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.height = height
        self.angle = angle
        self.env = env
        self.callback = Callback
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
        # Check if the bullet is coliding with any platforms
        if self.env:
            for platform in self.env.platforms:
                # Check for collision with the platform
                if self.rect.colliderect(platform.rect) or self.checkIfOutOfScreen():
                    print("Collision with platform detected or out of screen")
                    # Handle collision with the platform
                    self.callback()
                    break
            if self.env.checkCollisionWithEnnemy(self.rect):
                print("Collision with ennemy detected")
                # Handle collision with the ennemy
                self.callback()
    def checkIfOutOfScreen(self):
        """
        Check if the bullet is out of the screen
        :return: True if the bullet is out of the screen, False otherwise
        """
        if self.rect.x > self.env.screenWidth or self.rect.x < 0 or self.rect.y > self.env.screenHeight or self.rect.y < 0:
            return True
        return False

