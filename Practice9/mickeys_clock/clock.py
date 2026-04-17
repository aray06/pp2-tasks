import pygame
import datetime

# Поправки, чтобы выровнять руки по вертикали на 12 часов
OFFSET_MIN = -45   # Для правой руки (image_3)
OFFSET_SEC = -135  # Для левой руки (image_4)

def get_angles():
    now = datetime.datetime.now()
    
    # Секунды: 6 градусов за каждую секунду
    angle_sec = 90 - (now.second * 6) + OFFSET_SEC
    
    # Минуты: 6 градусов за каждую минуту
    angle_min = 90 - (now.minute * 6) + OFFSET_MIN
    
    return angle_min, angle_sec

def draw_rotated_hand(surf, image, center_pos, pivot, angle):
    """Функция вращения вокруг сустава (запястья)"""
    image_rect = image.get_rect()
    offset = pygame.math.Vector2(pivot[0] - image_rect.centerx, 
                                 pivot[1] - image_rect.centery)
    rotated_offset = offset.rotate(-angle)
    rotated_image = pygame.transform.rotate(image, angle)
    
    rotated_image_rect = rotated_image.get_rect(
        center=(center_pos[0] - rotated_offset.x, center_pos[1] - rotated_offset.y)
    )
    surf.blit(rotated_image, rotated_image_rect)