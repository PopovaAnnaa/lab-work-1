import pygame
import json
import sys
import os

pygame.init()

WIDTH, HEIGHT = 1000, 800 
screen = pygame.display.set_mode((WIDTH, HEIGHT)) 
pygame.display.set_caption("Car Customization")

font = pygame.font.Font("fonts/Minecraft.ttf", 40)
small_font = pygame.font.Font("fonts/Minecraft.ttf", 30)

WHITE = (255, 255, 255)
GRAY = (170, 170, 170)
BLACK = (0, 0, 0)

CAR_ASSETS_PATH = os.path.join("assets", "cars")
ROAD_ASSETS_PATH = os.path.join("assets", "roads")

skins = ["cars1.png", "cars2.png", "cars3.png"]
skin_costs = {"cars1.png": 0, "cars2.png": 10, "cars3.png": 20}
roads = ["road1.png", "road2.png", "road3.png"]

def load_customization_data():
    try:
        with open("customization_data.json", "r") as file:
            data = json.load(file)
            if "selected_road" not in data:
                data["selected_road"] = "road1.png"
            return data
    except FileNotFoundError:
        return {"selected_skin": "cars1.png", "selected_road": "road1.png"}

def save_customization_data(data):
    with open("customization_data.json", "w") as file:
        json.dump(data, file)

def load_game_data():
    try:
        with open("game_data.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"score": 0, "highscore": 0}

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

def scale_image_to_width(image, width):
    original_width, original_height = image.get_size()
    new_height = int((width / original_width) * original_height)
    return pygame.transform.scale(image, (width, new_height))

def customization_screen():
    global screen
    customization_data = load_customization_data()
    game_data = load_game_data()

    unlocked_skins = ["cars1.png"]
    if game_data["highscore"] >= 10:
        unlocked_skins.append("cars2.png")
    if game_data["highscore"] >= 20:
        unlocked_skins.append("cars3.png")

    selected_skin = customization_data["selected_skin"]
    selected_road = customization_data["selected_road"]

    car_images = {skin: pygame.image.load(os.path.join(CAR_ASSETS_PATH, skin)) for skin in skins}
    road_images = {road: pygame.image.load(os.path.join(ROAD_ASSETS_PATH, road)) for road in roads}

    running = True
    while running:
        screen.fill(WHITE)
        mx, my = pygame.mouse.get_pos()

        draw_text("Car Customization", font, BLACK, screen, (WIDTH//2)-150 , 50)

        back_button = pygame.Rect(50, 650, 150, 60)
        pygame.draw.rect(screen, GRAY if back_button.collidepoint((mx, my)) else BLACK, back_button)
        draw_text("Back", small_font, WHITE, screen, back_button.centerx, back_button.centery)

        y_offset = 100
        car_button_height = 60
        car_spacing = 100 
        for skin in unlocked_skins:
            button = pygame.Rect(300, y_offset + 15, 250, 80)
            pygame.draw.rect(screen, BLACK if skin != selected_skin else (19, 207, 19), button)
            car_image = scale_image_to_width(car_images[skin], car_button_height)
            screen.blit(car_image, (100, y_offset))
            draw_text(f"{skin.split('.')[0]} - {skin_costs[skin]} pts", small_font, WHITE, screen, button.centerx, button.centery)
            y_offset += car_button_height + car_spacing

        road_y_offset = 100
        for road in roads:
            road_button = pygame.Rect(900, road_y_offset, 200, 80)
            pygame.draw.rect(screen, BLACK if road != selected_road else (19, 207, 19), road_button)
            draw_text(road.split('.')[0], small_font, WHITE, screen, road_button.centerx, road_button.centery)
            road_y_offset += 120

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
                    y_offset += car_button_height + car_spacing

                road_y_offset = 100
                for road in roads:
                    road_button = pygame.Rect(900, road_y_offset, 200, 80)
                    if road_button.collidepoint((mx, my)):
                        selected_road = road
                        customization_data["selected_road"] = road
                        save_customization_data(customization_data)
                    road_y_offset += 120

        draw_text("Road Customization", font, BLACK, screen, WIDTH-100 , 50)

        road_x, road_y = 650, 90
        for road in roads:

            road_image = pygame.transform.scale(road_images[road], (120, 80))  # Розмір картинки
            screen.blit(road_image, (road_x + 15, road_y + 10))  # Відображаємо картинку на екрані
            
            road_y += 120  # Відступ між елементами

        pygame.display.flip()

if __name__ == "__main__":
    customization_screen()
