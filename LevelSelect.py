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
        self.spacing_x = 40
        self.spacing_y = 30

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

        screen_w, screen_h = screen.get_size()

        # ===== TITLE =====
        title = self.title_font.render("SELECT LEVEL", True, (255, 255, 255))
        title_rect = title.get_rect(center=(screen_w // 2, 60))
        screen.blit(title, title_rect)

        # ===== GRID SETUP =====
        rows = math.ceil(self.total_levels / self.columns)

        # base size
        box_w, box_h = 120, 60

        # total grid size
        grid_width = self.columns * box_w + (self.columns - 1) * self.spacing_x
        grid_height = rows * box_h + (rows - 1) * self.spacing_y

        # ===== AUTO SCALE nếu quá cao =====
        max_height = screen_h - 150

        if grid_height > max_height:
            scale_factor = max_height / grid_height
            box_w *= scale_factor
            box_h *= scale_factor
            spacing_x = self.spacing_x * scale_factor
            spacing_y = self.spacing_y * scale_factor
        else:
            spacing_x = self.spacing_x
            spacing_y = self.spacing_y

        # ===== CENTER GRID =====
        grid_width = self.columns * box_w + (self.columns - 1) * spacing_x
        grid_height = rows * box_h + (rows - 1) * spacing_y

        start_x = (screen_w - grid_width) // 2
        start_y = (screen_h - grid_height) // 2 + 40

        # ===== DRAW LEVELS =====
        for i in range(self.total_levels):

            col = i % self.columns
            row = i // self.columns

            x = start_x + col * (box_w + spacing_x)
            y = start_y + row * (box_h + spacing_y)

            rect = pygame.Rect(x, y, box_w, box_h)

            # ===== STYLE =====
            if i <= self.max_unlocked:
                color = (40, 40, 60)
                border = (0, 255, 0)
            else:
                color = (30, 30, 30)
                border = (100, 100, 100)

            # ===== SELECT EFFECT =====
            if i == self.selected:
                border = (255, 255, 0)
                scale = 1.1
            else:
                scale = 1.0

            scaled_rect = rect.inflate(
                rect.width * (scale - 1),
                rect.height * (scale - 1)
            )

            # ===== DRAW BOX =====
            pygame.draw.rect(screen, color, scaled_rect, border_radius=10)
            pygame.draw.rect(screen, border, scaled_rect, 3, border_radius=10)

            # ===== TEXT =====
            text = self.font.render(f"Lv {i}", True, (255, 255, 255))
            text_rect = text.get_rect(center=scaled_rect.center)
            screen.blit(text, text_rect)

            # ===== LOCK ICON =====
            if i > self.max_unlocked:
                lock_text = self.font.render("", True, (200, 200, 200))
                lock_rect = lock_text.get_rect(
                    center=(scaled_rect.centerx, scaled_rect.centery + 18)
                )
                screen.blit(lock_text, lock_rect)