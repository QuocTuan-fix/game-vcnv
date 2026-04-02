import pygame
from firebase_manager import login_user, register_user

def login_screen(screen):

    pygame.font.init()

    title_font = pygame.font.SysFont("arial", 60)
    font = pygame.font.SysFont("arial", 36)
    small_font = pygame.font.SysFont("arial", 26)

    username = ""
    password = ""

    active_input = "username"  # "username" hoặc "password"
    message = ""

    input_box_user = pygame.Rect(250, 180, 300, 40)
    input_box_pass = pygame.Rect(250, 260, 300, 40)

    while True:
        screen.fill((20, 20, 30))

        # ===== TITLE =====
        title = title_font.render("LOGIN", True, (255, 255, 0))
        screen.blit(title, (320, 80))

        # ===== DRAW BOX =====
        color_user = (0,255,0) if active_input == "username" else (200,200,200)
        color_pass = (0,255,0) if active_input == "password" else (200,200,200)

        pygame.draw.rect(screen, color_user, input_box_user, 2)
        pygame.draw.rect(screen, color_pass, input_box_pass, 2)

        # ===== TEXT =====
        user_text = font.render(username, True, (255,255,255))
        pass_text = font.render("*" * len(password), True, (255,255,255))

        screen.blit(user_text, (input_box_user.x + 10, input_box_user.y + 5))
        screen.blit(pass_text, (input_box_pass.x + 10, input_box_pass.y + 5))

        # ===== LABEL =====
        screen.blit(small_font.render("Username", True, (180,180,180)), (250, 150))
        screen.blit(small_font.render("Password", True, (180,180,180)), (250, 230))

        # ===== MESSAGE =====
        msg_surface = small_font.render(message, True, (255,100,100))
        screen.blit(msg_surface, (250, 320))

        # ===== HINT =====
        hint = small_font.render("ENTER = Login | TAB = Switch", True, (150,150,150))
        screen.blit(hint, (230, 380))

        # ===== EVENT =====
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return None

            if event.type == pygame.KEYDOWN:

                # chuyển ô
                if event.key == pygame.K_TAB:
                    active_input = "password" if active_input == "username" else "username"

                # login
                elif event.key == pygame.K_RETURN:

                    if username == "" or password == "":
                        message = "Vui long nhap day du!"
                        continue

                    user = login_user(username, password)

                    if user:
                        return username, user

                    else:
                        # check user tồn tại chưa (IMPORTANT)
                        existing_user = login_user(username, "___check___")

                        if existing_user is None:
                            # chưa có → tạo tài khoản
                            register_user(username, password)
                            message = "Da tao tai khoan!"
                            return username, login_user(username, password)
                        else:
                            # sai mật khẩu
                            message = "Sai mat khau, thu lai!"
                            password = ""

                # xoá ký tự
                elif event.key == pygame.K_BACKSPACE:
                    if active_input == "username":
                        username = username[:-1]
                    else:
                        password = password[:-1]

                # nhập ký tự
                else:
                    if event.unicode.isprintable():
                        if active_input == "username":
                            username += event.unicode
                        else:
                            password += event.unicode

        pygame.display.flip()