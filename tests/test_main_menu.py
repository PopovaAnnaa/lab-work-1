import pygame
import json
from unittest.mock import patch, mock_open, MagicMock
import main_menu
import threading


def test_read_highscore():
    mock_data = json.dumps({"highscore": 100})
    with patch("builtins.open", mock_open(read_data=mock_data)):
        assert main_menu.read_highscore() == 100

    with patch("builtins.open", side_effect=FileNotFoundError):
        assert main_menu.read_highscore() == 0

    with patch("builtins.open", mock_open(read_data="invalid json")):
        assert main_menu.read_highscore() == 0


def test_save_highscore():
    with patch("builtins.open", mock_open()) as mocked_file:
        main_menu.save_highscore(200)
        mocked_file.assert_called_once_with("game_data.json", "w")
        mocked_file().write.assert_called()


def test_draw_button():
    pygame.init()
    with patch("pygame.mouse.get_pos", return_value=(50, 50)):
        button_rect = main_menu.draw_button("Test", 40, 40, 20, 20)
        assert isinstance(button_rect, pygame.Rect)


def test_draw_text():
    pygame.init()
    screen = pygame.display.set_mode((100, 100))
    font = pygame.font.Font(None, 30)
    main_menu.draw_text("Hello", font, (255, 255, 255), screen, 50, 50)


def test_show_menu():
    with patch.object(main_menu, "read_highscore", return_value=150), \
            patch("pygame.init"), \
            patch("pygame.display.set_mode"), \
            patch("pygame.display.flip"), \
            patch("pygame.event.get", side_effect=[
                [MagicMock(type=pygame.QUIT)],  # Перша подія QUIT
                []  # Порожній список завершить цикл
            ]), \
            patch("pygame.quit"), \
            patch("sys.exit") as mock_exit:
        thread = threading.Thread(target=main_menu.show_menu)
        thread.start()
        thread.join(timeout=2)  # Чекаємо 2 секунди

        assert not thread.is_alive(), "show_menu() не завершився!"
        mock_exit.assert_called_once()