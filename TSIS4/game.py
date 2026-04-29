import pygame, random
from config import *

class GameEngine:
    def __init__(self, settings):
        self.settings = settings
        self.snake = [[WIDTH//2, HEIGHT//2]]
        self.direction = (SNAKE_BLOCK, 0)
        self.score, self.level = 0, 1
        self.base_speed = 7
        self.obstacles = [] 
        self.food = self.rand_pos([])
        self.food_type = 'reg'
        self.food_timer = pygame.time.get_ticks()
        self.poison = self.rand_pos([])
        self.powerup = None
        self.powerup_type = None
        self.powerup_spawn_time = 0
        self.active_powerup = None
        self.powerup_end_time = 0

    def rand_pos(self, ignore):
        while True:
            x = random.randrange(0, WIDTH - SNAKE_BLOCK, SNAKE_BLOCK)
            y = random.randrange(40, HEIGHT - SNAKE_BLOCK, SNAKE_BLOCK)
            if [x, y] not in self.snake and [x, y] not in self.obstacles and [x, y] not in ignore:
                return [x, y]

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.food_timer > 5000:
            self.food = self.rand_pos([])
            self.food_timer = now
        
        if self.powerup and now - self.powerup_spawn_time > 8000:
            self.powerup = None

        if not self.powerup and random.random() < 0.02:
            self.powerup = self.rand_pos([self.food])
            self.powerup_type = random.choice(['speed', 'slow', 'shield'])
            self.powerup_spawn_time = now

        new_head = [self.snake[-1][0] + self.direction[0], self.snake[-1][1] + self.direction[1]]
        
        # Столкновения
        if new_head in self.obstacles or new_head[0]<0 or new_head[0]>=WIDTH or new_head[1]<40 or new_head[1]>=HEIGHT:
            if self.active_powerup == 'shield':
                self.active_powerup = None
                return "shield_break"
            return False
            
        if new_head in self.snake: return False

        self.snake.append(new_head)

        if new_head == self.food:
            self.score += 5 if self.food_type == 'gold' else 1
            self.food = self.rand_pos([])
            self.food_type = random.choice(['reg', 'gold'])
            self.food_timer = now
            if self.score // 5 >= self.level:
                self.level += 1
                self.obstacles.append(self.rand_pos([self.food]))
            return "eat"
        
        elif new_head == self.poison:
            if len(self.snake) <= 3: return False
            for _ in range(3): self.snake.pop(0)
            self.poison = self.rand_pos([])
            return "poison"
            
        elif self.powerup and new_head == self.powerup:
            self.active_powerup = self.powerup_type
            self.powerup_end_time = now + 5000
            self.powerup = None
            return "powerup"
        
        self.snake.pop(0)
        if self.active_powerup in ['speed', 'slow'] and now > self.powerup_end_time:
            self.active_powerup = None
        return True

    def get_speed(self):
        s = self.base_speed + self.level
        if self.active_powerup == 'speed': return s + 5
        if self.active_powerup == 'slow': return max(3, s - 4)
        return s