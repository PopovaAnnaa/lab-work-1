import pygame
from car_customization import scale_image_to_width


def test_scale_image_to_width():
    pygame.init()
    original_image = pygame.Surface((200, 100))  # 200x100 px
    new_width = 100

    scaled_image = scale_image_to_width(original_image, new_width)

    assert scaled_image.get_width() == new_width
    assert scaled_image.get_height() == 50  # Maintaining aspect ratio
