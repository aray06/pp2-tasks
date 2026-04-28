import pygame
from tools import (flood_fill, save_canvas, get_right_triangle_points, 
                   get_equilateral_triangle_points, get_rhombus_points)

# Инициализация
pygame.init()
WIDTH, HEIGHT = 1000, 800
UI_HEIGHT = 100
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint TSIS 2 - Pro")

# Цвета
WHITE, BLACK, GRAY = (255, 255, 255), (0, 0, 0), (210, 210, 210)
COLORS = [BLACK, (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255)]

# Состояния
active_color = BLACK
active_tool = 'brush'
active_size = 2
drawing = False
start_pos, last_pos, snapshot = None, None, None
text_buffer, text_pos = "", None

font = pygame.font.SysFont("Arial", 18)
font_bold = pygame.font.SysFont("Arial", 18, bold=True)
screen.fill(WHITE)

def draw_ui():
    """Отрисовка интерфейса"""
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, UI_HEIGHT))
    pygame.draw.line(screen, BLACK, (0, UI_HEIGHT), (WIDTH, UI_HEIGHT), 2)

    # Палитра
    for i, color in enumerate(COLORS):
        rect = pygame.Rect(10 + i * 35, 10, 30, 30)
        pygame.draw.rect(screen, color, rect)
        if active_color == color:
            pygame.draw.rect(screen, WHITE, rect, 3)

    # Кнопки инструментов
    tools = ["Brush", "Line", "Eraser", "Square", "Right_Tri", "Equ_Tri", "Rhombus", "Fill", "Text"]
    for i, tool in enumerate(tools):
        rect = pygame.Rect(230 + i * 82, 10, 78, 35)
        bg = (160, 160, 160) if active_tool == tool.lower() else (230, 230, 230)
        pygame.draw.rect(screen, bg, rect, border_radius=5)
        pygame.draw.rect(screen, BLACK, rect, 1, border_radius=5)
        text_surf = font.render(tool, True, BLACK)
        screen.blit(text_surf, (rect.x + 5, rect.y + 8))

    # Информационная панель
    info = font_bold.render(f"SIZE: {active_size} px | TOOL: {active_tool.upper()}", True, BLACK)
    screen.blit(info, (10, 60))
    hint = font.render("Keys: 1, 2, 3 - Resize | Ctrl+S - Save | Enter - Confirm Text", True, (80, 80, 80))
    screen.blit(hint, (350, 60))

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        # Обработка клавиатуры
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1: active_size = 2
            elif event.key == pygame.K_2: active_size = 5
            elif event.key == pygame.K_3: active_size = 10
            
            # Сохранение через Ctrl+S
            if event.key == pygame.K_s and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                save_canvas(screen)

            # Ввод текста
            if active_tool == 'text' and text_pos:
                if event.key == pygame.K_RETURN:
                    text_pos = None # Фиксация текста
                elif event.key == pygame.K_BACKSPACE:
                    text_buffer = text_buffer[:-1]
                else:
                    text_buffer += event.unicode

        # Мышь
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.pos[1] < UI_HEIGHT:
                # Проверка кликов по кнопкам
                for i, color in enumerate(COLORS):
                    if pygame.Rect(10 + i * 35, 10, 30, 30).collidepoint(event.pos):
                        active_color = color
                tools_list = ["brush", "line", "eraser", "square", "right_tri", "equ_tri", "rhombus", "fill", "text"]
                for i, tool in enumerate(tools_list):
                    if pygame.Rect(230 + i * 82, 10, 78, 35).collidepoint(event.pos):
                        active_tool = tool
            else:
                drawing = True
                start_pos, last_pos = event.pos, event.pos
                snapshot = screen.copy() # Снимок для превью и очистки текста
                
                if active_tool == 'fill':
                    flood_fill(screen, *event.pos, active_color, UI_HEIGHT)
                elif active_tool == 'text':
                    text_pos, text_buffer = event.pos, ""

        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False

        if event.type == pygame.MOUSEMOTION and drawing:
            if active_tool in ['brush', 'eraser']:
                color = active_color if active_tool == 'brush' else WHITE
                pygame.draw.line(screen, color, last_pos, event.pos, active_size * 2)
                last_pos = event.pos
            
            elif active_tool in ['line', 'square', 'right_tri', 'equ_tri', 'rhombus']:
                screen.blit(snapshot, (0, 0)) # Стираем старое превью перед отрисовкой нового
                w, h = event.pos[0] - start_pos[0], event.pos[1] - start_pos[1]
                
                if active_tool == 'line':
                    pygame.draw.line(screen, active_color, start_pos, event.pos, active_size)
                elif active_tool == 'square':
                    side = max(abs(w), abs(h))
                    sx = start_pos[0] if w > 0 else start_pos[0] - side
                    sy = start_pos[1] if h > 0 else start_pos[1] - side
                    pygame.draw.rect(screen, active_color, [sx, sy, side, side], active_size)
                elif active_tool == 'right_tri':
                    pygame.draw.polygon(screen, active_color, get_right_triangle_points(start_pos, event.pos), active_size)
                elif active_tool == 'equ_tri':
                    pygame.draw.polygon(screen, active_color, get_equilateral_triangle_points(start_pos, event.pos), active_size)
                elif active_tool == 'rhombus':
                    pygame.draw.polygon(screen, active_color, get_rhombus_points(start_pos, event.pos), active_size)

    # Отрисовка текста без наслоения и линий
    if active_tool == 'text' and text_pos:
        screen.blit(snapshot, (0, 0)) # Очищаем фон под текстом
        text_surf = font.render(text_buffer, True, active_color)
        screen.blit(text_surf, text_pos)

    draw_ui()
    pygame.display.flip()

pygame.quit()