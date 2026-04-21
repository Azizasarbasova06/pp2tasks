import pygame

# 1. Инициализация Pygame
pygame.init()

# Константы окна 
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Ball Game")

# Цвета 
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Параметры шарика (Radius 25, 50x50 pixel)
ball_radius = 25
# Начальная позиция — центр экрана
ball_x = WIDTH // 2
ball_y = HEIGHT // 2

# Скорость (20 pixels per press)
STEP = 20

clock = pygame.time.Clock()
running = True

while running:
    # Очистка экрана (White background)
    screen.fill(WHITE)
    
    # Слушаем нажатия (Handle keyboard events)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Перемещение по стрелкам (Up, Down, Left, Right)
        if event.type == pygame.KEYDOWN:
            # УСЛОВИЕ: Ball cannot leave the screen boundaries
            if event.key == pygame.K_UP:
                # Проверяем: если шаг вверх не выведет край шарика за 0
                if ball_y - STEP >= ball_radius:
                    ball_y -= STEP
            
            elif event.key == pygame.K_DOWN:
                # Проверяем: если шаг вниз не выведет край за границу HEIGHT
                if ball_y + STEP <= HEIGHT - ball_radius:
                    ball_y += STEP
            
            elif event.key == pygame.K_LEFT:
                if ball_x - STEP >= ball_radius:
                    ball_x -= STEP
            
            elif event.key == pygame.K_RIGHT:
                if ball_x + STEP <= WIDTH - ball_radius:
                    ball_x += STEP

    # Отрисовка шарика 
    pygame.draw.circle(screen, RED, (ball_x, ball_y), ball_radius)

    # Обновление кадра (Smooth animation)
    pygame.display.flip()
    clock.tick(60) # 60 FPS для плавности

pygame.quit()