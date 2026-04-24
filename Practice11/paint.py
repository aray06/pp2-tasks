import pygame
import math

# Инициализация
pygame.init()

# Настройки окна
WIDTH, HEIGHT = 900, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint Practice 11 - Geometry Pro")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (220, 220, 220)
COLORS = [BLACK, (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255)]

# Состояние кисти
active_color = BLACK
# ЗАДАНИЕ: Добавлены новые инструменты
active_tool = 'brush' # brush, eraser, square, right_tri, equ_tri, rhombus
drawing = False
start_pos = None

screen.fill(WHITE)

def draw_ui():
    """Отрисовка панели управления с кнопками"""
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, 60))
    pygame.draw.line(screen, BLACK, (0, 60), (WIDTH, 60), 2)

    # Палитра
    for i, color in enumerate(COLORS):
        rect = pygame.Rect(10 + i * 35, 15, 30, 30)
        pygame.draw.rect(screen, color, rect)
        if active_color == color:
            pygame.draw.rect(screen, WHITE, rect, 3)

    # Кнопки инструментов
    font = pygame.font.SysFont("Arial", 12)
    # ЗАДАНИЕ: Список инструментов расширен согласно условию
    tools = ["Brush", "Eraser", "Square", "Right_Tri", "Equ_Tri", "Rhombus"]
    for i, tool in enumerate(tools):
        rect = pygame.Rect(230 + i * 85, 15, 80, 30)
        bg_color = (170, 170, 170) if active_tool == tool.lower() else (200, 200, 200)
        pygame.draw.rect(screen, bg_color, rect)
        pygame.draw.rect(screen, BLACK, rect, 1)
        
        text = font.render(tool, True, BLACK)
        screen.blit(text, (235 + i * 85, 22))

def get_ui_click(pos):
    """Логика нажатия на кнопки меню"""
    global active_color, active_tool
    # Проверка палитры
    for i, color in enumerate(COLORS):
        if pygame.Rect(10 + i * 35, 15, 30, 30).collidepoint(pos):
            active_color = color
            return True
    # Проверка инструментов
    tools = ["brush", "eraser", "square", "right_tri", "equ_tri", "rhombus"]
    for i, tool in enumerate(tools):
        if pygame.Rect(230 + i * 85, 15, 80, 30).collidepoint(pos):
            active_tool = tool
            return True
    return False

run = True
while run:
    draw_ui()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.pos[1] < 60: # Если клик в зоне меню
                get_ui_click(event.pos)
            else:
                drawing = True
                start_pos = event.pos
        
        if event.type == pygame.MOUSEBUTTONUP:
            if drawing and start_pos and event.pos[1] > 60:
                end_pos = event.pos
                w = end_pos[0] - start_pos[0]
                h = end_pos[1] - start_pos[1]

                # ЗАДАНИЕ: Draw square (Квадрат - это прямоугольник с равными сторонами)
                if active_tool == 'square':
                    side = max(abs(w), abs(h))
                    # Корректируем координаты в зависимости от направления ведения мышки
                    s_x = start_pos[0] if w > 0 else start_pos[0] - side
                    s_y = start_pos[1] if h > 0 else start_pos[1] - side
                    pygame.draw.rect(screen, active_color, [s_x, s_y, side, side], 2)

                # ЗАДАНИЕ: Draw right triangle (Прямоугольный треугольник)
                elif active_tool == 'right_tri':
                    points = [start_pos, (start_pos[0], end_pos[1]), end_pos]
                    pygame.draw.polygon(screen, active_color, points, 2)

                # ЗАДАНИЕ: Draw equilateral triangle (Равносторонний треугольник)
                elif active_tool == 'equ_tri':
                    # Используем ширину как сторону, высоту вычисляем по формуле
                    side = w
                    height_tri = (math.sqrt(3) / 2) * side
                    points = [
                        (start_pos[0], start_pos[1]), # Левый угол
                        (start_pos[0] + side, start_pos[1]), # Правый угол
                        (start_pos[0] + side / 2, start_pos[1] - height_tri) # Вершина
                    ]
                    pygame.draw.polygon(screen, active_color, points, 2)

                # ЗАДАНИЕ: Draw rhombus (Ромб)
                elif active_tool == 'rhombus':
                    points = [
                        (start_pos[0] + w / 2, start_pos[1]),     # Верх
                        (start_pos[0] + w, start_pos[1] + h / 2), # Право
                        (start_pos[0] + w / 2, start_pos[1] + h), # Низ
                        (start_pos[0], start_pos[1] + h / 2)      # Лево
                    ]
                    pygame.draw.polygon(screen, active_color, points, 2)

            drawing = False
            start_pos = None

        # Рисование кистью и ластиком в реальном времени
        if event.type == pygame.MOUSEMOTION and drawing and event.pos[1] > 60:
            if active_tool == 'brush':
                pygame.draw.circle(screen, active_color, event.pos, 5)
            elif active_tool == 'eraser':
                pygame.draw.circle(screen, WHITE, event.pos, 20)

    pygame.display.flip()

pygame.quit()