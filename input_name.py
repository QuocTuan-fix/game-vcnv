import pygame

pygame.font.init()
FONT = pygame.font.SysFont("Arial", 50)

def get_player_name(screen):

    text = ""

    while True:
        screen.fill((255, 182, 193))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "Guest"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return text if text != "" else "Guest"
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode

        title = FONT.render("Enter Name", True, (0, 0, 0))
        screen.blit(title, (250, 120))

        name_text = FONT.render(text, True, (0, 0, 0))
        screen.blit(name_text, (250, 220))

        pygame.display.flip()