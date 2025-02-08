import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
LANES = [WIDTH // 5, WIDTH // 5 * 2, WIDTH // 5 * 3, WIDTH // 5 * 4]
screen = pygame.display.set_mode((WIDTH, HEIGHT))

bg1 = pygame.image.load("assets/roads/road1.png")
bg1 = pygame.transform.scale(bg1, (WIDTH, HEIGHT))
bg_y1, bg_y2 = 0, -HEIGHT

WHITE, BLACK, RED = (255, 255, 255), (0, 0, 0), (255, 0, 0)
font = pygame.font.SysFont(None, 36)

clock = pygame.time.Clock()
FPS = 60

car_image = pygame.image.load("assets/cars/car1.png")
car_image = pygame.transform.scale(car_image, (80, 160))

car_x, car_y = LANES[1] - 40, HEIGHT - 200
car_speed, obstacle_speed, max_speed = 5, 7, 15

obstacle_images = [
    pygame.image.load("assets/cars/car2.png"),
    pygame.image.load("assets/cars/car3.png"),
]
obstacle_images = [pygame.transform.scale(img, (80, 160)) for img in obstacle_images]

def show_score(score):
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

def paused():
    while True:
        screen.fill(WHITE)
        text = font.render("Game Paused. Press ESC to Resume.", True, BLACK)
        screen.blit(text, (200, 250))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def game_over():
    while True:
        screen.fill(WHITE)
        text1 = font.render("Game Over!", True, RED)
        text2 = font.render("Press R to Restart or M for Main Menu", True, BLACK)
        screen.blit(text1, (350, 250))
        screen.blit(text2, (200, 300))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    main_game()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def main_game():
    global car_x, bg_y1, bg_y2, obstacle_speed
    score = 0
    obstacles = []
    running = True

    while running:
        screen.fill(WHITE)
        screen.blit(bg1, (0, bg_y1))
        screen.blit(bg1, (0, bg_y2))

        bg_y1 += 5
        bg_y2 += 5

        if bg_y1 >= HEIGHT:
            bg_y1 = -HEIGHT
        if bg_y2 >= HEIGHT:
            bg_y2 = -HEIGHT

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                paused()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            car_x = max(LANES[0] - 40, car_x - car_speed * 3)
        if keys[pygame.K_RIGHT]:
            car_x = min(LANES[-1] - 40, car_x + car_speed * 3)

        car_y = HEIGHT - 200

        if random.randint(1, 30) == 1:
            lane = random.choice(LANES)
            if all(abs(obstacle[0].x - lane) > 80 for obstacle in obstacles):
                img = random.choice(obstacle_images)
                obstacles.append((pygame.Rect(lane - 40, -160, 80, 160), img))

        for obstacle in obstacles[:]:
            rect, img = obstacle
            rect.y += obstacle_speed
            if rect.colliderect(pygame.Rect(car_x, car_y, 80, 160)):
                game_over()
            if rect.y > HEIGHT:
                obstacles.remove(obstacle)
                score += 1

        screen.blit(car_image, (car_x, car_y))

        for rect, img in obstacles:
            screen.blit(img, (rect.x, rect.y))

        show_score(score)

        pygame.display.flip()
        clock.tick(FPS)
