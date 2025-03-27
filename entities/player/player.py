import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((255, 44, 102))
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y
        self.speed = 5
        self.jump_height = 10
        self.gravity = 0.5
        self.velocity = 0

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

    def jump(self):
        if self.rect.y == 500:
            self.velocity = -self.jump_height

    def draw(self, surface):
        surface.blit(self.image, self.rect)
