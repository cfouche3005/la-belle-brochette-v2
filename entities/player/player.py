import pygame
import math
import os

from pygame.transform import rotate


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        # Image de base (au repos)
        self.original_image = pygame.image.load("assets/frames/fire/fire(body)_0001.png").convert_alpha()
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()

        # Chargement des images de marche
        self.walk_frames = []
        for i in range(1, 5):  # 4 images de marche
            img = pygame.image.load(f"assets/frames/walk/body_000{i}.png").convert_alpha()
            self.walk_frames.append(img)

        # Variables pour l'animation
        self.current_frame = 0
        self.animation_speed = 0.15  # Vitesse de l'animation
        self.animation_timer = 0
        self.is_walking = False

        # Chargement de l'image du bras
        self.arm_image = pygame.transform.rotate(
            pygame.image.load("assets/frames/fire/fire(arm)_0001.png").convert_alpha(), -90)
        self.arm_original = self.arm_image.copy()
        self.arm_rect = self.arm_image.get_rect()

        # Point de fixation du bras sur le corps
        self.pivot = pygame.Vector2(64, 64)  # Point de pivot sur le corps

        # Variable pour suivre l'orientation du joueur (True = droite, False = gauche)
        self.facing_right = True

        self.rect.x = x
        self.rect.y = y
        self.speed = 5
        self.jump_height = 10
        self.gravity = 0.5
        self.velocity = 0
        self.arm_angle = 0

    def update(self):
        # Réinitialisation de l'état de marche
        self.is_walking = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            self.is_walking = True
            # Forcer l'orientation vers la gauche
            if self.facing_right:
                self.facing_right = False
                self.update_player_image()
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            self.is_walking = True
            # Forcer l'orientation vers la droite
            if not self.facing_right:
                self.facing_right = True
                self.update_player_image()
        if keys[pygame.K_UP]:
            self.jump()

        # Gestion de l'animation de marche
        if self.is_walking:
            self.animation_timer += self.animation_speed
            if self.animation_timer >= 1:
                self.animation_timer = 0
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames)
                self.update_player_image()
        else:
            # Retour à l'image de base si on ne marche pas
            if self.image != self.original_image:
                self.image = self.original_image.copy()
                if not self.facing_right:
                    self.image = pygame.transform.flip(self.image, True, False)

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

    def update_player_image(self):
        """Met à jour l'image du joueur en fonction de l'animation et de l'orientation"""
        if self.is_walking:
            self.image = self.walk_frames[self.current_frame].copy()
        else:
            self.image = self.original_image.copy()

        if not self.facing_right:
            self.image = pygame.transform.flip(self.image, True, False)

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
        self.arm_angle = math.degrees(math.atan2(d_pos[0], d_pos[1]))  # Angle en degrés

        # Changer l'orientation du personnage en fonction de l'angle du bras
        should_face_right = -0 <= self.arm_angle <= 180

        # Si l'orientation doit changer, on tourne le personnage
        if should_face_right != self.facing_right:
            self.facing_right = should_face_right
            self.update_player_image()

        # Utiliser l'image du bras originale et l'adapter selon l'orientation
        arm_to_rotate = self.arm_original.copy()

        # Retourner le bras horizontalement si le personnage regarde à gauche
        if not self.facing_right:
            arm_to_rotate = pygame.transform.flip(arm_to_rotate, True, False)

        # Appliquer la rotation au bras selon l'angle calculé
        rotated_arm = pygame.transform.rotate(arm_to_rotate, self.arm_angle)

        # Calculer l'offset après rotation
        origin_rect = self.arm_original.get_rect(center=(pivot_screen_pos[0], pivot_screen_pos[1]))
        rotated_rect = rotated_arm.get_rect()

        # Centrer l'image rotative sur le point de pivot
        rotated_rect.center = origin_rect.center

        # Mise à jour de l'image et du rectangle du bras
        self.arm_image = rotated_arm
        self.arm_rect = rotated_rect

    def draw(self, surface):
        # Dessiner le corps du joueur
        surface.blit(self.image, self.rect)

        # Dessiner le bras pivoté
        surface.blit(self.arm_image, self.arm_rect)