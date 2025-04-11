import pygame

class BarreDeVie:
    def __init__(self, max_vies=5, game_over_cb=None):
        """
        Life bar class to manage the player's life in the game.
        :param max_vies: Maximum number of lives the player can have.
        :param game_over_cb: Callback function to be called when the player runs out of lives.
        """
        self.vies = max_vies
        self.max_vies = max_vies
        self.x = 20
        self.y = 20
        self.coeur_image = pygame.image.load("assets/COEUR_PA.png").convert_alpha()
        self.coeur_image = pygame.transform.scale(self.coeur_image, (50, 50))
        self.gameOverCB = game_over_cb

    def perdre_vie(self, damage):
        """
        dès que le personnage reçoit des dégats soit d'une chute ou bien d'une arme il perd des vies
        """
        self.vies -= damage
        if self.vies < 0:
            self.vies = 0
            if self.gameOverCB:
                self.gameOverCB()

    def draw(self, screen):
        """
        Dessiner la barre de vie du personnage en haut à gauche
        :param screen:  The screen where the life bar will be drawn.
        """
        for i in range(self.vies):
            screen.blit(self.coeur_image, (self.x + i * 45, self.y))
