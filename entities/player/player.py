import pygame, math
from game.camera import Camera
from game.env import Env
from environnement.vie import BarreDeVie

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
        self.vie = BarreDeVie(5)

    def ramasser_pu(self, power_ups, distance_threshold=50):
        for power_up in list(power_ups):
            distance_x = self.rect.centerx - power_up.rect.centerx
            distance_y = self.rect.centery - power_up.rect.centery
            distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

            print(f"Distance entre le joueur et le PU: {distance}")

            if distance <= distance_threshold:
                print(f"PU ramassé ! Distance: {distance}")
                power_ups.remove(power_up)  # Retirer le power-up du groupe
                return  # Sortir après avoir ramassé le power-up
        print("Aucun PU ramassé")  # Si aucun power-up n'est à proximité

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
