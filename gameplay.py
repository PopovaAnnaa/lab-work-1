import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
LANES = [WIDTH // 5, WIDTH // 5 * 2, WIDTH // 5 * 3, WIDTH // 5 * 4]  # 4 смуги
screen = pygame.display.set_mode((WIDTH, HEIGHT))

bg1 = pygame.image.load("images/roads/road1.png")
bg1 = pygame.transform.scale(bg1, (WIDTH, HEIGHT))
bg_y1 = 0
bg_y2 = -HEIGHT  # для створення ефекту руху дороги

pygame.display.set_caption("Car Racing Game")

WHITE = (255, 255, 255)

# годинник для контролю фпс
clock = pygame.time.Clock()
FPS = 60

car_image = pygame.image.load("images/cars/cars7.png")
car_image = pygame.transform.scale(car_image, (80, 160))

car_x = LANES[1] - 40  # початкова позиція на 2-й смузі
car_y = HEIGHT - 200
car_speed = 5
max_speed = 15

obstacle_images = [
    pygame.image.load("images/cars/cars1.png"),
    pygame.image.load("images/cars/cars2.png"),
    pygame.image.load("images/cars/cars3.png")
]
obstacle_images = [pygame.transform.scale(img, (80, 160)) for img in obstacle_images]

obstacle_speed = 7
obstacles = []  # список кортежів (прямокутник, зображення)

font = pygame.font.SysFont(None, 36)

# функція для відображення рахунку
def show_score(score):
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

def main():
    global car_x, bg_y1, bg_y2, obstacle_speed
    score = 0
    running = True

    while running:
        screen.fill(WHITE)

        # анімація руху дороги
        screen.blit(bg1, (0, bg_y1))
        screen.blit(bg1, (0, bg_y2))
        bg_y1 += 5
        bg_y2 += 5

        # перезапускаємо фонові зображення для безперервного руху
        if bg_y1 >= HEIGHT:
            bg_y1 = -HEIGHT
        if bg_y2 >= HEIGHT:
            bg_y2 = -HEIGHT

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            car_x = max(LANES[0] - 40, car_x - car_speed * 3)
        if keys[pygame.K_RIGHT]:
            car_x = min(LANES[-1] - 40, car_x + car_speed * 3)
        if keys[pygame.K_UP]:
            obstacle_speed = min(max_speed, obstacle_speed + 0.2)
        if keys[pygame.K_DOWN]:
            obstacle_speed = max(5, obstacle_speed - 0.2)

        # імітація руху: при прискоренні машина трохи піднімається, при гальмуванні - опускається
        car_y = HEIGHT - 200 + (max_speed - obstacle_speed) * 3

        if random.randint(1, 30) == 1:
            lane = random.choice(LANES)
            if all(abs(obstacle[0].x - lane) > 80 for obstacle in obstacles):
                img = random.choice(obstacle_images)
                obstacles.append((pygame.Rect(lane - 40, -160, 80, 160), img))

        for obstacle in obstacles[:]:
            rect, img = obstacle
            rect.y += obstacle_speed
            if rect.colliderect(pygame.Rect(car_x, car_y, 80, 160)):
                running = False
            if rect.y > HEIGHT:
                obstacles.remove(obstacle)
                score += 1
                
        screen.blit(car_image, (car_x, car_y))

        for rect, img in obstacles:
            screen.blit(img, (rect.x, rect.y))

        show_score(score)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
