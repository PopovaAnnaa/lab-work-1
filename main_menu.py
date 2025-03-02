import pygame
import sys
from car_customization import customization_screen

pygame.init()

WIDTH, HEIGHT = 1250, 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Main Menu")

try:
    font = pygame.font.Font("fonts/Minecraft.ttf", 30)
except IOError:
    print("Font not found, using default font.")
    font = pygame.font.Font(None, 50)  
    
WHITE = (255, 255, 255)
GRAY = (170, 170, 170)
BLACK = (0, 0, 0)

def draw_button(text, x, y, width, height):
    mx, my = pygame.mouse.get_pos()
    button_rect = pygame.Rect(x, y, width, height)
    color = GRAY if button_rect.collidepoint((mx, my)) else BLACK
    pygame.draw.rect(screen, color, button_rect, border_radius=10)
    
    text_surf = font.render(text, True, WHITE)
    text_rect = text_surf.get_rect(center=button_rect.center)
    screen.blit(text_surf, text_rect)
    
    return button_rect

def show_menu():
    while True:
        screen.fill(WHITE)
        
        button_width, button_height = 200, 60
        center_x = (WIDTH - button_width) // 2  

        play_button = draw_button("Play", center_x, 200, button_width, button_height)
        settings_button = draw_button("Settings", center_x, 300, button_width, button_height)
        quit_button = draw_button("Quit", center_x, 400, button_width, button_height)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):
                    return "play"
                if settings_button.collidepoint(event.pos):
                    customization_screen()
                if quit_button.collidepoint(event.pos):
                    return "quit"

        pygame.display.flip()
