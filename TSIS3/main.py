import pygame, sys, random
from racer import Player, Enemy, Coin, PowerUp
from ui import button, draw_text
from persistence import load_data, save_data, update_leaderboard

# Инициализация
pygame.init()
pygame.mixer.init()

SCREEN = pygame.display.set_mode((400, 600))
CLK = pygame.time.Clock()

# Загружаем настройки СРАЗУ, чтобы знать, включать ли музыку
settings = load_data('settings.json', {"sound": True, "color": [255,255,255]})

# Загрузка ресурсов
BG = pygame.transform.scale(pygame.image.load("assets/image_street.png"), (400, 600))

import os
print("Текущая рабочая директория:", os.getcwd())
if os.path.exists("assets"):
    print("Папка assets найдена!")
    print("Файлы в ней:", os.listdir("assets"))
else:
    print("ОШИБКА: Папка assets НЕ НАЙДЕНА в", os.getcwd())

try:
    pygame.mixer.music.load("assets/background.mp3")
    catch_sound = pygame.mixer.Sound("assets/catch.mp3")
    if settings.get("sound", True):
        pygame.mixer.music.play(-1)
except:
    print("Звуковые файлы не найдены!")
    catch_sound = None

STATE = "MENU"
user_name = "Player"

def draw_settings():
    global STATE, settings
    SCREEN.fill((230, 230, 230))
    draw_text(SCREEN, "SETTINGS", 40, 110, 50)

    # Кнопка переключения звука
    label = "SOUND: ON" if settings["sound"] else "SOUND: OFF"
    # Цвет кнопки меняется в зависимости от состояния
    btn_color = (0, 200, 0) if settings["sound"] else (200, 0, 0)
    
    if button(SCREEN, label, 100, 150, 200, 50, btn_color, (180, 180, 180)):
        # 1. Меняем состояние
        settings["sound"] = not settings["sound"]
        # 2. Сохраняем в файл
        save_data('settings.json', settings)
        
        # 3. Управляем музыкой
        if settings["sound"]:
            try:
                # Проверяем, загружена ли музыка вообще
                pygame.mixer.music.unpause() # Пробуем снять с паузы
                if not pygame.mixer.music.get_busy():
                    pygame.mixer.music.play(-1)
            except pygame.error:
                print("Музыка не загружена, играть нечего.")
        else:
            pygame.mixer.music.pause() # Вместо стоп лучше пауза
        
        # Задержка, чтобы одно нажатие не засчиталось как десять
        pygame.time.delay(200)

    # Выбор цвета (оставляем как было)
    draw_text(SCREEN, "CAR COLOR:", 20, 140, 230)
    if button(SCREEN, "RED", 50, 280, 80, 40, (200, 0, 0), (255, 0, 0)):
        settings["color"] = [255, 0, 0]; save_data('settings.json', settings)
    if button(SCREEN, "GREEN", 150, 280, 80, 40, (0, 200, 0), (0, 255, 0)):
        settings["color"] = [0, 255, 0]; save_data('settings.json', settings)
    if button(SCREEN, "WHITE", 250, 280, 80, 40, (255, 255, 255), (200, 200, 200)):
        settings["color"] = [255, 255, 255]; save_data('settings.json', settings)

    if button(SCREEN, "BACK", 150, 450, 100, 50, (100, 100, 100), (150, 150, 150)):
        STATE = "MENU"

    # Выбор цвета
    draw_text(SCREEN, "CAR COLOR:", 20, 140, 230)
    if button(SCREEN, "RED", 50, 280, 80, 40, (200, 0, 0), (255, 0, 0)):
        settings["color"] = [255, 0, 0]; save_data('settings.json', settings)
    if button(SCREEN, "GREEN", 150, 280, 80, 40, (0, 200, 0), (0, 255, 0)):
        settings["color"] = [0, 255, 0]; save_data('settings.json', settings)
    if button(SCREEN, "WHITE", 250, 280, 80, 40, (255, 255, 255), (200, 200, 200)):
        settings["color"] = [255, 255, 255]; save_data('settings.json', settings)

    if button(SCREEN, "BACK", 150, 450, 100, 50, (100, 100, 100), (150, 150, 150)):
        STATE = "MENU"

def game_loop():
    global STATE
    score = 0
    speed = 5
    p1 = Player(tuple(settings["color"]))
    enemies = pygame.sprite.Group(Enemy(speed))
    coins = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group(p1)

    while True:
        SCREEN.blit(BG, (0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()

        # Появление объектов
        if random.randint(1, 100) == 1:
            c = Coin(); coins.add(c); all_sprites.add(c)
        if random.randint(1, 500) == 1:
            pw = PowerUp(); powerups.add(pw); all_sprites.add(pw)

        # Движение
        p1.move()
        for e in enemies: e.move()
        for c in coins: c.move()
        for p in powerups: p.move()

        # Коллизии с врагами
        if pygame.sprite.spritecollideany(p1, enemies):
            if p1.shielded:
                p1.shielded = False
                for e in enemies: e.spawn()
            else:
                update_leaderboard(user_name, score)
                STATE = "GAMEOVER"; return

        # Коллизии с монетами
        collected = pygame.sprite.spritecollide(p1, coins, True)
        for c in collected:
            score += c.weight
            if catch_sound and settings["sound"]:
                catch_sound.play()
            if score > 0 and score % 10 == 0: # Ускорение
                speed += 1
                for e in enemies: e.speed = speed

# Коллизии с бонусами (Power-Ups)
        p_collected = pygame.sprite.spritecollide(p1, powerups, True)
        for p in p_collected:
            if p.type == "shield":
                p1.shielded = True
                print("Бонус: Щит активирован!")
            elif p.type == "nitro":
                # Nitro временно ускоряет игрока (или замедляет врагов)
                speed = max(2, speed - 2) 
                print("Бонус: Nitro (враги замедлены)!")
            elif p.type == "repair":
                # Repair мгновенно убирает врагов с дороги
                for e in enemies:
                    e.spawn()
                print("Бонус: Дорога расчищена (Repair)!")
                
        # Отрисовка
        all_sprites.draw(SCREEN)
        enemies.draw(SCREEN)
        draw_text(SCREEN, f"Score: {score}", 25, 10, 10, (255, 255, 255))
        if p1.shielded: draw_text(SCREEN, "SHIELD ACTIVE", 15, 10, 40, (0, 255, 0))
        
        pygame.display.update()
        CLK.tick(60)

# Главный цикл
while True:
    SCREEN.fill((220, 220, 220))
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT: pygame.quit(); sys.exit()
        if STATE == "MENU" and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE: user_name = user_name[:-1]
            elif event.key == pygame.K_RETURN: pass # Можно добавить старт на Enter
            else: user_name += event.unicode

    if STATE == "MENU":
        draw_text(SCREEN, "RACER 3.0", 50, 70, 50)
        draw_text(SCREEN, f"Name: {user_name}", 20, 100, 150)
        if button(SCREEN, "START GAME", 100, 250, 200, 50, (0,200,0), (0,255,0)): STATE = "GAME"
        if button(SCREEN, "SETTINGS", 100, 320, 200, 50, (150,150,150), (180,180,180)): STATE = "SETTINGS"
        if button(SCREEN, "LEADERBOARD", 100, 390, 200, 50, (200,200,0), (255,255,0)): STATE = "LB"

    elif STATE == "SETTINGS":
        draw_settings()

    elif STATE == "GAME":
        game_loop()

    elif STATE == "GAMEOVER":
        draw_text(SCREEN, "GAME OVER", 50, 60, 200, (200,0,0))
        if button(SCREEN, "MENU", 150, 350, 100, 50, (255,255,255), (200,200,200)): STATE = "MENU"

    elif STATE == "LB":
        draw_text(SCREEN, "TOP 10", 30, 150, 50)
        data = load_data('leaderboard.json', [])
        for i, entry in enumerate(data):
            draw_text(SCREEN, f"{i+1}. {entry['name']} - {entry['score']}", 20, 100, 100 + i*30)
        if button(SCREEN, "BACK", 150, 500, 100, 50, (150,150,150), (180,180,180)): STATE = "MENU"

    pygame.display.update()
    CLK.tick(60)