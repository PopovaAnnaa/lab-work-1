import pygame
from unittest.mock import patch
from gameplay import pause_menu

def test_pause_menu_resume():
    with patch("pygame.event.get", return_value=[pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_p})]):
        result = pause_menu()
        assert result == "resume"

def test_pause_menu_quit():
    with patch("pygame.event.get", return_value=[pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_q})]):
        result = pause_menu()
        assert result == "quit"
