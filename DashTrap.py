import pygame
from Enemy import Enemy
from spritesheet import load_sprite_sheet
from Animation import Animation

class DashTrap(Enemy):

    # STATE
    IDLE = 0
    FAKE = 1
    DASH = 2
    COOLDOWN = 3

    needs_player = True

    def __init__(
        self,
        x,
        y,
        direction="right",
        speed=6,
        dash_distance=120,
        trigger_range=80,
        cooldown=120,
        aim_player=True,
        enable_fake=False
    ):
        super().__init__(x, y)

        # STATE
        self.state = self.IDLE

        # MOVEMENT
        self.speed = speed
        self.dash_distance = dash_distance
        self.trigger_range = trigger_range

        # DIRECTION
        self.direction = direction
        self.dir = 1 if direction == "right" else -1
        self.aim_player = aim_player

        # DASH CONTROL
        self.moved = 0

        # COOLDOWN
        self.cooldown_max = cooldown
        self.cooldown_timer = 0

        # FAKE DASH
        self.enable_fake = enable_fake
        self.fake_time = 30
        self.fake_timer = 0

        # ===== IMAGE =====
        frames = load_sprite_sheet("assets/trap/stone.png", 64, 62)
        self.image = frames[0]
        self.rect = pygame.Rect(x, 0, 40, 40)

        self.rect.bottom = 325
        self.start_x = x
    
    def draw(self, screen):
        draw_x = self.rect.x
        draw_y = self.rect.bottom - self.image.get_height()
        screen.blit(self.image, (draw_x, draw_y))

    def update(self, player):

        if self.state == self.IDLE:
            self.check_trigger(player)

        elif self.state == self.FAKE:
            self.fake()

        elif self.state == self.DASH:
            self.dash()

        elif self.state == self.COOLDOWN:
            self.cooldown()

    def check_trigger(self, player):

        dx = abs(player.rect.centerx - self.rect.centerx)
        dy = abs(player.rect.centery - self.rect.centery)

        if dx < self.trigger_range and dy < 40:

            # chọn hướng dash theo player
            if self.aim_player:
                if player.rect.centerx > self.rect.centerx:
                    self.dir = 1
                else:
                    self.dir = -1

            # fake dash
            if self.enable_fake:
                self.state = self.FAKE
                self.fake_timer = self.fake_time
            else:
                self.start_dash()

    def start_dash(self):
        self.state = self.DASH
        self.moved = 0

    def fake(self):

        self.fake_timer -= 1

        if self.fake_timer <= 0:
            self.start_dash()

    def dash(self):

        self.rect.x += self.speed * self.dir
        self.moved += abs(self.speed)

        if self.moved >= self.dash_distance:
            self.state = self.COOLDOWN
            self.cooldown_timer = self.cooldown_max

    def cooldown(self):

        # quay về vị trí ban đầu
        if abs(self.rect.x - self.start_x) > self.speed:

            if self.rect.x > self.start_x:
                self.rect.x -= self.speed
            else:
                self.rect.x += self.speed

        else:
            self.rect.x = self.start_x
            self.cooldown_timer -= 1

            if self.cooldown_timer <= 0:
                self.state = self.IDLE