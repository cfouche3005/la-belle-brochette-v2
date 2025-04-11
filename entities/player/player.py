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
    def __init__(self, x, y, width, height, game_over_cb = None):
        """
        Initialise le joueur
        :param x: Origine x du joueur
        :param y: Origine y du joueur
        :param width: Largeur du joueur
        :param height: Hauteur du joueur
        :param game_over_cb: Fonction de rappel pour le game over
        """
        super().__init__()
        self.projectile = []
        self.cooldown = 0

        self.image = pygame.Surface((width, height))
        self.image.fill((255, 44, 102))
        # Image de base (au repos)
        self.original_image = pygame.image.load("assets/frames/fire/fire(body)_0001.png").convert_alpha()
        self.image = self.original_image.copy()
        self.width = width
        self.height = height

        hitbox_width = int(width * 0.7)  # Largeur de la hitbox
        hitbox_height = int(height * 0.7)

        # Centrage de la hitbox
        hitbox_x = x + (width - hitbox_width) // 2
        hitbox_y = y + (height - hitbox_height) // 2

        # Création de la hitbox
        self.hitbox = pygame.Rect(hitbox_x, hitbox_y, hitbox_width, hitbox_height)


        self.rect = self.image.get_rect()
        self.update_rect_from_hitbox()

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

        print("Callback de la fonction game_over_cb")
        print(game_over_cb)
        self.gameOverCb = game_over_cb

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
        self.vie = BarreDeVie(5, lambda: self.callGameOver())
        self.platforms_invisibles = []
        self.inventaire = Inventaire()
        self.coeur_image = pygame.transform.scale(pygame.image.load("assets/COEUR_PA.png"), (50, 50))
        self.hearts =[]
        self.on_ground = True
        self.arm_angle = 0
        self.is_shooting = True
        self.shooting_timer = 0
        self.shooting_duration = 10

    def callGameOver(self):
        """
        Fonction pour appeler le game over
        """
        if self.gameOverCb:
            self.gameOverCb()

    def update_rect_from_hitbox(self):
        """Mise à jour du rect d'affichage en fonction de la hitbox"""
        # Le rect est plus grand que la hitbox, on le centre sur celle-ci
        offset_x = (self.hitbox.width - self.rect.width) // 2
        offset_y = (self.hitbox.height - self.rect.height) // 2
        self.rect.x = self.hitbox.x - (self.rect.width + offset_x) // 2
        self.rect.y = self.hitbox.y - (self.rect.height + offset_y)

    def shoot(self, angle, env: Env):
        """
        Fonction pour tirer une balle
        :param angle: Angle de tir
        :param env: Instance de l'environnement pour la gestion des projectiles
        :return:
        """
        print("shoot")
        print("angle", angle)
        # Implémentation de la logique de tir
        bullet = Bullet(self.rect.centerx, self.rect.centery, 10, 10, (0,0,0) , angle, env, lambda : self.deleteBullet(bullet))
        self.projectile.append(bullet)
        self.is_shooting = True
        self.shooting_timer = self.shooting_duration

        # Réinitialiser le cooldown
        self.cooldown = 15

    def deleteBullet(self, bullet):
        """
        Fonction pour supprimer une balle de la liste des projectiles
        :param bullet: Balle à supprimer
        """
        if bullet in self.projectile:
            self.projectile.remove(bullet)
            bullet.kill()
            print("Balle supprimée")
        else:
            print("Balle non trouvée dans la liste des projectiles")

    def ramasser_chargeur(self, power_ups, distance_min=50):
        """
        Fonction pour ramasser le power-up chargeur si le joueur est à une certaine distance.
        Si un PU est ramassé, il est supprimé de la liste des power-ups.
        :param power_ups: Liste des power-ups
        :param distance_min: Distance minimale pour ramasser le PU
        """
        for pu in power_ups:
            if pu.type == "chargeur":
                distance_x = self.hitbox.centerx - pu.rect.centerx
                distance_y = self.hitbox.centery - pu.rect.centery
                distance = math.sqrt(distance_x ** 2 + distance_y ** 2)
                if distance <= distance_min:
                    power_ups.remove(pu)
                    self.inventaire.ajouter("chargeur")
                    return

    def ramasser_km(self, power_ups, distance_threshold=50):
        """
        Fonction pour ramasser le power-up KM si le joueur est à une certaine distance.
        Si un PU est ramassé, il est supprimé de la liste des power-ups.
        :param power_ups: Liste des power-ups
        :param distance_threshold: Distance minimale pour ramasser le PU
        """
        for pu in power_ups:
            if pu.type == "km":
                distance_x = self.hitbox.centerx - pu.rect.centerx
                distance_y = self.hitbox.centery - pu.rect.centery
                distance = math.sqrt(distance_x ** 2 + distance_y ** 2)
                if distance <= distance_threshold:
                    power_ups.remove(pu)
                    self.inventaire.ajouter("km")
                    return

    def ramasser_crayon(self, elements_sol, distance_min=50):
        """
        Fonction pour ramasser le crayon si le joueur est à une certaine distance.
        Si un crayon est ramassé, il est supprimé de la liste des éléments au sol.
        :param elements_sol: Liste des éléments au sol
        :param distance_min: Distance minimale pour ramasser le crayon
        """
        for element in elements_sol:
            if element.type == "crayon":
                distance_x = self.hitbox.centerx - element.rect.centerx
                distance_y = self.hitbox.centery - element.rect.centery
                distance = math.sqrt(distance_x ** 2 + distance_y ** 2)
                if distance <= distance_min:
                    elements_sol.remove(element)
                    self.inventaire.ajouter("crayon")
                    return

    def ouvrir_portes(self, elements_sol_fixes, distance_min=50):
        """
        Permet au joueur d'ouvrir une portee s'il est à une certaine distance de cette dernière
        et pour l'ouvrir il appuie sur la touche E
        Aide de GPT pour "if isinstance(element, ElementAuSol):" car problème au niveau de l'état (fermé ou ouvert)
        lorsqu'il était placé dans la classe Porte(ElementAuSol). Pour éviter les erreurs, l'état a été placé dans la classe
        mère ElementAuSol
        :param elements_sol_fixes: Liste des éléments au sol fixes
        :param distance_min: Distance minimale pour ouvrir la porte
        """
        for element in elements_sol_fixes:
            if isinstance(element, ElementAuSol): #vérifie si l'élément fait partie de la classe ElementAuSol
                if element.type == "porte":
                    distance_x = self.hitbox.centerx - element.rect.centerx
                    distance_y = self.hitbox.centery - element.rect.centery
                    distance = math.sqrt(distance_x ** 2 + distance_y ** 2)
                    if distance <= distance_min:
                        element.ouvrir()
                        break

    def check_trou_collision(self, elements_sol, runtime):
        """
        Vérifier si le joueur est tombé dans un trou, si c'est le cas il meurt directement
        :param elements_sol: Liste des éléments au sol
        :param runtime: Instance de l'environnement pour la gestion des projectiles
        """
        for element in elements_sol:
            if element.type == "trou":
                rect_trou = pygame.Rect(element.rect.x, element.rect.y, 50, 50)
                if self.hitbox.colliderect(rect_trou):
                    self.mourir(runtime)
                    return

    def afficher_game_over(self):
        """
        Affiche à l'écran gameover si le joueur est tombé dans un trou ou a été tué par les ennemis
                """
        if self.game_over_image:
            screen = pygame.display.get_surface()
            screen.blit(self.game_over_image, (150, 150))

    def check_platform_collisions_horizontal(self, env):
        """
        Vérifie les collisions horizontales avec les plateformes
        :param env:  Instance de l'environnement pour la gestion des plateformes
        :return:
        """
        for platform in env.platforms:
            if self.hitbox.colliderect(platform.rect):
                if platform.type == "escalier":
                    continue

                # Si collision, ajuster la hitbox
                if self.hitbox.right > platform.rect.left and self.hitbox.left < platform.rect.left:
                    self.hitbox.right = platform.rect.left
                elif self.hitbox.left < platform.rect.right and self.hitbox.right > platform.rect.right:
                    self.hitbox.left = platform.rect.right

    def check_platform_collisions_vertical(self, env):
        """Vérifie les collisions verticales avec les plateformes
        :param env: Instance de l'environnement pour la gestion des plateformes"""
        self.on_ground = False

        for platform in env.platforms:
            if self.hitbox.colliderect(platform.rect):
                # Collision par le haut
                if self.velocity > 0 and self.hitbox.bottom > platform.rect.top and self.hitbox.top < platform.rect.top:
                    self.hitbox.bottom = platform.rect.top
                    self.velocity = 0
                    self.on_ground = True
                # Collision par le bas
                elif self.velocity < 0 and self.hitbox.top < platform.rect.bottom and self.hitbox.bottom > platform.rect.bottom:
                    if platform.type != "escalier":
                        self.hitbox.top = platform.rect.bottom
                        self.velocity = 0
                    else:
                        self.on_ground = True

    def gagner_vie(self):
        """Ajoute une vie au joueur"""
        if len(self.hearts) < self.vie.vies:
            self.hearts.append(self.coeur_image)

    def mourir(self, runtime):
        """
        Fait mourir le joueur et réinitialise sa barre de vie à 0
        :param runtime: Instance de l'environnement pour la gestion des plateformes
        """
        self.vie.vies = 0
        runtime.changeGameState("gameover")

    def update(self, env: Env, camera: Camera):
        """
        Met à jour la position du joueur, gère les entrées clavier et les animations
        :param env: Instance de l'environnement pour la gestion des plateformes
        :param camera: Instance de la caméra pour le défilement
        :return:
        """
        # Réinitialisation de l'état de marche
        self.is_walking = False
        keys = pygame.key.get_pressed()

        # Vérification des clics de souris
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0]:  # Clic gauche
            if self.cooldown == 0:
                self.shoot(self.arm_angle-90, env)

        # Déplacement du joueur dans le monde
        if keys[pygame.K_LEFT]:
            self.hitbox.x -= self.speed  # Déplacer la hitbox
            self.is_walking = True
            if self.facing_right:
                self.facing_right = False
                self.update_player_image()
        if keys[pygame.K_RIGHT]:
            self.hitbox.x += self.speed  # Déplacer la hitbox
            self.is_walking = True
            if not self.facing_right:
                self.facing_right = True
                self.update_player_image()
        if keys[pygame.K_UP]:
            self.jump()
        if keys[pygame.K_w]:
            self.ramasser_chargeur(env.power_ups)
            self.ramasser_km(env.power_ups)
            self.ramasser_crayon(env.element_group)
        if keys[pygame.K_e]:
            self.ouvrir_portes(env.element_group)
        if keys[pygame.K_s]:
            if self.vie.vies < 5 and self.inventaire.possede("km"):
                self.vie.vies += 1
                self.gagner_vie()
                self.inventaire.retirer("km")


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
        self.hitbox.y += self.velocity

        self.check_platform_collisions_vertical(env)

        # Limites du monde
        if self.hitbox.y > 500:
            self.hitbox.y = 500
            self.velocity = 0
        if self.hitbox.y < 0:
            self.hitbox.y = 0
            self.velocity = 0
        if self.hitbox.x < 0:
            self.hitbox.x = 0
        if self.hitbox.x > env.width - self.width:
            self.hitbox.x = env.width - self.width

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
        self.update_rect_from_hitbox()

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
        """
        Fonction pour faire sauter le joueur
        :return:
        """
        if self.hitbox.y == 500 or self.on_ground:
            self.velocity = -self.jump_height

    def update_arm_angle(self, camera):
        """
        Met à jour l'angle du bras en fonction de la position de la souris
        :param camera:
        Fait avec GPT mais retravaillé car GPt est mauvais dans les calculs mathématiques
        """
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
        :param surface: Surface sur laquelle dessiner le joueur
        :param camera: Instance de la caméra pour le défilement
        """
        # Dessin de l'entité avec le décalage de la caméra
        rect_camera = camera.apply(self)
        surface.blit(self.image, rect_camera)
        temp_sprite = TempSprite(self.arm_rect)
        arm_rect_camera = camera.apply(temp_sprite)
        surface.blit(self.arm_image, arm_rect_camera)
        for bullet in self.projectile:
            bullet.draw(surface, camera)

        hitbox_temp = pygame.Rect(self.hitbox.x, self.hitbox.y, self.hitbox.width, self.hitbox.height)
        hitbox_sprite = TempSprite(hitbox_temp)
        hitbox_camera = camera.apply(hitbox_sprite)
        pygame.draw.rect(surface, (255, 0, 0), hitbox_camera, 2)  # Rouge avec épaisseur de 2 pixels

        x_offset = 20
        y_offset = 20
        for i in range(5):
            if i < self.vie.vies:
                surface.blit(self.coeur_image, (x_offset + i * 45, y_offset))
            else:
                empty_heart = pygame.Surface((30, 30), pygame.SRCALPHA) #"couleur transparente"
                surface.blit(empty_heart, (x_offset + i * 45, y_offset))  # Afficher le coeur vide avec la couleur invisible

class TempSprite:
    def __init__(self, rect):
        self.rect = rect
