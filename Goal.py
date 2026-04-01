import pygame
from spritesheet import load_sprite_sheet

class Goal(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        frames = load_sprite_sheet("assets/gate/gate.png", 64, 64)

        self.image = pygame.transform.scale(frames[0], (39, 64))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.rect.bottom = 332
        self.rect.x = x + 100

        

    # ======================
    # UPDATE
    # ======================

    def update(self):
        pass

    # ======================
    # DRAW
    # ======================

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))