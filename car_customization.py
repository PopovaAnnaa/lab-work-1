import pygame
import sys
import json
import os

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car Customization")

font = pygame.font.SysFont(None, 40)
small_font = pygame.font.SysFont(None, 30)  # Менший шрифт для довгого тексту

WHITE = (255, 255, 255)
GRAY = (170, 170, 170)
BLACK = (0, 0, 0)

# Load data
DATA_FILE = "player_data.json"
def load_data():
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"score": 0, "selected_skin": "cars1.png"}

def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file)

data = load_data()

# Available skins
skins = ["cars1.png", "cars2.png", "cars3.png"]
skin_costs = {"cars1.png": 0, "cars2.png": 10, "cars3.png": 20}

CAR_ASSETS_PATH = os.path.join("assets", "cars")

# Load car images
car_images = {skin: pygame.image.load(os.path.join(CAR_ASSETS_PATH, skin)) for skin in skins}

def customization_screen():
    running = True
    selected_skin = data["selected_skin"]

    while running:
        screen.fill(WHITE)
        mx, my = pygame.mouse.get_pos()

        # Buttons
        back_button = pygame.Rect(50, 500, 150, 60)
        pygame.draw.rect(screen, GRAY if back_button.collidepoint((mx, my)) else BLACK, back_button)
        draw_text("Back", font, WHITE, screen, back_button.centerx, back_button.centery)

        save_button = pygame.Rect(550, 500, 200, 60)  # Збільшена кнопка
        pygame.draw.rect(screen, GRAY if save_button.collidepoint((mx, my)) else BLACK, save_button)
        draw_text("Save Changes", small_font, WHITE, screen, save_button.centerx, save_button.centery)  # Менший шрифт
        
        # Car selection
        y_offset = 100
        for skin in skins:
            button = pygame.Rect(300, y_offset, 250, 80)  # Ширші кнопки
            color = GRAY if skin_costs[skin] > data["score"] else BLACK
            pygame.draw.rect(screen, color if button.collidepoint((mx, my)) else BLACK, button)

            # Відображення машинки
            car_image = pygame.transform.scale(car_images[skin], (80, 80))
            screen.blit(car_image, (100, y_offset))

            # Відображення тексту праворуч
            draw_text(f"{skin.split('.')[0]} - {skin_costs[skin]} pts", font, WHITE, screen, button.centerx, button.centery)

            # Виділення вибраного скіна
            if skin == selected_skin:
                pygame.draw.rect(screen, (0, 255, 0), button, 5)

            y_offset += 120  # Відступ між кнопками

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint((mx, my)):
                    running = False
                if save_button.collidepoint((mx, my)):
                    save_data(data)
                y_offset = 100
                for skin in skins:
                    button = pygame.Rect(300, y_offset, 250, 80)
                    if button.collidepoint((mx, my)) and data["score"] >= skin_costs[skin]:
                        selected_skin = skin
                        data["selected_skin"] = skin
                        save_data(data)
                    y_offset += 120

        pygame.display.flip()

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

if __name__ == "__main__":
    customization_screen()
