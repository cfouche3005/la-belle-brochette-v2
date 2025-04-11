import pygame

class BarreDeVie:
    def __init__(self, max_vies=5, game_over_cb=None):
        self.vies = max_vies
        self.max_vies = max_vies
        self.x = 20
        self.y = 20
        self.coeur_image = pygame.image.load("assets/COEUR_PA.png").convert_alpha()
        self.coeur_image = pygame.transform.scale(self.coeur_image, (50, 50))
        print("Game over callback:", game_over_cb)
        self.gameOverCB = game_over_cb

    def perdre_vie(self, damage):
        """
        dès que le personnage reçoit des dégats soit d'une chute ou bien d'une arme il perd des vies
        """
        self.vies -= damage
        if self.vies < 0:
            self.vies = 0
            if self.gameOverCB:
                print("Game Over")
                self.gameOverCB()

    def draw(self, screen):
        for i in range(self.vies):
            screen.blit(self.coeur_image, (self.x + i * 45, self.y))
