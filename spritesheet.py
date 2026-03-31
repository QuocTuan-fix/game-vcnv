import pygame

def load_sprite_sheet(path, frame_width, frame_height):

    sheet = pygame.image.load(path).convert_alpha()
    frames = []

    sheet_width = sheet.get_width()
    sheet_height = sheet.get_height()

    for y in range(0, sheet_height, frame_height):
        for x in range(0, sheet_width, frame_width):

            if x + frame_width <= sheet_width and y + frame_height <= sheet_height:
                frame = sheet.subsurface((x, y, frame_width, frame_height))
                frames.append(frame)

    return frames