import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Main Menu")

font = pygame.font.SysFont(None, 50)

WHITE = (255, 255, 255)
GRAY = (170, 170, 170)
BLACK = (0, 0, 0)

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

def show_menu():
    while True:
        screen.fill(WHITE)

        mx, my = pygame.mouse.get_pos()

        play_button = pygame.Rect(300, 200, 200, 60)
        quit_button = pygame.Rect(300, 300, 200, 60)

        pygame.draw.rect(screen, GRAY if play_button.collidepoint((mx, my)) else BLACK, play_button)
        pygame.draw.rect(screen, GRAY if quit_button.collidepoint((mx, my)) else BLACK, quit_button)

        draw_text("Play", font, WHITE, screen, 400, 230)
        draw_text("Quit", font, WHITE, screen, 400, 330)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint((mx, my)):
                    return "play"
                if quit_button.collidepoint((mx, my)):
                    return "quit"

        pygame.display.flip()
