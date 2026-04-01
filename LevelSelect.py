import pygame


class LevelSelect:

    def __init__(self, total_levels=5):
        self.total_levels = total_levels
        self.selected = 0
        self.max_unlocked = 0

        self.font = pygame.font.SysFont(None, 40)

    def handle_event(self, event):

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_RIGHT:
                self.selected = (self.selected + 1) % self.total_levels

            elif event.key == pygame.K_LEFT:
                self.selected = (self.selected - 1) % self.total_levels

            elif event.key == pygame.K_RETURN:
                if self.selected <= self.max_unlocked:
                    return self.selected

        return None

    def draw(self, screen):

        screen.fill((20, 20, 20))

        title = self.font.render("SELECT LEVEL", True, (255, 255, 255))
        screen.blit(title, (300, 80))

        for i in range(self.total_levels):

            if i <= self.max_unlocked:
                color = (0, 255, 0)   # 🟢 mở
            else:
                color = (100, 100, 100)  # 🔒 khóa

            if i == self.selected:
                color = (255, 255, 0)

            text = self.font.render(f"Level {i}", True, color)

            screen.blit(text, (330, 150 + i * 50))