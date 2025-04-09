import pygame
import math

from pygame.transform import rotate


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.image.load("assets/frames/fire/fire(body)_0001.png").convert_alpha()
        self.rect = self.image.get_rect()


        # Chargement de l'image du bras
        self.arm_image = pygame.transform.rotate(pygame.image.load("assets/frames/fire/fire(arm)_0001.png").convert_alpha(), -90)
        self.arm_original = self.arm_image.copy()
        self.arm_rect = self.arm_image.get_rect()

        # Point de fixation du bras sur le corps (à ajuster selon votre sprite)
        self.pivot = pygame.Vector2(64, 64)  # Point de pivot sur le corps (coordonnées relatives à l'image du corps)

        self.rect.x = x
        self.rect.y = y
        self.speed = 5
        self.jump_height = 10
        self.gravity = 0.5
        self.velocity = 0
        self.arm_angle = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
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

        # Mise à jour de l'angle du bras en fonction de la position de la souris
        self.update_arm_angle()

    def jump(self):
        if self.rect.y == 500:
            self.velocity = -self.jump_height

    def update_arm_angle(self):
        # Obtenir la position de la souris
        mouse_pos = pygame.mouse.get_pos()

        # Calculer la position du point de pivot dans les coordonnées de l'écran
        pivot_screen_pos = (self.rect.x + self.pivot[0], self.rect.y + self.pivot[1])

        # Calculer l'angle entre le point de pivot et la position de la souris
        d_pos = pygame.Vector2(mouse_pos[0] - pivot_screen_pos[0], mouse_pos[1] - pivot_screen_pos[1])
        self.arm_angle = math.degrees(math.atan2(d_pos[0],d_pos[1]))  # Angle en degrés

        rotated_arm = pygame.transform.rotate(self.arm_original, self.arm_angle)

        # Calculer l'offset après rotation
        origin_rect = self.arm_original.get_rect(center=(pivot_screen_pos[0] ,
                                                          pivot_screen_pos[1]))
        rotated_rect = rotated_arm.get_rect()

        # Centrer l'image rotative sur le point de pivot
        rotated_rect.center = origin_rect.center

        # Ajuster le sprite du bras pour qu'il soit positionné correctement


        # Mise à jour de l'image et du rectangle du bras
        self.arm_image = rotated_arm
        self.arm_rect = rotated_rect


    def draw(self, surface):
        # Dessiner le corps du joueur
        surface.blit(self.image, self.rect)

        # Dessiner le bras pivoté (déjà positionné dans update_arm_angle)
        surface.blit(self.arm_image, self.arm_rect)