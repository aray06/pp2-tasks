import pygame
import random

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

class Player(pygame.sprite.Sprite):
    def __init__(self, color=(255,255,255)):
        super().__init__()
        img = pygame.image.load("assets/image_player1.png")
        self.image = pygame.transform.scale(img, (50, 90))
        self.image.fill(color, special_flags=pygame.BLEND_RGB_MULT)
        self.rect = self.image.get_rect(center=(200, 520))
        self.shielded = False

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0: self.rect.move_ip(-7, 0)
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH: self.rect.move_ip(7, 0)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        img = pygame.image.load("assets/image_player2.png")
        self.image = pygame.transform.scale(img, (105, 95))
        self.rect = self.image.get_rect()
        self.speed = speed
        self.spawn()

    def spawn(self):
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), -100)

    def move(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > SCREEN_HEIGHT: self.spawn()

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        img = pygame.image.load("assets/image_coin.png")
        self.weight = random.choice([1, 5])
        self.image = pygame.transform.scale(img, (30, 30))
        if self.weight == 5: self.image.fill((255, 215, 0), special_flags=pygame.BLEND_RGB_MULT)
        self.rect = self.image.get_rect(center=(random.randint(40, 360), -50))

    def move(self):
        self.rect.move_ip(0, 5)
        if self.rect.top > SCREEN_HEIGHT: self.kill()

class PowerUp(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # ТЕПЕРЬ ИХ ТРИ: shield, nitro, repair
        self.type = random.choice(["shield", "nitro", "repair"])
        self.image = pygame.Surface((30, 30))
        
        # Разные цвета для разных бонусов
        if self.type == "shield":
            color = (0, 255, 0)   # Зеленый
        elif self.type == "nitro":
            color = (0, 0, 255)   # Синий
        else:
            color = (255, 255, 0) # Желтый (для Repair)
            
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(random.randint(40, 360), -50))

    def move(self):
        self.rect.move_ip(0, 5)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()