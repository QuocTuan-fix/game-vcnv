import pygame
from Enemy import Enemy
from spritesheet import load_sprite_sheet
from Animation import Animation


class PatrolEnemy(Enemy):

    def __init__(self, x, y, left_limit, right_limit, speed=2):
        super().__init__(x, y)

        self.rect = pygame.Rect(x, y, 8, 8)

        self.animation = Animation(
            load_sprite_sheet("assets/enemy/patrol/Bat.png", 16, 16),
            speed=0.2
        )

        self.image = self.animation.get()

        self.left_limit = left_limit
        self.right_limit = right_limit
        self.speed = speed

    def update(self, player=None):

        self.rect.x += self.speed

        if self.rect.left <= self.left_limit or self.rect.right >= self.right_limit:
            self.speed *= -1

        self.animation.update()
        self.image = self.animation.get()

    def draw(self, screen):

        draw_x = self.rect.x - 8
        draw_y = self.rect.y - 8

        screen.blit(self.image, (draw_x, draw_y))