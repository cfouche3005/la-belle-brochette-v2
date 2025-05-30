import random

import pygame

from environnement.environnement_jeu import plateformes_fixes, Plateforme, elements_sol_fixes, ElementAuSol, Chargeur, \
    Kit_Med, positions_powerups
from game.camera import Camera
from entities.enemy import Enemy

PLATFORME_TEXTUREPATH = {
    "assets2": "assets/GROUND.jpg",
}

ELEMENT_TEXTUREPATH = {
    "porte": "assets/porte_noire.png",
    "escalier": "assets/escalier_urbain.png",
    "trou": "assets/trou_sol.png",
    "crayon": "assets/crayon.png"

}

class Env:
    def __init__(self, width : int, height : int, background : str, screenInstance : pygame.Surface, camera: Camera):
        """
        Initialize the game environment
        :param width: The width of the environment
        :param height: The height of the environment
        :param background: Path to the background image
        :param screenInstance: The screen instance where the environment will be drawn
        :param camera: The camera instance used to manage the view
        """
        self.screenWidth = width
        self.invisibleWidth = 200
        self.screenHeight = height
        self.width = width*2
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

        self.enemies = pygame.sprite.Group()

        self.power_group = pygame.sprite.Group()

        self.power_ups = pygame.sprite.Group()

        self.loadbackground()
        self.loadPlatforms()
        self.loadElements()
        self.loadPowerUps()
        self.spawnEnemies(5)

    def spawnEnemies(self, count: int):
        """
        Spawn enemies on the platforms
        :param count: Number of enemies to spawn
        :return:
        """
        valid_platforms = [p for p in self.platforms if p.type != "escalier"]
        if not valid_platforms:
            return

        for _ in range(count):
            platform = random.choice(valid_platforms)
            x = random.randint(platform.rect.left, platform.rect.right - 30)
            y = platform.rect.top

            enemy = Enemy(x, y, 30, 30, self.screen, self.camera)
            enemy.current_platform = platform
            self.enemies.add(enemy)
    def loadbackground(self):
        """
        Load the background image and scale it to fit the environment
        :return:
        """
        try:
            self.background = pygame.image.load(self.background_path).convert()
            self.background = pygame.transform.scale(self.background, (self.width, self.height))
            print(self.background.get_width(), "x", self.background.get_height())
            self.background.get_rect().move((self.x, self.y))

        except Exception as e:
            print(f"Error loading background: {e}")

    def loadPlatforms(self):
        """
        Load the platforms in the environment
        :return:
        """
        for x, y, width, height, platform_type in plateformes_fixes:
            texture = None
            if platform_type == "escalier":
                print(platform_type)
                texture = ELEMENT_TEXTUREPATH[platform_type]
            else:
                # Choix aléatoire de la texture parmi les options disponibles
                texture = random.choice(list(PLATFORME_TEXTUREPATH.values()))
            platform = Plateforme(x, y, width, height, texture, platform_type)
            self.platforms.add(platform)
    def loadPowerUps(self):
        """
        Load the power-ups in the environment
        :return:
        """
        for pos in positions_powerups:
            x, y, power_up_type = pos
            print(pos)
            if power_up_type == "chargeur":
                self.power_ups.add(Chargeur(x, y))
            elif power_up_type == "km":
                self.power_ups.add(Kit_Med(x, y))

    def loadElements(self):
        """
        Load the elements in the environment
        :return:
        """
        for x, y, type_element in elements_sol_fixes:
            if type_element in ELEMENT_TEXTUREPATH:
                element = ElementAuSol(x, y, 50, 50, ELEMENT_TEXTUREPATH[type_element], type_element)
                self.element_group.add(element)

    def draw(self):
        """
        Draw the environment on the screen
        :return:
        """
        bg_rect = pygame.Rect(self.x + self.camera.offset_x, self.y, self.width, self.height)
        self.screen.blit(self.background, bg_rect)
        for platform in self.platforms:
            self.screen.blit(platform.image, self.camera.apply(platform))
        for element in self.element_group:
            self.screen.blit(element.image, self.camera.apply(element))
        for power_up in self.power_ups:
            self.screen.blit(power_up.image, self.camera.apply(power_up))
        for enemy in self.enemies:
            enemy.draw()

    def update(self, player):
        """
        Update the environment
        :param player: Player instance
        :return:
        """
        for enemy in self.enemies:
            enemy.update(self.platforms, player, self)
        if self.getNumberOfEnemies() < 5:
            self.spawnMoreEnemies(1)
    def checkCollisionWithEnnemy(self, rect: pygame.Rect):
        """
        Check if the rect collides with any enemy
        :param rect: pygame.Rect
        :return: True if collides, False otherwise
        """
        for enemy in self.enemies:
            if rect.colliderect(enemy.rect):
                self.killEnemy(enemy)
                return True
        return False
    def spawnMoreEnemies(self, count: int):
        """
        Spawn more enemies in the environment
        :param count: Number of enemies to spawn
        :return:
        """
        for _ in range(count):
            platform = random.choice(self.platforms.sprites())
            x = random.randint(platform.rect.left, platform.rect.right - 30)
            y = platform.rect.top

            enemy = Enemy(x, y, 30, 30, self.screen, self.camera)
            enemy.current_platform = platform
            print("Spawned enemy at", x, y)
            self.enemies.add(enemy)
    def getNumberOfEnemies(self):
        """
        Get the number of enemies in the environment
        :return: Number of enemies
        """
        return len(self.enemies)
    def killEnemy(self, enemy):
        """
        Kill the enemy
        :param enemy: Enemy to kill
        """
        if enemy in self.enemies:
            self.enemies.remove(enemy)
            enemy.kill()

    def moveRight(self):
        """
        Move the environment to the right
        :return:
        """
        self.x -= 5
        if self.x < -self.width + self.screenWidth:
            self.x = -self.width + self.screenWidth
            return False
        return True
    def moveLeft(self):
        """
        Move the environment to the left
        :return:
        """
        self.x += 5
        if self.x > 0:
            self.x = 0
            return False
        return True

