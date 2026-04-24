import pygame
import time
import random

# Инициализация Pygame
pygame.init()

# Настройка цветов (RGB)
COLOR_BG = (20, 25, 30)         # Фон
COLOR_SNAKE = (46, 204, 113)     # Змейка
COLOR_SNAKE_SHADE = (39, 174, 96)# Контур змейки
COLOR_FOOD_BASE = (231, 76, 60)  # Обычная еда (красная)
COLOR_FOOD_GOLD = (241, 196, 15)  # Супер-еда (золотая)
COLOR_TEXT = (236, 240, 241)     # Текст
COLOR_LEVEL = (241, 196, 15)     # Уровень

# Параметры окна
WIDTH, HEIGHT = 600, 400
dis = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Practice 11 - Weights and Timers')

# Игровые константы
snake_block = 20
initial_speed = 7
clock = pygame.time.Clock()

# Шрифты
font_style = pygame.font.SysFont("Verdana", 25)
score_font = pygame.font.SysFont("Verdana", 20)

def display_stats(score, level, timer_val):
    """Отображение счета, уровня и оставшегося времени до исчезновения еды"""
    pygame.draw.rect(dis, (44, 62, 80), [0, 0, WIDTH, 40])
    pygame.draw.line(dis, COLOR_LEVEL, (0, 40), (WIDTH, 40), 2)
    
    val_score = score_font.render(f"SCORE: {score}", True, COLOR_TEXT)
    val_level = score_font.render(f"LEVEL: {level}", True, COLOR_LEVEL)
    # Таймер еды для удобства игрока
    val_timer = score_font.render(f"FOOD RESET IN: {int(timer_val)}s", True, COLOR_TEXT)
    
    dis.blit(val_score, [20, 10])
    dis.blit(val_level, [WIDTH // 2 - 40, 10])
    dis.blit(val_timer, [WIDTH - 220, 10])

def draw_snake(snake_list):
    """Рисование змейки с эффектом глаз у головы"""
    for i, x in enumerate(snake_list):
        pygame.draw.rect(dis, COLOR_SNAKE, [x[0], x[1], snake_block, snake_block])
        pygame.draw.rect(dis, COLOR_SNAKE_SHADE, [x[0], x[1], snake_block, snake_block], 1)
        # Голова
        if i == len(snake_list) - 1:
            pygame.draw.rect(dis, COLOR_BG, [x[0] + 4, x[1] + 4, 4, 4])
            pygame.draw.rect(dis, COLOR_BG, [x[0] + 12, x[1] + 4, 4, 4])

def draw_background():
    """Сетка на заднем фоне"""
    dis.fill(COLOR_BG)
    for x in range(0, WIDTH, snake_block):
        pygame.draw.line(dis, (30, 35, 40), (x, 40), (x, HEIGHT))
    for y in range(40, HEIGHT, snake_block):
        pygame.draw.line(dis, (30, 35, 40), (0, y), (WIDTH, y))

def gameLoop():
    game_over = False
    game_close = False

    # Начальная позиция змейки
    x1, y1 = WIDTH / 2, HEIGHT / 2
    x1_change, y1_change = 0, 0

    snake_List = []
    Length_of_snake = 1

    # ЗАДАНИЕ: Еда с разным весом
    # food_weight может быть 1 (обычная) или 5 (золотая)
    food_weight = random.choice([1, 5])
    foodx = round(random.randrange(0, WIDTH - snake_block) / 20.0) * 20.0
    foody = round(random.randrange(40, HEIGHT - snake_block) / 20.0) * 20.0

    # ЗАДАНИЕ: Таймер для еды
    # Еда исчезает через 5 секунд (5000 миллисекунд)
    food_spawn_time = pygame.time.get_ticks() 
    food_lifetime = 5000 

    score = 0
    level = 1
    current_speed = initial_speed

    while not game_over:

        while game_close:
            dis.fill(COLOR_BG)
            msg = font_style.render("GAME OVER", True, COLOR_FOOD_BASE)
            sub_msg = score_font.render("C - Restart | Q - Quit", True, COLOR_TEXT)
            dis.blit(msg, [WIDTH / 2 - 80, HEIGHT / 2 - 40])
            dis.blit(sub_msg, [WIDTH / 2 - 95, HEIGHT / 2 + 10])
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change, y1_change = -snake_block, 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change, y1_change = snake_block, 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change, x1_change = -snake_block, 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change, x1_change = snake_block, 0

        # Проверка выхода за границы
        if x1 >= WIDTH or x1 < 0 or y1 >= HEIGHT or y1 < 40:
            game_close = True
        
        x1 += x1_change
        y1 += y1_change
        
        draw_background()

        # ЗАДАНИЕ: Foods which are disappearing after some time
        current_time = pygame.time.get_ticks()
        if current_time - food_spawn_time > food_lifetime:
            # Время вышло - пересоздаем еду в новом месте
            food_weight = random.choice([1, 5])
            foodx = round(random.randrange(0, WIDTH - snake_block) / 20.0) * 20.0
            foody = round(random.randrange(40, HEIGHT - snake_block) / 20.0) * 20.0
            food_spawn_time = current_time

        # ЗАДАНИЕ: Рисуем еду разного цвета в зависимости от веса
        color = COLOR_FOOD_GOLD if food_weight == 5 else COLOR_FOOD_BASE
        pygame.draw.circle(dis, color, (int(foodx + 10), int(foody + 10)), 8)
        
        # Логика тела змейки
        snake_Head = [x1, y1]
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        draw_snake(snake_List)
        
        # Рассчитываем оставшееся время для отображения
        time_left = max(0, (food_lifetime - (current_time - food_spawn_time)) / 1000)
        display_stats(score, level, time_left)

        pygame.display.update()

        # Проверка поедания еды
        if x1 == foodx and y1 == foody:
            score += food_weight # Прибавляем вес еды к счету
            Length_of_snake += 1 # Змейка растет всегда на 1
            
            # Генерация новой еды сразу после поедания
            food_weight = random.choice([1, 5])
            while True:
                foodx = round(random.randrange(0, WIDTH - snake_block) / 20.0) * 20.0
                foody = round(random.randrange(40, HEIGHT - snake_block) / 20.0) * 20.0
                if [foodx, foody] not in snake_List:
                    break
            food_spawn_time = pygame.time.get_ticks()

            # Уровни и скорость
            if score // 5 >= level: # Каждые 5 очков - новый уровень
                level += 1
                current_speed += 1

        clock.tick(current_speed)

    pygame.quit()
    quit()

if __name__ == "__main__":
    gameLoop()