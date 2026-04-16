import pygame

class Ball:
    def __init__(self, x, y, radius, color, screen_w, screen_h):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.speed = 20

    def move(self, direction):
        if direction == "up":
            if self.y - self.speed >= self.radius:
                self.y -= self.speed
        elif direction == "down":
            if self.y + self.speed <= self.screen_h - self.radius:
                self.y += self.speed
        elif direction == "left":
            if self.x - self.speed >= self.radius:
                self.x -= self.speed
        elif direction == "right":
            if self.x + self.speed <= self.screen_w - self.radius:
                self.x += self.speed

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)