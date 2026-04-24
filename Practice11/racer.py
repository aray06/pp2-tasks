import pygame, sys, random, time
from pygame.locals import *

# Инициализация
pygame.init()

# Настройки экрана и FPS
FPS = 60
FramePerSec = pygame.time.Clock()
SCREEN_WIDTH, SCREEN_HEIGHT = 400, 600
SPEED = 5 # Начальная скорость врагов
COIN_SCORE = 0
N = 10 # Ускоряем врага каждые 10 очков

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Создание окна
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Racer Practice 11")

# Загрузка ресурсов
try:
    background = pygame.image.load("images/image_street.png")
    player_img = pygame.image.load("images/image_player1.png")
    enemy_img = pygame.image.load("images/image_player2.png")
    coin_img = pygame.image.load("images/image_coin.png")
except:
    print("Error: Images not found in 'images' folder!")
    pygame.quit()
    sys.exit()

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.transform.scale(enemy_img, (105, 95))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0) 

    def move(self):
        # Move enemy down by current SPEED
        self.rect.move_ip(0, SPEED)
        if (self.rect.top > SCREEN_HEIGHT):
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
            

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.transform.scale(player_img, (50, 90))
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
        # TASK: Generate coins with different weights (1 or 5)
        self.weight = random.choice([1, 5])
        self.image = pygame.transform.scale(coin_img, (30, 30))
        
        # Visually distinguish "heavy" coins with a gold tint
        if self.weight == 5:
            self.image.fill((255, 215, 0), special_flags=pygame.BLEND_RGB_MULT)
        
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), -50)

    def move(self):
        self.rect.move_ip(0, 5) # Coins move at a steady speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill() 

# Setting up Sprites
P1 = Player()
E1 = Enemy()


enemies = pygame.sprite.Group()
enemies.add(E1)

coins = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)



# Font for scoring
font = pygame.font.SysFont("Verdana", 20)

# Main Game Loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # TASK: Randomly generating coins
    if len(coins) < 2 and random.randint(1, 100) == 1:
        new_coin = Coin()
        coins.add(new_coin)
        all_sprites.add(new_coin)

    # Draw Background
    DISPLAYSURF.blit(pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0,0))
    
    # Show Coin Score
    scores = font.render(f"Coins: {COIN_SCORE}", True, BLACK)
    DISPLAYSURF.blit(scores, (10, 10))
    speed_text = font.render(f"Enemy Speed: {SPEED}", True, BLACK)
    DISPLAYSURF.blit(speed_text, (10, 35))

    # Move and Draw all sprites
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    # Collision with Coins
    collected_coins = pygame.sprite.spritecollide(P1, coins, True)
    for coin in collected_coins:
        old_score = COIN_SCORE
        COIN_SCORE += coin.weight
        
        # TASK: Increase enemy speed when player earns N coins
        if COIN_SCORE // N > old_score // N:
            SPEED += 1

    # Collision with Enemy
    if pygame.sprite.spritecollideany(P1, enemies):
        DISPLAYSURF.fill((255, 0, 0))
        msg = pygame.font.SysFont("Verdana", 40).render("CRASHED!", True, WHITE)
        DISPLAYSURF.blit(msg, (100, 250))
        pygame.display.update()
        time.sleep(2)
        pygame.quit()
        sys.exit()

    pygame.display.update()
    FramePerSec.tick(FPS)