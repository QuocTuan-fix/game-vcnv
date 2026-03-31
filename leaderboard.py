import pygame
from data_manager import get_top_players

pygame.font.init()
FONT = pygame.font.SysFont("Arial", 35)

def show_leaderboard(screen):

    while True:
        screen.fill((200, 200, 255))

        title = FONT.render("TOP PLAYERS", True, (0, 0, 0))
        screen.blit(title, (280, 80))

        players = get_top_players()

        y = 150
        rank = 1
        for p in players:
            text = f"{rank}. {p['name']} - {p['score']}"
            t = FONT.render(text, True, (0, 0, 0))
            screen.blit(t, (250, y))
            y += 50
            rank += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

        pygame.display.flip()