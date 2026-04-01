import pygame
from firebase_manager import get_leaderboard

pygame.font.init()
FONT = pygame.font.SysFont("Arial", 35)

def show_leaderboard(screen):

    while True:
        screen.fill((200, 200, 255))

        title = FONT.render("ONLINE LEADERBOARD", True, (0, 0, 0))
        screen.blit(title, (220, 80))

        #players = get_leaderboard_online()

        y = 150
        players = get_leaderboard()
        for i, p in enumerate(players):
            text = f"{p['name']} - Lv {p['level']} - Deaths {p['deaths']}"
            t = FONT.render(text, True, (0, 0, 0))
            screen.blit(t, (250, y))
            y += 50

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

        pygame.display.flip()