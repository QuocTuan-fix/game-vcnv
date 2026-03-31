from Enemy import Enemy
import pygame
from spritesheet import load_sprite_sheet
from Animation import Animation


class DropEnemy(Enemy):

    needs_player = True

    def __init__(self, x, y, gravity=0.6, trigger_range=100):
        super().__init__(x, y)

        # ===== HITBOX =====
        self.rect = pygame.Rect(x, y, 20, 40)

        # ===== PHYSICS =====
        self.gravity = gravity
        self.vel_y = 0
        self.active = False
        self.trigger_range = trigger_range
        self.x_tolerance = 20

        # ===== ANIMATION =====
        frames = load_sprite_sheet("assets/enemy/drop/fire.png", 40, 123)

        # scale riêng cho drop enemy
        frames = [pygame.transform.scale(f, (25, 70)) for f in frames]

        self.animation = Animation(frames, speed=6)

    # =========================
    # UPDATE
    # =========================

    def update(self, player):

        # check player đứng dưới
        if not self.active:

            dx = abs(player.rect.centerx - self.rect.centerx)
            player_is_below = player.rect.top >= self.rect.bottom

            if dx <= self.x_tolerance and player_is_below:
                self.active = True

        # rơi
        if self.active:

            self.vel_y += self.gravity
            self.rect.y += self.vel_y

            if self.rect.bottom >= 327:
                self.rect.bottom = 327
                self.vel_y = 0
                self.active = False

        # animation
        self.animation.update()
        self.image = self.animation.get()

    # =========================
    # DRAW
    # =========================

    def draw(self, screen):

        draw_x = self.rect.x - 10
        draw_y = self.rect.y - 20

        screen.blit(self.image, (draw_x, draw_y))