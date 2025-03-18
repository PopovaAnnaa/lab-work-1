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


def load_json_data(filename, default_data):
    if not os.path.exists(filename) or os.path.getsize(filename) == 0:
        return default_data
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except Exception as e:
        print(f"Помилка завантаження {filename}: {e}")
        return default_data


game_data = load_json_data("game_data.json", {"score": 0, "highscore": 0})
customization_data = load_json_data("customization_data.json", {"selected_skin": "Basic.png", "selected_road": "Highway.png"})


def load_road_image(road_name):
    path = os.path.join("assets", "roads", road_name)
    if os.path.exists(path):
        return pygame.transform.scale(pygame.image.load(path), (WIDTH, HEIGHT))
    return pygame.Surface((WIDTH, HEIGHT))


selected_road = customization_data.get("selected_road", "Highway.png")
bg1 = load_road_image(selected_road)
bg2 = load_road_image(selected_road)

bg_y1 = 0
bg_y2 = -HEIGHT

car_width, car_height = 120, 240

car_image = pygame.image.load(os.path.join("assets/cars", customization_data["selected_skin"]))
car_image = pygame.transform.scale(car_image, (car_width, car_height))

obstacle_images = [
    pygame.image.load("assets/cars/cars3.png"),
    pygame.image.load("assets/cars/cars4.png"),
    pygame.image.load("assets/cars/cars5.png")
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


def save_customization_data():
    with open("customization_data.json", "w") as file:
        json.dump(customization_data, file)


def update_car_image(selected_skin):
    car_image = pygame.image.load(os.path.join("assets/cars", selected_skin))
    car_image = pygame.transform.scale(car_image, (120, 240))
    return car_image


def update_skin_and_road():
    global car_image, bg1, bg2, selected_road, customization_data
    new_data = load_json_data("customization_data.json", customization_data)

    if new_data["selected_skin"] != customization_data["selected_skin"]:
        customization_data["selected_skin"] = new_data["selected_skin"]
        car_image = update_car_image(customization_data["selected_skin"])

    if new_data["selected_road"] != selected_road:
        selected_road = new_data["selected_road"]
        bg1 = load_road_image(selected_road)
        bg2 = load_road_image(selected_road)


def run_game():
    global bg_y1, bg_y2, car_image, customization_data, bg1, bg2, selected_road

    car_x = LANES[1] - car_width / 2
    car_speed = 5
    max_speed = 15
    obstacle_speed = 7
    obstacles = []
    score = 0
    running = True

    highscore = game_data["highscore"]

    unlocked_skins = ["Basic.png"]
    if highscore >= 10:
        unlocked_skins.append("Striker.png")
    if highscore >= 20:
        unlocked_skins.append("Wrecker.png")

    while running:
        update_skin_and_road()

        if score >= 10 and "Striker.png" not in unlocked_skins:
            unlocked_skins.append("Striker.png")
            customization_data["selected_skin"] = "Striker.png"
            car_image = update_car_image(customization_data["selected_skin"])
            save_game_data(score, highscore)
            save_customization_data()

        if score >= 20 and "Wrecker.png" not in unlocked_skins:
            unlocked_skins.append("Wrecker.png")
            customization_data["selected_skin"] = "Wrecker.png"
            car_image = update_car_image(customization_data["selected_skin"])
            save_game_data(score, highscore)
            save_customization_data()

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
            car_x = max(LANES[0] - car_width / 2, car_x - car_speed * 3)
        if keys[pygame.K_RIGHT]:
            car_x = min(LANES[-1] - car_width / 2, car_x + car_speed * 3)
        if keys[pygame.K_UP]:
            obstacle_speed = min(max_speed, obstacle_speed + 0.2)
        if keys[pygame.K_DOWN]:
            obstacle_speed = max(5, obstacle_speed - 0.2)

        car_y = HEIGHT - 300 + (max_speed - obstacle_speed) * 3

        if random.randint(1, 30) == 1:
            lane = random.choice(LANES)
            if all(abs(obstacle[0].x - lane) > 80 for obstacle in obstacles):
                img = random.choice(obstacle_images)
                obstacles.append((pygame.Rect(lane - car_width / 2, -160, car_width, car_height), img))

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
