import pygame
from spritesheet import load_sprite_sheet
from utils import resource_path


class Spike(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()

        # ===== HITBOX =====
        self.rect = pygame.Rect(x, y, 70, 30)
        self.rect.bottom = 325

        # ===== IMAGE =====
        frames = load_sprite_sheet(resource_path("assets/trap/spike.png"), 70, 30)

        self.image = frames[0]   # spike chỉ có 1 frame

    def update(self):
        pass

    def draw(self, screen):

        screen.blit(self.image, (self.rect.x, self.rect.y))