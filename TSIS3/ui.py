import pygame

def draw_text(screen, text, size, x, y, color=(0,0,0)):
    font = pygame.font.SysFont("Verdana", size)
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

def button(screen, msg, x, y, w, h, ic, ac):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen, ac, (x, y, w, h))
        if click[0] == 1:
            pygame.time.delay(150)
            return True
    else:
        pygame.draw.rect(screen, ic, (x, y, w, h))
    draw_text(screen, msg, 20, x + 10, y + 10)
    return False