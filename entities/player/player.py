import os
import pygame, math
from pygame.transform import rotate

from entities.bullet import Bullet
from game.camera import Camera
from game.env import Env
from environnement.vie import BarreDeVie
from environnement.environnement_jeu import Plateforme, ElementAuSol
from environnement.inventaire import Inventaire

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.projectile = []
        self.cooldown = 0

        self.image = pygame.Surface((width, height))
        self.image.fill((255, 44, 102))
        # Image de base (au repos)
        self.original_image = pygame.image.load("assets/frames/fire/fire(body)_0001.png").convert_alpha()
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.width = width
        self.height = height

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
        self.vie = BarreDeVie(5)
        self.platforms_invisibles = []
        self.inventaire = Inventaire()
        self.coeur_image = pygame.transform.scale(pygame.image.load("assets/COEUR_PA.png"), (50, 50))
        self.hearts =[]
        self.on_ground = True
        self.arm_angle = 0
        self.is_shooting = True
        self.shooting_timer = 0
        self.shooting_duration = 10


    def shoot(self, angle):
        print("shoot")
        print("angle", angle)
        # Implémentation de la logique de tir
        bullet = Bullet(self.rect.centerx, self.rect.centery, 10, 10, (0,0,0) , angle)
        self.projectile.append(bullet)
        self.vie = BarreDeVie(5)
        self.is_shooting = True
        self.shooting_timer = self.shooting_duration

        # Réinitialiser le cooldown
        self.cooldown = 15

    def ramasser_chargeur(self, power_ups, distance_min=50):
        """
        Fonction pour ramasser le power-up chargeur si le joueur est à une certaine distance.
        Si un PU est ramassé, il est supprimé de la liste des power-ups.
        Aide de GPT pour l'utilisation de ".type"
        """
        for pu in power_ups:
            if pu.type == "chargeur":
                distance_x = self.rect.centerx - pu.rect.centerx
                distance_y = self.rect.centery - pu.rect.centery
                distance = math.sqrt(distance_x ** 2 + distance_y ** 2)
                if distance <= distance_min:
                    power_ups.remove(pu)
                    self.inventaire.ajouter("chargeur")
                    return

    def ramasser_km(self, power_ups, distance_threshold=50):
        """
        Fonction pour ramasser le power-up KM si le joueur est à une certaine distance.
        Si un PU est ramassé, il est supprimé de la liste des power-ups.
        """
        for pu in power_ups:
            if pu.type == "km":
                distance_x = self.rect.centerx - pu.rect.centerx
                distance_y = self.rect.centery - pu.rect.centery
                distance = math.sqrt(distance_x ** 2 + distance_y ** 2)
                if distance <= distance_threshold:
                    power_ups.remove(pu)
                    self.inventaire.ajouter("km")
                    return

    def ramasser_crayon(self, elements_sol, distance_min=50):
        """
        Fonction pour ramasser le crayon si le joueur est à une certaine distance.
        Si un crayon est ramassé, il est supprimé de la liste des éléments au sol.
        """
        for element in elements_sol:
            if element.type == "crayon":
                distance_x = self.rect.centerx - element.rect.centerx
                distance_y = self.rect.centery - element.rect.centery
                distance = math.sqrt(distance_x ** 2 + distance_y ** 2)
                if distance <= distance_min:
                    elements_sol.remove(element)
                    self.inventaire.ajouter("crayon")
                    return

    def monter_escaliers(self, elements_sol, distance_threshold=50):
        """
        Permet au joueur de monter les escaliers s'il est à une certaine distance d'un escalier
        et appuie sur la touche Q.
        """
        for element in elements_sol:
            if element.type == "escalier":
                distance_x = self.rect.centerx - element.rect.centerx
                distance_y = self.rect.centery - element.rect.centery
                distance = math.sqrt(distance_x ** 2 + distance_y ** 2)
                if distance <= distance_threshold:
                    plateforme = Plateforme(element.rect.x + 45, 450, element.rect.width, 10, "assets/GROUND.jpg")
                    self.platforms_invisibles.append(plateforme)
                    return
        self.platform_invisible = None

    def ouvrir_portes(self, elements_sol_fixes, distance_min=50):
        """
        Permet au joueur d'ouvrir une portee s'il est à une certaine distance de cette dernière
        et pour l'ouvrir il appuie sur la touche E
        Aide de GPT pour "if isinstance(element, ElementAuSol):" car problème au niveau de l'état (fermé ou ouvert)
        lorsqu'il était placé dans la classe Porte(ElementAuSol). Pour éviter les erreurs, l'état a été placé dans la classe
        mère ElementAuSol
        """
        for element in elements_sol_fixes:
            if isinstance(element, ElementAuSol):
                if element.type == "porte":
                    distance_x = self.rect.centerx - element.rect.centerx
                    distance_y = self.rect.centery - element.rect.centery
                    distance = math.sqrt(distance_x ** 2 + distance_y ** 2)
                    if distance <= distance_min:
                        element.ouvrir()
                        break

    def check_trou_collision(self, elements_sol, runtime):
        """
        Vérifier si le joueur est tombé dans un trou, si c'est le cas il meurt directement
        """
        for element in elements_sol:
            if element.type == "trou":
                rect_trou = pygame.Rect(element.rect.x, element.rect.y, 50, 50)
                if self.rect.colliderect(rect_trou):
                    self.mourir(runtime)
                    return

    def set_game_over_image(self, image):
        self.game_over_image = image

    def afficher_game_over(self):
        """
        Affiche à l'écran gameover si le joueur est tombé dans un trou ou a été tué par les ennemis
                """
        if self.game_over_image:
            screen = pygame.display.get_surface()
            screen.blit(self.game_over_image, (150, 150))

    def check_platform_collisions_horizontal(self, env):
        """Vérifie et gère les collisions horizontales avec les plateformes"""
        for platform in env.platforms:  # On suppose que les plateformes sont accessibles via env.game.platforms
            if self.rect.colliderect(platform.rect):
                # Si c'est un escalier, on ne fait rien
                if platform.type == "escalier":
                    continue

                # Si collision, annuler le mouvement horizontal
                if self.rect.right > platform.rect.left and self.rect.left < platform.rect.left:
                    self.rect.right = platform.rect.left
                elif self.rect.left < platform.rect.right and self.rect.right > platform.rect.right:
                    self.rect.left = platform.rect.right

    def check_platform_collisions_vertical(self, env):
        """Vérifie et gère les collisions verticales avec les plateformes"""
        self.on_ground = False  # Pour savoir si le joueur est sur le sol ou une plateforme

        for platform in env.platforms:  # On suppose que les plateformes sont accessibles via env.game.platforms
            if self.rect.colliderect(platform.rect):

                # Collision par le haut (le joueur est sur la plateforme)
                if self.velocity > 0 and self.rect.bottom > platform.rect.top and self.rect.top < platform.rect.top:
                    self.rect.bottom = platform.rect.top
                    self.velocity = 0
                    self.on_ground = True
                # Collision par le bas (le joueur heurte une plateforme en sautant)
                elif self.velocity < 0 and self.rect.top < platform.rect.bottom and self.rect.bottom > platform.rect.bottom:
                    # Si la plateforme est un escalier, on ne fait rien
                    if platform.type != "escalier":
                        self.rect.top = platform.rect.bottom
                        self.velocity = 0
                    else:
                        self.on_ground = True

    def gagner_vie(self):
        if len(self.hearts) < self.vie.vies:
            self.hearts.append(self.coeur_image)

    def mourir(self, runtime):
        """
        Fait mourir le joueur et réinitialise sa barre de vie à 0
        """
        self.vie.vies = 0
        runtime.changeGameState("gameover")

    def update(self, env: Env, camera: Camera):
        # Réinitialisation de l'état de marche
        self.is_walking = False
        keys = pygame.key.get_pressed()

        # Vérification des clics de souris
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0]:  # Clic gauche
            if self.cooldown == 0:
                self.shoot(self.arm_angle-90)

        # Déplacement du joueur dans le monde
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
        self.check_platform_collisions_horizontal(env)

        # Appliquer la gravité
        self.velocity += self.gravity
        self.rect.y += self.velocity

        self.check_platform_collisions_vertical(env)

        # Ajout d'une plateforme invisible pour permettre au joueur de rester en haut d'un escalier.
        # Lorsqu'il est au sommet de l'escalier, cette plateforme invisible lui permet de marcher ou sauter
        # vers d'autres plateformes sans tomber immédiatement, en le maintenant à une hauteur stable.
        for plateforme in self.platforms_invisibles:
            if self.rect.colliderect(plateforme.rect):
                self.rect.y = plateforme.rect.top
                self.velocity = 0

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

        if self.is_shooting:
            if self.shooting_timer > 0:
                # Utiliser les sprites de tir
                self.original_image = pygame.image.load("assets/frames/fire/fire(body)_0002.png").convert_alpha()
                self.arm_original = pygame.transform.rotate(
                    pygame.image.load("assets/frames/fire/fire(arm)_0002.png").convert_alpha(), -90)
                self.shooting_timer -= 1
            else:
                # Revenir aux sprites normaux
                self.original_image = pygame.image.load("assets/frames/fire/fire(body)_0001.png").convert_alpha()
                self.arm_original = pygame.transform.rotate(
                    pygame.image.load("assets/frames/fire/fire(arm)_0001.png").convert_alpha(), -90)
                self.is_shooting = False

        # Mettre à jour l'image après avoir géré l'animation de tir
        self.update_player_image()

        # Mise à jour de la caméra
        camera.update(self)
        if self.cooldown > 0:
            self.cooldown -= 1

        # Mise à jour de l'angle du bras en fonction de la position de la souris
        self.update_arm_angle(camera)

    def update_player_image(self):
        """Met à jour l'image du joueur en fonction de l'animation et de l'orientation"""
        if self.is_walking:
            self.image = self.walk_frames[self.current_frame].copy()
        else:
            self.image = self.original_image.copy()

        if not self.facing_right:
            self.image = pygame.transform.flip(self.image, True, False)

    def jump(self):
        if self.rect.y == 500 or self.on_ground:
            self.velocity = -self.jump_height

    def update_arm_angle(self, camera):
        # Obtenir la position de la souris (en coordonnées d'écran)
        mouse_pos = pygame.mouse.get_pos()

        # Créer un objet temporaire avec la position du point de pivot
        pivot_world_pos = pygame.Rect(self.rect.x + self.pivot[0], self.rect.y + self.pivot[1], 1, 1)
        temp_sprite = TempSprite(pivot_world_pos)

        # Appliquer la caméra pour obtenir la position à l'écran
        pivot_screen_pos = camera.apply(temp_sprite)

        # Calculer l'angle entre le point de pivot et la position de la souris
        d_pos = pygame.Vector2(mouse_pos[0] - pivot_screen_pos.x,
                               mouse_pos[1] - pivot_screen_pos.y)
        self.arm_angle = math.degrees(math.atan2(d_pos[0], d_pos[1]))

        # Orientation du joueur en fonction de l'angle du bras
        should_face_right = -0 <= self.arm_angle <= 180

        if should_face_right != self.facing_right:
            self.facing_right = should_face_right
            self.update_player_image()

        # Rotation du bras
        arm_to_rotate = self.arm_original.copy()
        if not self.facing_right:
            arm_to_rotate = pygame.transform.flip(arm_to_rotate, True, False)
        rotated_arm = pygame.transform.rotate(arm_to_rotate, self.arm_angle)

        # Positionnement du bras dans le monde, pas à l'écran
        # On stocke dans arm_rect les coordonnées du monde, pas de l'écran
        self.arm_rect = rotated_arm.get_rect()

        # Le bras doit être attaché au joueur dans le monde, pas à l'écran
        self.arm_rect.center = (self.rect.x + self.pivot[0], self.rect.y + self.pivot[1])

        self.arm_image = rotated_arm

    def draw(self, surface, camera):
        """
        Ajouter de la vie au personnage s'il a un kit dans son inventaire.
        Reprise de l'affichage des vies utilisé dans la classe BarreDeVie
        Les vies seront ajoutées aux endroits où il y a un vide (aide de GPT pour ceci)
        """
        # Dessin de l'entité avec le décalage de la caméra
        rect_camera = camera.apply(self)
        surface.blit(self.image, rect_camera)
        temp_sprite = TempSprite(self.arm_rect)
        arm_rect_camera = camera.apply(temp_sprite)
        surface.blit(self.arm_image, arm_rect_camera)
        for bullet in self.projectile:
            bullet.draw(surface, camera)

        x_offset = 20
        y_offset = 20
        for i in range(5):
            if i < self.vie.vies:
                surface.blit(self.coeur_image, (x_offset + i * 45, y_offset))
            else:
                empty_heart = pygame.Surface((30, 30), pygame.SRCALPHA) #"couleur transparente"
                surface.blit(empty_heart, (x_offset + i * 45, y_offset))  # Afficher le coeur vide avec la couleur invisible

# Solution 2: Créer un sprite temporaire
class TempSprite:
    def __init__(self, rect):
        self.rect = rect
