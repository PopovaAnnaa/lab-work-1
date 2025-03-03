import pygame
import sys
import json
from car_customization import customization_screen

pygame.init()

WIDTH, HEIGHT = 1250, 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car Racing")

try:
    large_font = pygame.font.Font("fonts/Minecraft.ttf", 60)
    medium_font = pygame.font.Font("fonts/Minecraft.ttf", 40)
    small_font = pygame.font.Font("fonts/Minecraft.ttf", 30)
except IOError:
    print("Font not found, using default font.")
    font = pygame.font.Font(None, 50)  

WHITE = (255, 255, 255)
GRAY = (170, 170, 170)
BLACK = (0, 0, 0)

def read_highscore():
    try:
        with open("game_data.json", "r") as file:
            data = json.load(file)
            return data.get("highscore", 0)
    except (FileNotFoundError, json.JSONDecodeError):
        return 0

def save_highscore(score):
    try:
        with open("game_data.json", "w") as file:
            json.dump({"highscore": score}, file)
    except IOError:
        print("Error saving highscore.")

def draw_button(text, x, y, width, height):
    mx, my = pygame.mouse.get_pos()
    button_rect = pygame.Rect(x, y, width, height)
    color = GRAY if button_rect.collidepoint((mx, my)) else BLACK
    pygame.draw.rect(screen, color, button_rect)
    
    text_surf = small_font.render(text, True, WHITE)
    text_rect = text_surf.get_rect(center=button_rect.center)
    screen.blit(text_surf, text_rect)
    
    return button_rect

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

def show_menu():
    highscore = read_highscore()
    
    while True:
        screen.fill(WHITE)
        
        button_width, button_height = 200, 60
        center_x = (WIDTH - button_width) // 2  
        
        draw_text("Car Racing", large_font, BLACK, screen, WIDTH / 2, 100)

        play_button = draw_button("Play", center_x, 300, button_width, button_height)
        settings_button = draw_button("Settings", center_x, 400, button_width, button_height)
        quit_button = draw_button("Quit", center_x, 500, button_width, button_height)
        
        highscore_text = f"Highscore: {highscore}"
        highscore_surf = medium_font.render(highscore_text, True, BLACK)
        screen.blit(highscore_surf, (WIDTH // 2 - highscore_surf.get_width() // 2, 180))

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