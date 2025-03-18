import pygame
from unittest.mock import patch, MagicMock
from gameplay import load_road_image, WIDTH, HEIGHT


def test_load_road_image_exists():
    mock_surface = MagicMock(spec=pygame.Surface)  # Створюємо фейковий Surface
    with patch("pygame.image.load", return_value=mock_surface):
        with patch("pygame.transform.scale", return_value=mock_surface) as mock_scale:
            result = load_road_image("Highway.png")
            assert result == mock_surface
            mock_scale.assert_called_once_with(mock_surface, (WIDTH, HEIGHT))


def test_load_road_image_not_exists():
    with patch("pygame.image.load", side_effect=FileNotFoundError):
        result = load_road_image("NonExistentRoad.png")
        assert isinstance(result, pygame.Surface)
