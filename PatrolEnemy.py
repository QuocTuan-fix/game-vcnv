import pygame
from Enemy import Enemy
from spritesheet import load_sprite_sheet
from Animation import Animation
from utils import resource_path


class PatrolEnemy(Enemy):

    def __init__(self, x, y, left_limit, right_limit, speed=2):
        super().__init__(x, y)

        self.rect = pygame.Rect(x, y, 70, 35)
        self.rect.bottom = 280

        self.animation = Animation(
            load_sprite_sheet(resource_path("assets/enemy/patrol/Bat.png"), 16, 16),
            speed=0.8
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
        self.image = pygame.transform.smoothscale(self.image, (40, 40)) 

    def draw(self, screen):

        draw_x = self.rect.x - 2
        draw_y = self.rect.y - 2

        screen.blit(self.image, (draw_x, draw_y))