import pygame
import os

from level_manager import LevelManager
from LevelSelect import LevelSelect
from login_screen import login_screen
from leaderboard import show_leaderboard
from ui_overlay import UIOverlay
from utils import resource_path


class Game:

    MENU = 0
    PLAYING = 1

    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode((800, 450))
        pygame.display.set_caption("Die Again - Troll Edition 💀")

        self.clock = pygame.time.Clock()
        self.running = True

        # ===== BACKGROUND =====
        self.background = pygame.image.load(
            resource_path("assets/background/background.png")
        ).convert()

        self.background = pygame.transform.smoothscale(
            self.background, (800, 450)
        )

        # ===== AUDIO =====
        pygame.mixer.music.load(resource_path("assets/sounds/bg_music.ogg"))
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

        self.win_sound = pygame.mixer.Sound(resource_path("assets/sounds/win.ogg"))

        # ===== UI =====
        self.ui = UIOverlay()

        # ===== LOGIN =====
        self.player_name, data = login_screen(self.screen)

        # ===== SYSTEM =====
        self.level_manager = LevelManager(self.player_name)

        # load progress
        self.level_manager.level = data["level"]
        self.level_manager.deaths = data["deaths"]
        self.level_manager.max_level_unlocked = data["level"]

        self.level_manager.load_level(self.level_manager.level)

        # ===== LEVEL SELECT (AUTO COUNT) =====
        self.level_select = LevelSelect()  # ⭐ tự count level

        # sync data
        self.level_select.max_unlocked = self.level_manager.max_level_unlocked
        self.level_select.selected = self.level_manager.level

        # ===== STATE =====
        self.state = self.MENU

    # ======================
    # START LEVEL (callback style)
    # ======================
    def start_level(self, level):
        self.level_manager.level = level
        self.level_manager.load_level(level)
        self.state = self.PLAYING

    # ======================
    # MAIN LOOP
    # ======================
    def run(self):

        while self.running:

            for event in pygame.event.get():

                self.ui.handle_event(event)

                if event.type == pygame.QUIT:
                    self.running = False

                # ===== MENU =====
                if self.state == self.MENU:

                    # sync unlock mỗi frame
                    self.level_select.max_unlocked = self.level_manager.max_level_unlocked

                    level = self.level_select.handle_event(event)

                    if level is not None:
                        self.start_level(level)

                # ===== PLAYING =====
                elif self.state == self.PLAYING:

                    if event.type == pygame.KEYDOWN:

                        # ESC về menu
                        if event.key == pygame.K_ESCAPE:
                            self.state = self.MENU
                            self.level_select.selected = self.level_manager.level

                        # RESET GAME
                        elif event.key == pygame.K_r:
                            self.level_manager.game_won = False
                            self.level_manager.level = 0
                            self.level_manager.deaths = 0
                            self.level_manager.load_level(0)

                        # LEADERBOARD
                        elif event.key == pygame.K_l:
                            show_leaderboard(self.screen)

                        # WIN MENU
                        if self.level_manager.game_won:
                            action = self.level_manager.handle_win_input(event)

                            if action == "leaderboard":
                                show_leaderboard(self.screen)

                            elif action == "menu":
                                self.state = self.MENU

                            continue

            # ===== UPDATE =====
            if self.state == self.PLAYING:
                self.level_manager.update()

                # ⭐ sync unlock khi qua màn
                self.level_select.max_unlocked = self.level_manager.max_level_unlocked

            self.ui.update()

            # ===== DRAW =====
            if self.state == self.MENU:
                self.screen.fill((20, 20, 20))
                self.level_select.draw(self.screen)

            elif self.state == self.PLAYING:
                self.screen.blit(self.background, (0, 0))
                self.level_manager.draw(self.screen)

            self.ui.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()