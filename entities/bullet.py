import math

import pygame

from game.env import Env


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color=(0, 0, 255), angle=0, env: Env = None, Callback=None, speed = 100):
        """
        Initialize the bullet object
        :param x: Origin x position of the bullet
        :param y: Origin y position of the bullet
        :param width: Width of the bullet
        :param height: Height of the bullet
        :param color: Color of the bullet
        :param angle: Angle of the bullet in degrees
        :param env: The environment where the bullet is created
        :param Callback: Function to call when the bullet collides with a platform or an enemy
        :param speed: Speed of the bullet
        """
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.angle = angle
        self.env = env
        self.callback = Callback
    def draw(self, surface, camera):
        """
        Draw the bullet on the screen
        :param surface: The surface to draw the bullet on
        :param camera: The camera used to manage the view
        :return:
        """
        self.move()
        rect_camera = camera.apply(self)
        surface.blit(self.image, rect_camera)

    def move(self):
        """
        Calculate a new position for the bullet based on its angle and speed.
        """
        radians = math.radians(self.angle)
        self.rect.x += self.speed * math.cos(radians)
        self.rect.y -= self.speed * math.sin(radians)
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
        print(self.env.screenWidth)
        if self.rect.x > self.env.width or self.rect.x < 0 or self.rect.y > self.env.height or self.rect.y < 0:
            return True
        return False

