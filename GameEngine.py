import pygame
from level_manager import LevelManager
from LevelSelect import LevelSelect
from login_screen import login_screen
from leaderboard import show_leaderboard
from ui_overlay import UIOverlay


class Game:

    MENU = 0
    PLAYING = 1

    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((800, 450))
        pygame.display.set_caption("Die Again - Test")
        pygame.mixer.init()

        # nhạc nền
        pygame.mixer.music.load("assets/sounds/bg_music.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)  # loop

        # sound effect
        self.jump_sound = pygame.mixer.Sound("assets/sounds/jump.mp3")
        self.win_sound = pygame.mixer.Sound("assets/sounds/win.mp3")

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
        self.ui = UIOverlay()

        # ===== SYSTEMS =====
        self.level_select = LevelSelect(total_levels=3)
        # nhập tên người chơi trước
        #self.player_name = get_player_name(self.screen)
        self.player_name, data = login_screen(self.screen)

        self.level_manager = LevelManager(self.player_name)

        # load progress
        self.level_manager.level = data["level"]
        self.level_manager.deaths = data["deaths"]
        self.level_manager.load_level(self.level_manager.level)
        #  quan trọng
        self.max_level_unlocked = data["level"]

    def run(self):

        while self.running:

            for event in pygame.event.get():
                self.ui.handle_event(event)

                if event.type == pygame.QUIT:
                    self.running = False

                # ===== MENU =====
                if self.state == self.MENU:
                    # ⭐ cập nhật level đã mở
                    self.level_select.max_unlocked = self.max_level_unlocked
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
                            self.level_manager.game_won = False
                            self.level_manager.level = 0
                            self.level_manager.score = 0
                            self.level_manager.load_level(0)
                        
                        # ⭐ WIN MENU
                        if self.level_manager.game_won:
                            action = self.level_manager.handle_win_input(event)

                            if action == "leaderboard":
                                show_leaderboard(self.screen)

                            elif action == "menu":
                                self.state = self.MENU

                            continue

                        if event.type == pygame.KEYDOWN:

                            if event.key == pygame.K_ESCAPE:
                                self.state = self.MENU

                            if event.key == pygame.K_l:
                                show_leaderboard(self.screen)

            # ===== UPDATE =====
            if self.state == self.PLAYING:
                self.level_manager.update()
            self.ui.update()
            # ===== DRAW =====
            if self.state == self.MENU:

                self.screen.fill((20, 20, 20))
                self.level_select.draw(self.screen)

            elif self.state == self.PLAYING:

                # vẽ background trước
                self.screen.blit(self.background, (0, 0))

                # sau đó vẽ game
                self.level_manager.draw(self.screen)
            self.ui.draw(self.screen)
            
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()