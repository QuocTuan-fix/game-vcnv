import pygame
from spritesheet import load_sprite_sheet


class Spike(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()

        # ===== HITBOX =====
        self.rect = pygame.Rect(x, y, 39, 64)
        

        # ===== IMAGE =====
        frames = load_sprite_sheet("assets/trap/spike.png", 32, 32)

        self.image = frames[0]   # spike chỉ có 1 frame

    def update(self):
        pass

    def draw(self, screen):

        screen.blit(self.image, (self.rect.x, self.rect.y))