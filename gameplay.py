import pygame
import random
import json
import os


pygame.init()

WIDTH, HEIGHT = 800, 600
LANES = [WIDTH // 5, WIDTH // 5 * 2, WIDTH // 5 * 3, WIDTH // 5 * 4]
screen = pygame.display.set_mode((WIDTH, HEIGHT))

bg1 = pygame.image.load("assets/roads/road1.png")
bg1 = pygame.transform.scale(bg1, (WIDTH, HEIGHT))
bg_y1 = 0
bg_y2 = -HEIGHT

pygame.display.set_caption("Car Racing Game")

WHITE = (255, 255, 255)
clock = pygame.time.Clock()
FPS = 60

# Зчитування даних з json
def load_game_data():
    if not os.path.exists("game_data.json") or os.path.getsize("game_data.json") == 0:
        return {"score": 0, "highscore": 0}
    try:
        with open("game_data.json", "r") as file:
            return json.load(file)
    except Exception as e:
        print(f"Error: {e}")
        return {"score": 0, "highscore": 0}

def load_customization_data():
    if not os.path.exists("customization_data.json") or os.path.getsize("customization_data.json") == 0:
        return {"selected_skin": "cars1.png"}
    try:
        with open("customization_data.json", "r") as file:
            return json.load(file)
    except Exception as e:
        print(f"Error: {e}")
        return {"selected_skin": "cars1.png"}

# Функция сохранения данных
def save_game_data(data):
    try:
        with open("game_data.json", "w") as file:
            json.dump(data, file)
    except Exception as e:
        print(f"Error: {e}")

def save_customization_data(data):
    try:
        with open("customization_data.json", "w") as file:
            json.dump(data, file)
    except Exception as e:
        print(f"Error: {e}")

# Завантажуємо вибраний скин
game_data = load_game_data()
customization_data = load_customization_data()

# Загружаем изображение выбранного скина
car_image = pygame.image.load(os.path.join("assets/cars", customization_data["selected_skin"]))
car_image = pygame.transform.scale(car_image, (80, 160))

obstacle_images = [
    pygame.image.load("assets/cars/cars1.png"),
    pygame.image.load("assets/cars/cars2.png"),
    pygame.image.load("assets/cars/cars3.png")
]
obstacle_images = [pygame.transform.scale(img, (80, 160)) for img in obstacle_images]

font = pygame.font.SysFont(None, 36)

def show_score(score):
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

def draw_text(text, font, color, surface, x, y):
    """Функция для малювання тексту на екрані."""
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

def pause_menu():
    pause_running = True
    while pause_running:
        screen.fill(WHITE)
        draw_text("Paused", font, (0, 0, 0), screen, WIDTH // 2, HEIGHT // 4)
        draw_text("Press P to Resume or Q to Quit", font, (0, 0, 0), screen, WIDTH // 2, HEIGHT // 2)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    return "resume"
                if event.key == pygame.K_q:
                    return "quit"

def save_game_data_and_customization(score, highscore):
    game_data["score"] = score
    game_data["highscore"] = highscore
    save_game_data(game_data)

def run_game():
    global bg_y1, bg_y2, car_image, customization_data
    car_x = LANES[1] - 40
    car_y = HEIGHT - 200
    car_speed = 5
    max_speed = 15
    obstacle_speed = 7
    obstacles = []
    score = 0
    running = True

    highscore = game_data["highscore"]
    selected_skin = customization_data["selected_skin"]

    unlocked_skins = ["cars1.png"]  
    if highscore >= 10:
        unlocked_skins.append("cars2.png")
    if highscore >= 20:
        unlocked_skins.append("cars3.png")

    def update_car_image(selected_skin):
        car_image = pygame.image.load(os.path.join("assets/cars", selected_skin))
        car_image = pygame.transform.scale(car_image, (80, 160))
        return car_image

    def check_skin_update():
        global customization_data, car_image
        new_data = load_customization_data()
        if new_data["selected_skin"] != customization_data["selected_skin"]:
            customization_data = new_data
            car_image = update_car_image(customization_data["selected_skin"])
            print(f"Skin updated to: {customization_data['selected_skin']}")  

    while running:
        check_skin_update()  

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if score > highscore:
                    highscore = score
                    save_game_data_and_customization(score, highscore)
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                result = pause_menu()
                if result == "quit":
                    if score > highscore:
                        highscore = score
                    save_game_data_and_customization(score, highscore)
                    return
                elif result == "resume":
                    continue

        screen.fill(WHITE)

        screen.blit(bg1, (0, bg_y1))
        screen.blit(bg1, (0, bg_y2))
        bg_y1 += 5
        bg_y2 += 5

        if bg_y1 >= HEIGHT:
            bg_y1 = -HEIGHT
        if bg_y2 >= HEIGHT:
            bg_y2 = -HEIGHT

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            car_x = max(LANES[0] - 40, car_x - car_speed * 3)
        if keys[pygame.K_RIGHT]:
            car_x = min(LANES[-1] - 40, car_x + car_speed * 3)
        if keys[pygame.K_UP]:
            obstacle_speed = min(max_speed, obstacle_speed + 0.2)
        if keys[pygame.K_DOWN]:
            obstacle_speed = max(5, obstacle_speed - 0.2)

        car_y = HEIGHT - 200 + (max_speed - obstacle_speed) * 3

        if score >= 10 and "cars2.png" not in unlocked_skins:
            unlocked_skins.append("cars2.png")
            selected_skin = "cars2.png"
            car_image = update_car_image(selected_skin)
            save_customization_data({"selected_skin": selected_skin})

        if score >= 20 and "cars3.png" not in unlocked_skins:
            unlocked_skins.append("cars3.png")
            selected_skin = "cars3.png"
            car_image = update_car_image(selected_skin)
            save_customization_data({"selected_skin": selected_skin})

        if random.randint(1, 30) == 1:
            lane = random.choice(LANES)
            if all(abs(obstacle[0].x - lane) > 80 for obstacle in obstacles):
                img = random.choice(obstacle_images)
                obstacles.append((pygame.Rect(lane - 40, -160, 80, 160), img))

        for obstacle in obstacles[:]:
            rect, img = obstacle
            rect.y += obstacle_speed
            if rect.colliderect(pygame.Rect(car_x, car_y, 80, 160)):
                if score > highscore:
                    highscore = score
                save_game_data_and_customization(score, highscore)
                return
            if rect.y > HEIGHT:
                obstacles.remove(obstacle)
                score += 1

        screen.blit(car_image, (car_x, car_y))

        for rect, img in obstacles:
            screen.blit(img, (rect.x, rect.y))

        show_score(score)

        pygame.display.flip()
        clock.tick(FPS)
