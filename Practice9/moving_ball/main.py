import pygame
from ball import Ball # Импортируем наш класс Ball

# Инициализация всех модулей pygame
pygame.init()

# Константы размеров окна
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Ball")

# clock помогает контролировать частоту кадров (FPS)
clock = pygame.time.Clock()

# Создаем экземпляр шара в центре экрана
ball = Ball(WIDTH // 2, HEIGHT // 2)

running = True
# Основной игровой цикл
while running:
    # Очистка экрана: заливаем всё белым цветом перед каждым новым кадром
    screen.fill((255, 255, 255))

    # Обработка событий (нажатия клавиш, закрытие окна)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False # Выход из цикла при закрытии окна

        # Обработка одиночных нажатий клавиш
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                ball.move_left()
            elif event.key == pygame.K_RIGHT:
                ball.move_right(WIDTH)
            elif event.key == pygame.K_UP:
                ball.move_up()
            elif event.key == pygame.K_DOWN:
                ball.move_down(HEIGHT)

    # Рисуем шар в его актуальных координатах
    ball.draw(screen)
    
    # Обновляем содержимое всего экрана
    pygame.display.flip()
    
    # Ограничиваем цикл до 60 кадров в секунду
    clock.tick(60)

pygame.quit()