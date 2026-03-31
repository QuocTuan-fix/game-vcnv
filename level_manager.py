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
from data_manager import save_player_score


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

        self.player = Player(100, 300)
        self.all_sprites.add(self.player)

        self.load_level(self.level)

    def load_level(self, level_index):
        # clear
        self.all_sprites = pygame.sprite.Group()
        self.traps = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.goals = pygame.sprite.Group()

        # load json
        path = os.path.join(self.level_folder, f"level_{level_index}.json")
        if not os.path.exists(path):
            self.level = 0
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

        # xử lý chết
        if self.player.dead:
            death_anim = self.player.animations["death"]

            if death_anim.finished:
                self.load_level(self.level)

        # ⭐⭐⭐ SỬA DUY NHẤT Ở ĐÂY ⭐⭐⭐
        if pygame.sprite.spritecollide(self.player, self.goals, False):

            self.score += 100  # ⭐ cộng điểm
            self.level += 1

            path = os.path.join(self.level_folder, f"level_{self.level}.json")

            # nếu hết level -> WIN
            if not os.path.exists(path):
                print("🎉 WIN GAME")

                save_player_score(self.player_name, self.score)

                # reset game
                self.level = 0
                self.score = 0
                self.load_level(self.level)
            else:
                self.load_level(self.level)

    def draw(self, screen):
        for sprite in self.all_sprites:
            if hasattr(sprite, "draw"):
                sprite.draw(screen)
            else:
                screen.blit(sprite.image, sprite.rect)