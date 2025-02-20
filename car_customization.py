import pygame
import json
import sys
import os

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car Customization")
font = pygame.font.SysFont(None, 40)
small_font = pygame.font.SysFont(None, 30)
WHITE = (255, 255, 255)
GRAY = (170, 170, 170)
BLACK = (0, 0, 0)

CAR_ASSETS_PATH = os.path.join("assets", "cars")
skins = ["cars1.png", "cars2.png", "cars3.png"]
skin_costs = {"cars1.png": 0, "cars2.png": 10, "cars3.png": 20}

def load_customization_data():
    try:
        with open("customization_data.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"selected_skin": "cars1.png"}

def save_customization_data(data):
    with open("customization_data.json", "w") as file:
        json.dump(data, file)

def load_game_data():
    try:
        with open("game_data.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"score": 0, "highscore": 0}

def save_game_data(data):
    with open("game_data.json", "w") as file:
        json.dump(data, file)

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

def customization_screen():
    global screen, car_image, customization_data
    customization_data = load_customization_data()
    game_data = load_game_data()

    unlocked_skins = ["cars1.png"]  
    if game_data["highscore"] >= 10:  
        unlocked_skins.append("cars2.png")
    if game_data["highscore"] >= 20:  
        unlocked_skins.append("cars3.png")

    selected_skin = customization_data["selected_skin"]
    car_images = {skin: pygame.image.load(os.path.join(CAR_ASSETS_PATH, skin)) for skin in skins}

    running = True
    while running:
        screen.fill(WHITE)
        mx, my = pygame.mouse.get_pos()

        back_button = pygame.Rect(50, 500, 150, 60)
        pygame.draw.rect(screen, GRAY if back_button.collidepoint((mx, my)) else BLACK, back_button)
        draw_text("Back", font, WHITE, screen, back_button.centerx, back_button.centery)

        y_offset = 100
        for skin in unlocked_skins:
            button = pygame.Rect(300, y_offset, 250, 80)
            pygame.draw.rect(screen, GRAY if skin != selected_skin else (0, 255, 0), button)
            car_image = pygame.transform.scale(car_images[skin], (80, 80))
            screen.blit(car_image, (100, y_offset))
            draw_text(f"{skin.split('.')[0]} - {skin_costs[skin]} pts", font, WHITE, screen, button.centerx, button.centery)

            y_offset += 120

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint((mx, my)):
                    running = False

                y_offset = 100
                for skin in unlocked_skins:
                    button = pygame.Rect(300, y_offset, 250, 80)
                    if button.collidepoint((mx, my)):
                        selected_skin = skin
                        customization_data["selected_skin"] = skin
                        save_customization_data(customization_data)  
                        car_image = pygame.transform.scale(car_images[skin], (80, 160))  
                    y_offset += 120

        pygame.display.flip()