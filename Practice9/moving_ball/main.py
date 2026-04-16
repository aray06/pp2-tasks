import pygame
from ball import Ball

pygame.init()
W, H = 800, 600
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Moving Ball Task")

# Создаем объект мяча
my_ball = Ball(W//2, H//2, 25, (255, 0, 0), W, H)

running = True
clock = pygame.time.Clock()

while running:
    screen.fill((255, 255, 255)) # Белый фон

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                my_ball.move("up")
            elif event.key == pygame.K_DOWN:
                my_ball.move("down")
            elif event.key == pygame.K_LEFT:
                my_ball.move("left")
            elif event.key == pygame.K_RIGHT:
                my_ball.move("right")

    # Рисуем мяч
    my_ball.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()