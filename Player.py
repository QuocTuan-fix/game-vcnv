import pygame
from spritesheet import load_sprite_sheet
from Animation import Animation
from utils import resource_path


class Player(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()

        # ===== HITBOX =====
        self.rect = pygame.Rect(x, y, 30, 30)

        # ===== ANIMATION =====
        self.animations = {

            "idle": Animation(load_sprite_sheet(resource_path(
                "assets/player/Idle.png"), 64, 64)),

            "run": Animation(load_sprite_sheet(resource_path(
                "assets/player/Walk.png"), 64, 64)),

            "jump": Animation(load_sprite_sheet(resource_path(
                "assets/player/JumpFallLand.png"), 64, 64)),

            "death": Animation(load_sprite_sheet(resource_path(
                "assets/player/Death.png"), 64, 64),speed=6,loop=False)
        }
        self.prev_state = "idle"
        self.state = "idle"
        self.image = self.animations[self.state].get()

        # ===== MOVEMENT =====
        self.vel_x = 0
        self.vel_y = 0

        self.speed = 8
        self.jump_power = -13

        self.on_ground = False
        self.dead = False
        self.death_timer = 0
        self.jump_sound = pygame.mixer.Sound(resource_path("assets/sounds/jump.ogg"))

    # ======================
    # PLAYER DIE
    # ======================

    def die(self):
        if not self.dead:
            self.dead = True
            self.state = "death"

            self.animations["death"].reset()
            self.death_timer = 0

    # ======================
    # UPDATE
    # ======================

    def update(self):

        # ===== DEATH ANIMATION =====
        if self.dead:

            anim = self.animations["death"]
            anim.update()
            self.image = anim.get()

            return

        # ===== INPUT =====
        keys = pygame.key.get_pressed()

        self.vel_x = 0

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.vel_x = -self.speed

        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.vel_x = self.speed

        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = self.jump_power
            self.on_ground = False
            if not self.dead:
                self.jump_sound.play()

        # ===== GRAVITY =====
        self.vel_y += 0.8

        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

        # ===== GROUND =====
        if self.rect.bottom >= 320:
            self.rect.bottom = 320
            self.vel_y = 0
            self.on_ground = True

        # ===== STATE =====

        if not self.on_ground:
            new_state = "jump"

        elif self.vel_x != 0:
            new_state = "run"

        else:
            new_state = "idle"

        # reset animation khi đổi state
        if new_state != self.state:
            self.animations[new_state].reset()

        self.state = new_state


        # ===== UPDATE ANIMATION =====

        anim = self.animations[self.state]
        anim.update()

        frame = anim.get()
        self.image = pygame.transform.smoothscale(frame, (75, 75)) 

    # ======================
    # DRAW
    # ======================

    def draw(self, screen):

        # sprite lớn hơn hitbox
        draw_x = self.rect.x - 26
        draw_y = self.rect.y - 26

        screen.blit(self.image, (draw_x, draw_y))