import pygame

class Env:
    def __init__(self, width : int, height : int, background : str):
        self.screenWidth = width
        self.invisibleWidth = 200
        self.screenHeight = height
        self.width = width*3
        self.height = height
        self.x = 0
        self.y = 0
        self.background_path = background
        self.background = None

        self.loadbackground()

    def loadbackground(self):
        try:
            self.background = pygame.image.load(self.background_path).convert()
            self.background = pygame.transform.scale(self.background, (self.width, self.height))
            print(self.background.get_width(), "x", self.background.get_height())
            self.background.get_rect().move((self.x, self.y))

        except Exception as e:
            print(f"Error loading background: {e}")
    def draw(self, surface):
        surface.blit(self.background, (self.x, self.y))

    def moveRight(self):
        self.x -= 5
        if self.x < -self.width + self.screenWidth:
            self.x = -self.width + self.screenWidth
            return False
        return True
    def moveLeft(self):
        self.x += 5
        if self.x > 0:
            self.x = 0
            return False
        return True

