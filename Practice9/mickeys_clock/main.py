import pygame
import os
from clock import get_angles, draw_rotated_hand

pygame.init()
W, H = 800, 800
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Mickey Clock - Small Hands")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 1. Загрузка фона
bg = pygame.image.load(os.path.join(BASE_DIR, 'images', 'image_2.png')).convert()
bg = pygame.transform.scale(bg, (W, H))

# 2. Загрузка и уменьшение рук (теперь они еще компактнее)
# Правая (минуты)
img_min = pygame.image.load(os.path.join(BASE_DIR, 'images', 'image_3.png')).convert_alpha()
img_min = pygame.transform.scale(img_min, (150, 150)) 
pivot_min = (12, 138) # Координата запястья для нового размера

# Левая (секунды)
img_sec = pygame.image.load(os.path.join(BASE_DIR, 'images', 'image_4.png')).convert_alpha()
img_sec = pygame.transform.scale(img_sec, (140, 140))
pivot_sec = (128, 128) # Координата запястья для нового размера

running = True
clock_timer = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    angle_min, angle_sec = get_angles()

    screen.blit(bg, (0, 0))
    center_mickey = (W // 2, H // 2)

    # Рисуем руки: сначала секунды, потом минуты
    draw_rotated_hand(screen, img_sec, center_mickey, pivot_sec, angle_sec)
    draw_rotated_hand(screen, img_min, center_mickey, pivot_min, angle_min)

    pygame.display.flip()
    clock_timer.tick(60)

pygame.quit()