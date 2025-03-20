from unittest.mock import patch, MagicMock
from gameplay import show_score, WHITE


def test_show_score():
    mock_font = MagicMock()
    mock_font.render.return_value = "mocked_text"
    mock_screen = MagicMock()

    with patch("gameplay.font", mock_font), patch("gameplay.screen", mock_screen):
        show_score(50)

        mock_font.render.assert_called_once_with("Score: 50", True, WHITE)
        mock_screen.blit.assert_called_once_with("mocked_text", (10, 10))
