import pygame
from clock import MickeyClock # Импортируем класс с логикой времени и отрисовки

# Инициализация всех модулей Pygame
pygame.init()

# Устанавливаем размер окна (800x800 пикселей)
SIZE = 800
screen = pygame.display.set_mode((SIZE, SIZE))
# Заголовок окна, который отображается в верхней панели
pygame.display.set_caption("Mickey Mouse Real Time Clock")

# Создаем объект наших часов, передавая ему размеры экрана
clock_logic = MickeyClock(SIZE, SIZE)

# Объект для контроля частоты кадров (FPS)
timer = pygame.time.Clock()

# Главный цикл программы (Main Loop)
running = True
while running:
    # 1. ОБРАБОТКА СОБЫТИЙ (Events)
    # Проверяем все действия пользователя (нажатия клавиш, мышки)
    for event in pygame.event.get():
        # Если пользователь нажал на "крестик", выходим из цикла
        if event.type == pygame.QUIT:
            running = False

    # 2. ОТРИСОВКА (Drawing)
    # Сначала заливаем экран белым цветом, чтобы стереть предыдущий кадр
    screen.fill((255, 255, 255))
    
    # Вызываем метод draw из нашего класса clock.py
    # Именно там происходит расчет углов и вращение стрелок
    clock_logic.draw(screen)
    
    # 3. ОБНОВЛЕНИЕ ЭКРАНА (Display Flip)
    # Выводим всё, что нарисовали в памяти, на реальный монитор
    pygame.display.flip()
    
    # 4. КОНТРОЛЬ ВРЕМЕНИ (FPS Control)
    # Ограничиваем цикл до 30 кадров в секунду. 
    # Этого достаточно для плавного движения секундной стрелки.
    timer.tick(30)

# Корректное завершение работы Pygame после выхода из цикла
pygame.quit()