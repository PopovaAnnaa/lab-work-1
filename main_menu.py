import pygame
import sys
from car_customization import customization_screen

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Main Menu")

WHITE = (255, 255, 255)
GRAY = (170, 170, 170)
BLACK = (0, 0, 0)

play_img = pygame.image.load("assets/menu buttons/large buttons/Play Button.png")
settings_img = pygame.image.load("assets/menu buttons/large buttons/Settings Button.png")
quit_img = pygame.image.load("assets/menu buttons/large buttons/Quit Button.png")

play_img = pygame.transform.scale(play_img, (200, 60))
settings_img = pygame.transform.scale(settings_img, (200, 60))
quit_img = pygame.transform.scale(quit_img, (200, 60))

def show_menu():
    while True:
        screen.fill(WHITE)
        mx, my = pygame.mouse.get_pos()

        play_button = pygame.Rect(300, 200, 200, 60)
        settings_button = pygame.Rect(300, 300, 200, 60)
        quit_button = pygame.Rect(300, 400, 200, 60)

        # Подсветка кнопок при наведении (опционально)
        if play_button.collidepoint((mx, my)):
            pygame.draw.rect(screen, GRAY, play_button, border_radius=10)
        if settings_button.collidepoint((mx, my)):
            pygame.draw.rect(screen, GRAY, settings_button, border_radius=10)
        if quit_button.collidepoint((mx, my)):
            pygame.draw.rect(screen, GRAY, quit_button, border_radius=10)

        # Отображение изображений
        screen.blit(play_img, (300, 200))
        screen.blit(settings_img, (300, 300))
        screen.blit(quit_img, (300, 400))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint((mx, my)):
                    return "play"
                if settings_button.collidepoint((mx, my)):   
                    customization_screen()  # Відкриває екран кастомізації
                if quit_button.collidepoint((mx, my)):
                    return "quit"

        pygame.display.flip()
