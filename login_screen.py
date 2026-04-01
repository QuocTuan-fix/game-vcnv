import pygame
from firebase_manager import login_user, register_user

def login_screen(screen):

    font = pygame.font.SysFont(None, 40)

    username = ""
    password = ""
    typing_password = False
    message = ""   # ⭐ thông báo lỗi

    while True:
        screen.fill((30,30,30))

        u_text = font.render("User: " + username, True, (255,255,255))
        p_text = font.render("Pass: " + ("*"*len(password)), True, (255,255,255))
        msg_text = font.render(message, True, (255,100,100))

        screen.blit(u_text, (200,150))
        screen.blit(p_text, (200,200))
        screen.blit(msg_text, (150,260))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_TAB:
                    typing_password = not typing_password

                elif event.key == pygame.K_RETURN:

                    user = login_user(username, password)

                    if user:
                        return username, user

                    else:
                        # check user tồn tại chưa
                        existing = login_user(username, password)

                        if existing is None:
                            # thử register
                            register_user(username, password)
                            return username, login_user(username, password)

                        # ⭐ sai mật khẩu
                        message = "Sai mat khau, vui long nhap lai!"
                        password = ""

                elif event.key == pygame.K_BACKSPACE:
                    if typing_password:
                        password = password[:-1]
                    else:
                        username = username[:-1]

                else:
                    if typing_password:
                        password += event.unicode
                    else:
                        username += event.unicode

        pygame.display.flip()