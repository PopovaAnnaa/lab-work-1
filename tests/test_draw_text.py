import pygame
from unittest.mock import MagicMock
from car_customization import draw_text, WHITE


def test_draw_text(mocker):
    mock_font = MagicMock()
    mock_surface = MagicMock()
    mock_surface.get_rect.return_value = pygame.Rect(100, 200, 50, 20)
    mock_font.render.return_value = mock_surface

    mock_screen = MagicMock()

    draw_text("Test Text", mock_font, WHITE, mock_screen, 100, 200)

    mock_font.render.assert_called_once_with("Test Text", True, WHITE)
    mock_screen.blit.assert_called_once_with(mock_surface, mocker.ANY)
