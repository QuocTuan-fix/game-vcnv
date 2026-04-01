# level_manager.py
import pygame
import json
import os

from Player import Player
from Trap import Spike
from Goal import Goal
from PatrolEnemy import PatrolEnemy
from DropEnemy import DropEnemy
from ChaseEnemy import ChaseEnemy
from DashTrap import DashTrap

#  thêm dòng này
from firebase_manager import save_progress


class LevelManager:
    def __init__(self, player_name="Guest"):
        self.level = 0
        self.player_name = player_name   # ⭐ thêm
        self.score = 0                   # ⭐ thêm
        self.level_folder = "levels"

        self.all_sprites = pygame.sprite.Group()
        self.traps = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.goals = pygame.sprite.Group()
        self.win_sound = pygame.mixer.Sound("assets/sounds/win.mp3")

        self.player = Player(100, 300)
        self.all_sprites.add(self.player)

        self.load_level(self.level)
        self.game_won = False
        self.win_option = 0 
        self.deaths = 0
        self.max_level_unlocked = 0

    def load_level(self, level_index):
        # clear
        self.all_sprites = pygame.sprite.Group()
        self.traps = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.goals = pygame.sprite.Group()

        # load json
        path = os.path.join(self.level_folder, f"level_{level_index}.json")
        if not os.path.exists(path):
            path = os.path.join(self.level_folder, "level_0.json")

        with open(path, "r") as f:
            data = json.load(f)

        # player
        self.player.rect.topleft = data["player_start"]

        # reset trạng thái player
        self.player.dead = False
        self.player.vel_x = 0
        self.player.vel_y = 0
        self.player.state = "idle"

        self.player.animations["death"].reset()

        self.all_sprites.add(self.player)

        # traps
        for t in data["traps"]:
            trap = None
            if t["type"] == "spike":
                trap = Spike(t["x"], t["y"])

            elif t["type"] == "dash":
                trap = DashTrap(
                    t["x"],
                    t["y"],
                    direction=t.get("direction", "right"),
                    speed=t.get("speed", 6),
                    dash_distance=t.get("dash_distance", 120),
                    trigger_range=t.get("trigger_range", 80)
                )

            if trap is not None:
                self.traps.add(trap)
                self.all_sprites.add(trap)

        # enemies
        for e in data["enemies"]:
            enemy = None

            if e["type"] == "patrol":
                enemy = PatrolEnemy(
                    e["x"], e["y"],
                    e["left"], e["right"],
                    e["speed"]
                )

            elif e["type"] == "drop":
                enemy = DropEnemy(
                    e["x"],
                    e["y"],
                    trigger_range=e.get("trigger_range", 40),
                    gravity=e.get("gravity", 4)
                )

            elif e["type"] == "chase":
                enemy = ChaseEnemy(
                    e["x"], e["y"],
                    e.get("speed", 2)
                )

            if enemy is not None:
                self.enemies.add(enemy)
                self.all_sprites.add(enemy)

        # goal
        for g in data["goals"]:
            if g["type"] == "goal":
                goal = Goal(g["x"], g["y"])
                self.goals.add(goal)
                self.all_sprites.add(goal)

    def update(self):
        if self.game_won:
            return
        # update player
        self.player.update()

        # update enemies
        for enemy in self.enemies:
            enemy.update(self.player)

        # update traps
        for trap in self.traps:
            if hasattr(trap, "needs_player") and trap.needs_player:
                trap.update(self.player)
            else:
                trap.update()

        # collision chết
        if not self.player.dead:
            if (
                pygame.sprite.spritecollide(self.player, self.traps, False)
                or pygame.sprite.spritecollide(self.player, self.enemies, False)
            ):
                self.player.die()
                self.deaths += 1

        # xử lý chết
        if self.player.dead:
            death_anim = self.player.animations["death"]

            if death_anim.finished:
                self.load_level(self.level)

        # ⭐⭐⭐ SỬA DUY NHẤT Ở ĐÂY ⭐⭐⭐
        if pygame.sprite.spritecollide(self.player, self.goals, False):

            self.level += 1

            path = os.path.join(self.level_folder, f"level_{self.level}.json")

            if self.level > self.max_level_unlocked:
                self.max_level_unlocked = self.level
            
            # nếu hết level -> WIN
            if not os.path.exists(path):
                print(" WIN GAME")
                self.win_sound.play()

                save_progress(self.player_name, self.level, self.deaths)

                self.game_won = True   # ⭐ đánh dấu thắng
                return
            self.load_level(self.level)
    def handle_win_input(self, event):

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_UP:
                self.win_option = (self.win_option - 1) % 2

            elif event.key == pygame.K_DOWN:
                self.win_option = (self.win_option + 1) % 2

            elif event.key == pygame.K_RETURN:

                # 0 = play again
                if self.win_option == 0:
                    self.game_won = False
                    self.level = 0
                    self.score = 0
                    self.deaths = 0
                    self.load_level(0)

                # 1 = leaderboard
                elif self.win_option == 1:
                    return "leaderboard"

                # 2 = menu
                elif self.win_option == 2:
                    return "menu"

        return None

    def draw(self, screen):
        for sprite in self.all_sprites:
            if hasattr(sprite, "draw"):
                sprite.draw(screen)
            else:
                screen.blit(sprite.image, sprite.rect)
        if self.game_won:
            font = pygame.font.SysFont(None, 60)
            small = pygame.font.SysFont(None, 40)

            screen.fill((0, 0, 0))

            title = font.render("YOU WIN!", True, (255, 255, 0))
            screen.blit(title, (280, 120))

            options = ["Play Again", "Leaderboard"]

            for i, option in enumerate(options):

                color = (255,255,0) if i == self.win_option else (255,255,255)

                text = small.render(option, True, color)
                screen.blit(text, (300, 220 + i * 50))

            return