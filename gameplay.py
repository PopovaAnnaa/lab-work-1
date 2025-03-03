import pygame
import random
import json
import os

pygame.init()

WIDTH, HEIGHT = 1250, 750
LANES = [WIDTH // 5, WIDTH // 5 * 2, WIDTH // 5 * 3, WIDTH // 5 * 4]
screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Car Racing Game")

WHITE = (255, 255, 255)
clock = pygame.time.Clock()
FPS = 60

# Функція для завантаження даних
def load_json_data(filename, default_data):
    if not os.path.exists(filename) or os.path.getsize(filename) == 0:
        return default_data
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except Exception as e:
        print(f"Помилка завантаження {filename}: {e}")
        return default_data

# Завантажуємо дані
game_data = load_json_data("game_data.json", {"score": 0, "highscore": 0})
customization_data = load_json_data("customization_data.json", {"selected_skin": "cars1.png", "selected_road": "road1.png"})

# Завантажуємо вибрану дорогу
def load_road_image(road_name):
    path = os.path.join("assets", "roads", road_name)
    if os.path.exists(path):
        return pygame.transform.scale(pygame.image.load(path), (WIDTH, HEIGHT))
    return pygame.Surface((WIDTH, HEIGHT))  # Порожній фон, якщо файлу немає

selected_road = customization_data.get("selected_road", "road1.png")
bg1 = load_road_image(selected_road)
bg2 = load_road_image(selected_road)

bg_y1 = 0
bg_y2 = -HEIGHT

car_width, car_height = 120, 240  # Розміри машини

# Завантаження машини
car_image = pygame.image.load(os.path.join("assets/cars", customization_data["selected_skin"]))
car_image = pygame.transform.scale(car_image, (car_width, car_height))

obstacle_images = [
    pygame.image.load("assets/cars/cars1.png"),
    pygame.image.load("assets/cars/cars2.png"),
    pygame.image.load("assets/cars/cars3.png")
]
obstacle_images = [pygame.transform.scale(img, (car_width, car_height)) for img in obstacle_images]

font = pygame.font.Font("fonts/Minecraft.ttf", 30)

def show_score(score):
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

def draw_text(text, font, color, surface, x, y):
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

def save_game_data(score, highscore):
    game_data["score"] = score
    game_data["highscore"] = highscore
    with open("game_data.json", "w") as file:
        json.dump(game_data, file)

def run_game():
    global bg_y1, bg_y2, car_image, customization_data, bg1, bg2, selected_road

    car_x = LANES[1] - car_width/2
    car_y = HEIGHT - 200
    car_speed = 5
    max_speed = 15
    obstacle_speed = 7
    obstacles = []
    score = 0
    running = True

    highscore = game_data["highscore"]

    def update_skin_and_road():
        """Оновлює скин та дорогу в реальному часі."""
        global car_image, bg1, bg2, selected_road
        new_data = load_json_data("customization_data.json", customization_data)

        if new_data["selected_skin"] != customization_data["selected_skin"]:
            customization_data["selected_skin"] = new_data["selected_skin"]
            car_image = pygame.image.load(os.path.join("assets/cars", customization_data["selected_skin"]))
            car_image = pygame.transform.scale(car_image, (car_width, car_height))
            print(f"Машинка оновлена: {customization_data['selected_skin']}")  

        if new_data["selected_road"] != selected_road:
            selected_road = new_data["selected_road"]
            bg1 = load_road_image(selected_road)
            bg2 = load_road_image(selected_road)
            print(f"Фон оновлений: {selected_road}")

    while running:
        update_skin_and_road()  

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if score > highscore:
                    highscore = score
                    save_game_data(score, highscore)
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                result = pause_menu()
                if result == "quit":
                    if score > highscore:
                        highscore = score
                    save_game_data(score, highscore)
                    return
                elif result == "resume":
                    continue

        screen.fill(WHITE)

        screen.blit(bg1, (0, bg_y1))
        screen.blit(bg2, (0, bg_y2))
        bg_y1 += 5
        bg_y2 += 5

        if bg_y1 >= HEIGHT:
            bg_y1 = -HEIGHT
        if bg_y2 >= HEIGHT:
            bg_y2 = -HEIGHT

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            car_x = max(LANES[0] - car_width/2, car_x - car_speed * 3)
        if keys[pygame.K_RIGHT]:
            car_x = min(LANES[-1] - car_width/2, car_x + car_speed * 3)
        if keys[pygame.K_UP]:
            obstacle_speed = min(max_speed, obstacle_speed + 0.2)
        if keys[pygame.K_DOWN]:
            obstacle_speed = max(5, obstacle_speed - 0.2)

        car_y = HEIGHT - 250 + (max_speed - obstacle_speed) * 3

        if random.randint(1, 30) == 1:
            lane = random.choice(LANES)
            if all(abs(obstacle[0].x - lane) > 80 for obstacle in obstacles):
                img = random.choice(obstacle_images)
                obstacles.append((pygame.Rect(lane - car_width/2, -160, car_width, car_height), img))

        for obstacle in obstacles[:]:
            rect, img = obstacle
            rect.y += obstacle_speed
            if rect.colliderect(pygame.Rect(car_x, car_y, 80, 160)):
                if score > highscore:
                    highscore = score
                save_game_data(score, highscore)
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
