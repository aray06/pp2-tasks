import pygame
import os
from clock import get_time_angles

# Инициализация Pygame
pygame.init()
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mickey's Clock")
clock = pygame.time.Clock()

# Настройка путей к изображениям
current_dir = os.path.dirname(__file__)
image_dir = os.path.join(current_dir, 'images')

# Загрузка фона и руки Микки
background = pygame.image.load(os.path.join(image_dir, 'mickeyclock.jpeg'))
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

hand_surf = pygame.image.load(os.path.join(image_dir, 'mickey_hand.png')).convert_alpha()
# Подбери размер руки под свой фон (например, 50x300)
hand_surf = pygame.transform.scale(hand_surf, (60, 320))

def blit_rotate_center(surf, image, center, angle):
    """
    Вращает изображение вокруг его центра и рисует на экране.
    """
    rotated_image = pygame.transform.rotate(image, angle)
    # Выравниваем центр нового (изменившегося в размере) прямоугольника с центром экрана
    new_rect = rotated_image.get_rect(center=image.get_rect(center=center).center)
    surf.blit(rotated_image, new_rect)

# Главный цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 1. Получаем углы из clock.py
    min_angle, sec_angle = get_time_angles()

    # 2. Отрисовка фона
    screen.blit(background, (0, 0))

    # 3. Отрисовка стрелок (центр 400x400)
    # Минутная стрелка (правая)
    blit_rotate_center(screen, hand_surf, (WIDTH // 2, HEIGHT // 2), min_angle)
    
    # Секундная стрелка (левая)
    blit_rotate_center(screen, hand_surf, (WIDTH // 2, HEIGHT // 2), sec_angle)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()