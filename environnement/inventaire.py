import pygame

class Inventaire:
    def __init__(self):
        """
        Initialize the player's inventory
        """
        self.pistolet = 1
        self.objets = {
            "chargeur": 0,
            "crayon": 0,
            "km": 0
        }
        self.textures = {
            "chargeur": pygame.transform.scale(pygame.image.load("assets/munition.png"), (30, 30)),
            "crayon": pygame.transform.scale(pygame.image.load("assets/crayon.png"), (30, 30)),
            "km": pygame.transform.scale(pygame.image.load("assets/kit_medical.png"), (30, 30)),
        }

        self.font = pygame.font.SysFont("Arial", 20) # Avec GPT

    def ajouter(self, type_objet):
        """
        Add an object to the inventory
        :param type_objet: The type of object to add (chargeur, crayon, km)
        :return:
        """
        if type_objet in self.objets:
            self.objets[type_objet] += 1

    def retirer(self, type_objet):
        """
        Remove an object from the inventory
        :param type_objet: The type of object to remove (chargeur, crayon, km)
        :return:
        """
        if self.possede(type_objet):
            self.objets[type_objet] -= 1

    def possede(self, type_objet):
        """
        Check if the player possesses a specific object
        :param type_objet: The type of object to check (chargeur, crayon, km)
        :return:
        """
        return type_objet in self.objets and self.objets[type_objet] > 0

    def draw(self, screen):
        """
        Dessiner en haut à droite de l'écran, les différents PU qui sont ramassés par le joueur au cours de la partie
        Aide de GPT pour cette fonction
        :param screen: l'écran sur lequel dessiner l'inventaire
        Aide de GPT pour cette fonction
        """
        screen_width = screen.get_width()
        x, y = screen_width - 150, 10
        for objet, count in self.objets.items():
            screen.blit(self.textures[objet], (x, y))
            txt = self.font.render(f"x{count}", True, (255, 255, 255))
            screen.blit(txt, (x + 35, y + 5))
            y += 40



