import pygame
from utils import resource_path
class UIOverlay:

    def __init__(self):

        self.font = pygame.font.SysFont(None, 28)

        # ===== LOAD ICON =====
        self.sound_on_img = pygame.image.load(resource_path("assets/sounds/soundon.png")).convert_alpha()
        self.sound_off_img = pygame.image.load(resource_path("assets/sounds/soundoff.png")).convert_alpha()
        self.help_img = pygame.image.load(resource_path("assets/sounds/help.png")).convert_alpha()

        # scale gốc
        self.base_size = 40

        # trạng thái
        self.sound_on = True
        self.show_help = False

        # animation scale
        self.sound_scale = 1.0
        self.help_scale = 1.0

        # rect
        self.sound_rect = pygame.Rect(10, 10, 40, 40)
        self.help_rect = pygame.Rect(60, 10, 40, 40)

    # =========================
    # EVENT
    # =========================
    def handle_event(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:

            if self.sound_rect.collidepoint(event.pos):
                self.sound_on = not self.sound_on

                # click animation
                self.sound_scale = 0.8

                if self.sound_on:
                    pygame.mixer.music.set_volume(0.5)
                else:
                    pygame.mixer.music.set_volume(0)

            if self.help_rect.collidepoint(event.pos):
                self.show_help = not self.show_help

                # click animation
                self.help_scale = 0.8

    # =========================
    # UPDATE ANIMATION
    # =========================
    def update(self):

        mouse = pygame.mouse.get_pos()

        # ===== SOUND BUTTON =====
        if self.sound_rect.collidepoint(mouse):
            target = 1.2
        else:
            target = 1.0

        self.sound_scale += (target - self.sound_scale) * 0.2

        # ===== HELP BUTTON =====
        if self.help_rect.collidepoint(mouse):
            target = 1.2
        else:
            target = 1.0

        self.help_scale += (target - self.help_scale) * 0.2

    # =========================
    # DRAW
    # =========================
    def draw(self, screen):

        # ===== SOUND ICON =====
        size = int(self.base_size * self.sound_scale)
        # chọn icon theo trạng thái
        if self.sound_on:
            icon = self.sound_on_img
        else:
            icon = self.sound_off_img

        img = pygame.transform.smoothscale(icon, (size, size))

        rect = img.get_rect(center=self.sound_rect.center)
        screen.blit(img, rect)

        # ===== HELP ICON =====
        size = int(self.base_size * self.help_scale)
        img = pygame.transform.smoothscale(self.help_img, (size, size))

        rect = img.get_rect(center=self.help_rect.center)
        screen.blit(img, rect)

        # ===== HELP PANEL =====
        if self.show_help:

            panel = pygame.Surface((400, 250))
            panel.set_alpha(230)
            panel.fill((20,20,20))

            screen.blit(panel, (200,100))

            lines = [
                "A / LEFT  : Move Left",
                "D / RIGHT : Move Right",
                "SPACE     : Jump",
                "R         : Restart",
                "ESC       : Menu",
                "L         : Leaderboard"
            ]

            for i, line in enumerate(lines):
                txt = self.font.render(line, True, (255,255,255))
                screen.blit(txt, (220, 120 + i*30))