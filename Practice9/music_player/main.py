import pygame
import os
from player import MusicPlayer

# Инициализация
pygame.init()
pygame.mixer.init()

W, H = 600, 400
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("KBTU Studio Player")

# Настройка шрифта
font = pygame.font.SysFont("Arial", 24)
title_font = pygame.font.SysFont("Arial", 32, bold=True)

# Инициализация логики плеера
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
music_path = os.path.join(BASE_DIR, 'music', 'sample_tracks')
my_player = MusicPlayer(music_path)

# Запускаем музыку сразу
my_player.play()

running = True
while running:
    screen.fill((30, 30, 30)) # Темно-серый фон

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p: my_player.toggle_pause()
            elif event.key == pygame.K_s: my_player.stop()
            elif event.key == pygame.K_n: my_player.next_track()
            elif event.key == pygame.K_b: my_player.prev_track()
            elif event.key == pygame.K_q: running = False

    # --- Отрисовка UI ---
    # Название песни
    text_surf = title_font.render(f"Now Playing:", True, (0, 255, 150))
    screen.blit(text_surf, (50, 100))
    
    song_surf = font.render(my_player.get_current_name(), True, (255, 255, 255))
    screen.blit(song_surf, (50, 150))

    # Инструкции
    hint = font.render("P: Play/Pause | S: Stop | N: Next | B: Back | Q: Quit", True, (150, 150, 150))
    screen.blit(hint, (50, 300))

    pygame.display.flip()

pygame.quit()