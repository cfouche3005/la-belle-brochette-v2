import random, pygame

screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))

# Coordonnées fixes des plateformes
plateformes_fixes = [
    (100, 200, 10, 20),
    (250, 200, 150, 20),
    (400, 200, 150, 20),
    (590, 200, 150, 20),
    (1000, 200, 150, 20),
    (1250, 300, 150, 20),
    (1400, 300, 150, 20),
    (1590, 300, 150, 20),
    (3500, 500, 150, 20),
    (4000, 250, 150, 20),
    (4500, 250, 150, 20),
    (5000, 400, 150, 20),
    (5500, 250, 150, 20),
    (6000, 450, 150, 20),
]

# Coordonnées fixes des éléments au sol
elements_sol_fixes = [
    (100, 500, 50, 50),
    (500, 500, 50, 50),
]
sol_y = 475

positions_powerups = [(300, 600), (1050, 550), (1640, 475), (3550, 400)]
# Classe des plateformes
class Plateforme(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image_path):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


class Trottoir(Plateforme):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "C:/Users/audem/Downloads/GROUND.jpg")

class Voiture(Plateforme):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "C:/Users/audem/Downloads/VOITURE2.png")


class ElementAuSol(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image_path):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

class Porte(ElementAuSol):
    def __init__(self, x, y):
        super().__init__(x, y, "C:/Users/audem/Downloads/PORTE1.png")

class Escalier(ElementAuSol):
    def __init__(self, x, y):
        super().__init__(x, y, "C:/Users/audem/Downloads/ESCALIER1.png")


class Trou(ElementAuSol):
    def __init__(self, x, y):
        super().__init__(x, y, "C:/Users/audem/Downloads/TROU1.png")


class Crayon(ElementAuSol):
    def __init__(self, x, y):
        super().__init__(x, y, "C:/Users/audem/Downloads/crayon_JW.png")


class PU(pygame.sprite.Sprite):
    def __init__(self, x, y_platform, image_path):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = random.choice([y_platform - self.rect.height, 475])
        print(f"PU créé à : {self.rect}")


class Pistolet(PU):
    def __init__(self, x, y_platform):
        super().__init__(x, y_platform, "C:/Users/audem/Downloads/PISTOLET.jpg")
        self.damage = 1


class Kit_Med(PU):
    def __init__(self, x, y_platform):
        super().__init__(x, y_platform, "C:/Users/audem/Downloads/MK.jpg")


class Piece(PU):
    def __init__(self, x, y_platform):
        super().__init__(x, y_platform, "C:/Users/audem/Downloads/PIECE.jpg")

    def init_game_elements(self):
        self.platforms = pygame.sprite.Group()
        self.power_ups = pygame.sprite.Group()
        self.element_group = pygame.sprite.Group()

        for x, y, width, height in plateformes_fixes:
            texture = random.choice(["C:/Users/audem/Downloads/VOITURE2.png", "C:/Users/audem/Downloads/TROTTOIR.jpg"])
            plateforme = Plateforme(x, y, width, height, texture)
            self.platforms.add(plateforme)

        for x, y, type_element in elements_sol_fixes:
            textures = {
                "porte": "C:/Users/audem/Downloads/PORTE1.png",
                "escalier": "C:/Users/audem/Downloads/ESCALIER1.png",
                "trou": "C:/Users/audem/Downloads/TROU1.png",
                "crayon": "C:/Users/audem/Downloads/CRAYON_JW.png"
            }
            if type_element in textures:
                element = ElementAuSol(x, y, 50, 50, textures[type_element])
                self.element_group.add(element)


        powerup_textures = [
            "C:/Users/audem/Downloads/PIECE.jpg",
            "C:/Users/audem/Downloads/PISTOLET.jpg",
            "C:/Users/audem/Downloads/MK.jpg"
        ]

        for x, y in positions_powerups:
            pu = PU(x, y, random.choice(powerup_textures))
            self.power_ups.add(pu)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                self.isRunning = False
            elif event.type == pygame.KEYDOWN:
                print(f"Touche pressée : {pygame.key.name(event.key)}")
                if pygame.key.name(event.key).lower() == "w":  # Touche w pour ramasser un PU
                    print("Touche w pressée")
                    self.player.ramasser_pu(self.power_ups)

    def update(self):
        if self.gameState == "game":
            self.platforms.update()
            self.element_group.update()
            self.power_ups.update()

    def run(self):
        while self.isRunning:
            events = pygame.event.get()
            self.handle_events(events)
            self.update()
            self.screen.fill("black")

            if self.gameState == "menu":
                self.menu.draw()
                self.menu.detect_click(events)

            elif self.gameState == "game":
                self.camera.update(self.player)  # MAJ caméra
                bg_rect = pygame.Rect(self.env.x + self.camera.offset_x, self.env.y, self.env.width, self.env.height)
                self.screen.blit(self.env.background, bg_rect)

                # Affichage des Power-Ups
                for pu in self.power_ups:
                    self.screen.blit(pu.image, self.camera.apply(pu))

                    # Affichage du joueur
                self.player.draw(self.screen, self.camera)

                # Affichage des plateformes
                for plateforme in self.platforms:
                    self.screen.blit(plateforme.image, self.camera.apply(plateforme))

                # Affichage des éléments au sol
                for element in self.element_group:
                    self.screen.blit(element.image, self.camera.apply(element))

                # Affichage des blocs statiques
                for block in self.static_blocks:
                    block.draw(self.screen, self.camera)

                # Affichage de la barre de vie
                self.barre_de_vie.draw(self.screen)



