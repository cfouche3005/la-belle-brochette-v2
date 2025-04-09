import random

import pygame

from environnement.environnement_jeu import plateformes_fixes, Plateforme, elements_sol_fixes, ElementAuSol
from game.camera import Camera

PLATFORME_TEXTUREPATH = {
    "assets1": "assets/VOITURE2.png",
    "assets2": "assets/GROUND.jpg",
}

ELEMENT_TEXTUREPATH = {
    "porte": "assets/PORTE1.png",
    "escalier": "assets/ESCALIER1.png",
    "trou": "assets/TROU1.png",
    "crayon": "assets/CRAYON_JW.png"

}

class Env:
    def __init__(self, width : int, height : int, background : str, screenInstance : pygame.Surface, camera: Camera):
        self.screenWidth = width
        self.invisibleWidth = 200
        self.screenHeight = height
        self.width = width*3
        self.height = height
        self.x = 0
        self.y = 0
        self.background_path = background
        self.background = None

        self.screen = screenInstance
        self.camera = camera

        #Initialisation des groupes
        self.platforms = pygame.sprite.Group()
        self.element_group = pygame.sprite.Group()


        self.loadbackground()
        self.loadPlatforms()
        self.loadElements()

    def loadbackground(self):
        try:
            self.background = pygame.image.load(self.background_path).convert()
            self.background = pygame.transform.scale(self.background, (self.width, self.height))
            print(self.background.get_width(), "x", self.background.get_height())
            self.background.get_rect().move((self.x, self.y))

        except Exception as e:
            print(f"Error loading background: {e}")

    def loadPlatforms(self):
        for x, y, width, height in plateformes_fixes:
            # Choix aléatoire de la texture parmi les options disponibles
            texture = random.choice(list(PLATFORME_TEXTUREPATH.values()))
            platform = Plateforme(x, y, width, height, texture)
            self.platforms.add(platform)
    def loadElements(self):
        for x, y, type_element in elements_sol_fixes:
            if type_element in ELEMENT_TEXTUREPATH:
                element = ElementAuSol(x, y, 50, 50, ELEMENT_TEXTUREPATH[type_element])
                self.element_group.add(element)
    def draw(self):
        bg_rect = pygame.Rect(self.x + self.camera.offset_x, self.y, self.width, self.height)
        self.screen.blit(self.background, bg_rect)
        for platform in self.platforms:
            self.screen.blit(platform.image, self.camera.apply(platform))
        for element in self.element_group:
            self.screen.blit(element.image, self.camera.apply(element))

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

