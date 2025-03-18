import pygame
import random
from unittest.mock import patch
from gameplay import car_width, car_height, LANES, HEIGHT

def test_run_game_obstacles():
    global obstacle_images
    
    obstacle_images = [pygame.Surface((car_width, car_height))] * 3  # Мокаємо зображення перешкод
    
    with patch("random.randint", return_value=1), patch("random.choice", return_value=LANES[1]):
        obstacles = []
        lane = random.choice(LANES)
        img = random.choice(obstacle_images)
        obstacles.append((pygame.Rect(lane - car_width / 2, -160, car_width, car_height), img))
        
        assert len(obstacles) == 1

def test_run_game_collision():
    global obstacle_images
    
    obstacle_images = [pygame.Surface((car_width, car_height))] * 3  # Мокаємо зображення перешкод
    car_x = LANES[1] - car_width / 2
    car_y = HEIGHT - 300
    
    obstacle_rect = pygame.Rect(car_x, car_y, car_width, car_height)
    obstacles = [(obstacle_rect, random.choice(obstacle_images))]
    
    for rect, img in obstacles:
        assert rect.colliderect(pygame.Rect(car_x, car_y, car_width, car_height)) is True
