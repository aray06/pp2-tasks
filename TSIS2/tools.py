import pygame
import math
import datetime
from collections import deque

def flood_fill(surface, x, y, new_color, ui_height):
    """Алгоритм заливки области (BFS)"""
    target_color = surface.get_at((x, y))
    if target_color == new_color:
        return
    
    width, height = surface.get_size()
    queue = deque([(x, y)])
    
    while queue:
        curr_x, curr_y = queue.popleft()
        if not (0 <= curr_x < width and ui_height <= curr_y < height):
            continue
        if surface.get_at((curr_x, curr_y)) != target_color:
            continue
            
        surface.set_at((curr_x, curr_y), new_color)
        queue.append((curr_x + 1, curr_y))
        queue.append((curr_x - 1, curr_y))
        queue.append((curr_x, curr_y + 1))
        queue.append((curr_x, curr_y - 1))

def save_canvas(surface):
    """Сохранение холста с временной меткой"""
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"paint_save_{timestamp}.png"
    pygame.image.save(surface, filename)
    print(f"Изображение сохранено как: {filename}")

def get_right_triangle_points(start, end):
    """Точки для прямоугольного треугольника"""
    return [start, (start[0], end[1]), end]

def get_equilateral_triangle_points(start, end):
    """Точки для равностороннего треугольника"""
    w = end[0] - start[0]
    h = (math.sqrt(3) / 2) * w
    return [start, (start[0] + w, start[1]), (start[0] + w/2, start[1] - h)]

def get_rhombus_points(start, end):
    """Точки для ромба"""
    w = end[0] - start[0]
    h = end[1] - start[1]
    return [
        (start[0] + w/2, start[1]),     # Верх
        (start[0] + w, start[1] + h/2), # Право
        (start[0] + w/2, start[1] + h), # Низ
        (start[0], start[1] + h/2)      # Лево
    ]