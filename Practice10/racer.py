import pygame, sys
from pygame.locals import *
import random, time

# Инициализация
pygame.init()

# Настройка FPS
FPS = 60
FramePerSec = pygame.time.Clock()

# Цвета
RED   = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Параметры экрана
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0
COIN_SCORE = 0 # Счетчик собранных монет

# Создание экрана
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Racer Practice 10")

# Шрифты
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over_text = font.render("Game Over", True, BLACK)

# Загрузка изображений 
try:
    background = pygame.image.load("images/image_street.png") # Фон
    player_img = pygame.image.load("images/image_player1.png") # Игрок
    enemy_img = pygame.image.load("images/image_player2.png")  # Враг
    coin_img = pygame.image.load("images/image_coin.png")   # Монета
except FileNotFoundError:
    print("Ошибка: Проверь, что папка 'images' находится рядом с файлом racer.py")
    pygame.quit()
    sys.exit()

# ИСПРАВЛЕНИЕ 1: Масштабирование
player_img = pygame.transform.scale(player_img, (50, 90))
# Врага делаем больше (75x130), чтобы компенсировать пустое место на его картинке
enemy_img = pygame.transform.scale(enemy_img, (105, 95)) 

coin_img = pygame.transform.scale(coin_img, (30, 30))
# ИСПРАВЛЕНИЕ 2: Убираем черный фон у JPG-монетки, чтобы она стала круглой
coin_img.set_colorkey(BLACK)

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = enemy_img
        self.rect = self.image.get_rect()
        # Спавним чуть выше экрана (-50), чтобы машина выезжала плавно
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), -50) 

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if (self.rect.top > 600):
            SCORE += 1 # Очко за то, что увернулись
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), -50)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
       
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0:
              if pressed_keys[K_LEFT]:
                  self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:        
              if pressed_keys[K_RIGHT]:
                  self.rect.move_ip(5, 0)

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = coin_img
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), -100)

    def move(self):
        global SPEED
        # ИСПРАВЛЕНИЕ 3: Монетка теперь двигается с той же скоростью, что и враги
        self.rect.move_ip(0, SPEED) 
        if (self.rect.top > 600):
            self.rect.top = 0
            # Если пропустили монету, она появится снова за экраном
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), -100)

# Создание объектов
P1 = Player()
E1 = Enemy()
C1 = Coin()

# Группировка
enemies = pygame.sprite.Group()
enemies.add(E1)

coins = pygame.sprite.Group()
coins.add(C1)

all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C1)

# Событие для постепенного ускорения игры
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

# Игровой цикл
while True:
    for event in pygame.event.get():
        if event.type == INC_SPEED:
              SPEED += 0.2 # Немного ускоряем игру каждую секунду     
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Отрисовка фона
    DISPLAYSURF.blit(pygame.transform.scale(background, (400,600)), (0,0))
    
    # Текст со счетом
    scores = font_small.render(f"Score: {SCORE}", True, BLACK)
    coin_text = font_small.render(f"Coins: {COIN_SCORE}", True, BLACK)
    DISPLAYSURF.blit(scores, (10,10))
    DISPLAYSURF.blit(coin_text, (280,10)) # Чуть сдвинул влево, чтобы не обрезалось

    # Отрисовка и движение всех объектов
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    # Проверка сбора монет
    if pygame.sprite.spritecollideany(P1, coins):
        for coin in pygame.sprite.spritecollide(P1, coins, True):
            COIN_SCORE += 1 
            new_coin = Coin()
            coins.add(new_coin)
            all_sprites.add(new_coin)

    # Столкновение с врагом
    if pygame.sprite.spritecollideany(P1, enemies):
          time.sleep(0.5)
          DISPLAYSURF.fill(RED)
          DISPLAYSURF.blit(game_over_text, (30,250))
          pygame.display.update()
          time.sleep(2)
          pygame.quit()
          sys.exit()        
        
    pygame.display.update()
    FramePerSec.tick(FPS)