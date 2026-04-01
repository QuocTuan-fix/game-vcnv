import pygame
from firebase_manager import get_leaderboard

pygame.font.init()

TITLE_FONT = pygame.font.SysFont("Arial", 50, bold=True)
FONT = pygame.font.SysFont("Arial", 30)

def show_leaderboard(screen):

    while True:
        screen.fill((30, 30, 60))  # nền tối đẹp hơn

        # ===== TITLE =====
        title = TITLE_FONT.render("LEADERBOARD", True, (255, 255, 0))
        screen.blit(title, (screen.get_width()//2 - title.get_width()//2, 50))

        # ===== BOX =====
        box_rect = pygame.Rect(150, 120, 500, 300)
        pygame.draw.rect(screen, (50, 50, 100), box_rect, border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), box_rect, 2, border_radius=10)

        # ===== DATA =====
        # ===== HEADER =====
        headers = ["Rank", "Name", "Level", "Deaths"]
        col_x = [180, 260, 450, 550]

        for i, h in enumerate(headers):
            text = FONT.render(h, True, (255, 255, 0))
            screen.blit(text, (col_x[i], 140))

        # ===== LINE =====
        pygame.draw.line(screen, (255, 255, 255), (170, 170), (620, 170), 2)

        # ===== DATA =====
        players = get_leaderboard()

        y = 190
        for i, p in enumerate(players):
            # 🔥 background xen kẽ
            if i % 2 == 0:
                pygame.draw.rect(screen, (40, 40, 80), (170, y-5, 450, 30))

            # màu top
            if i == 0:
                color = (255, 215, 0)
            elif i == 1:
                color = (192, 192, 192)
            elif i == 2:
                color = (205, 127, 50)
            else:
                color = (255, 255, 255)

            row = [
                str(i+1),
                p['name'],
                str(p['level']),
                str(p['deaths'])
            ]

            for j, item in enumerate(row):
                t = FONT.render(item, True, color)
                screen.blit(t, (col_x[j], y))

            y += 35

        # ===== EVENT =====
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

        pygame.display.flip()