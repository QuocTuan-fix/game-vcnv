    # Enemy.py
import pygame

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, w=40, h=40):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill((200, 50, 50))
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, player=None):
        pass