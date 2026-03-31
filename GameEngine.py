import pygame
from level_manager import LevelManager
from LevelSelect import LevelSelect


class Game:

    MENU = 0
    PLAYING = 1

    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((800, 450))
        pygame.display.set_caption("Die Again - Test")

        self.clock = pygame.time.Clock()
        self.running = True

        print("GAME STARTED")

        # ===== BACKGROUND =====
        self.background = pygame.image.load(
            "assets/background/background.png"
        ).convert()

        self.background = pygame.transform.smoothscale(
            self.background, (800, 450)
        )       

        # ===== STATE =====
        self.state = self.MENU

        # ===== SYSTEMS =====
        self.level_select = LevelSelect(total_levels=5)
        self.level_manager = LevelManager()

    def run(self):

        while self.running:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.running = False

                # ===== MENU =====
                if self.state == self.MENU:

                    level = self.level_select.handle_event(event)

                    if level is not None:
                        self.level_manager.level = level
                        self.level_manager.load_level(level)
                        self.state = self.PLAYING

                # ===== PLAYING =====
                elif self.state == self.PLAYING:

                    if event.type == pygame.KEYDOWN:

                        if event.key == pygame.K_ESCAPE:
                            self.state = self.MENU

                        if event.key == pygame.K_r:
                            self.level_manager.load_level(
                                self.level_manager.level
                            )

                        if event.key == pygame.K_n:
                            self.level_manager.next_level()

            # ===== UPDATE =====
            if self.state == self.PLAYING:
                self.level_manager.update()

            # ===== DRAW =====
            if self.state == self.MENU:

                self.screen.fill((20, 20, 20))
                self.level_select.draw(self.screen)

            elif self.state == self.PLAYING:

                # vẽ background trước
                self.screen.blit(self.background, (0, 0))

                # sau đó vẽ game
                self.level_manager.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()