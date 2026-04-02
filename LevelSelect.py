import pygame
import math
import os

class LevelSelect:

    def __init__(self, level_folder="levels"):
        self.level_folder = level_folder
        self.total_levels = self.count_levels()
        self.selected = 0
        self.max_unlocked = 0

        self.font = pygame.font.SysFont("arial", 30)
        self.title_font = pygame.font.SysFont("arial", 50)

        # layout
        self.columns = 3
        self.spacing_x = 180
        self.spacing_y = 100

        # animation
        self.scale = 1.0

    def count_levels(self):
        count = 0
        while True:
            path = os.path.join(self.level_folder, f"level_{count}.json")
            if os.path.exists(path):
                count += 1
            else:
                break
        return count
    def handle_event(self, event):

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_RIGHT:
                self.selected = (self.selected + 1) % self.total_levels

            elif event.key == pygame.K_LEFT:
                self.selected = (self.selected - 1) % self.total_levels

            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + self.columns) % self.total_levels

            elif event.key == pygame.K_UP:
                self.selected = (self.selected - self.columns) % self.total_levels

            elif event.key == pygame.K_RETURN:
                if self.selected <= self.max_unlocked:
                    return self.selected

        return None

    def draw(self, screen):

        screen.fill((15, 15, 25))

        # ===== TITLE =====
        title = self.title_font.render("SELECT LEVEL", True, (255, 255, 255))
        screen.blit(title, (220, 40))

        start_x = 140
        start_y = 120

        for i in range(self.total_levels):

            col = i % self.columns
            row = i // self.columns

            x = start_x + col * self.spacing_x
            y = start_y + row * self.spacing_y

            rect = pygame.Rect(x, y, 120, 60)

            # ===== STYLE =====
            if i <= self.max_unlocked:
                color = (40, 40, 60)
                border = (0, 255, 0)
            else:
                color = (30, 30, 30)
                border = (100, 100, 100)

            # SELECTED EFFECT
            if i == self.selected:
                border = (255, 255, 0)
                scale = 1.1
            else:
                scale = 1.0

            # SCALE EFFECT
            scaled_rect = rect.inflate(
                rect.width * (scale - 1),
                rect.height * (scale - 1)
            )

            # DRAW BOX
            pygame.draw.rect(screen, color, scaled_rect, border_radius=10)
            pygame.draw.rect(screen, border, scaled_rect, 3, border_radius=10)

            # ===== TEXT =====
            text = self.font.render(f"Lv {i}", True, (255, 255, 255))
            text_rect = text.get_rect(center=scaled_rect.center)
            screen.blit(text, text_rect)

            # ===== LOCK ICON =====
            if i > self.max_unlocked:
                lock_text = self.font.render("🔒", True, (200, 200, 200))
                lock_rect = lock_text.get_rect(center=(scaled_rect.centerx, scaled_rect.centery + 20))
                screen.blit(lock_text, lock_rect)