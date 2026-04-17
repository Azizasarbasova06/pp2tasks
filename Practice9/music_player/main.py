import pygame
from player import MusicPlayer

# Запуск Pygame и звукового движка
pygame.init()
pygame.mixer.init()

# Создаем окно 500x350 пикселей
screen = pygame.display.set_mode((500, 350))
pygame.display.set_caption("My Music Player")
# Подгружаем шрифт для вывода информации
font = pygame.font.SysFont("Arial", 20)
# clock нужен для контроля скорости программы
clock = pygame.time.Clock()

# Инициализируем плеер.
player = MusicPlayer("music/sample_tracks/")

running = True
is_paused = False # Отслеживаем состояние паузы вручную

while running:
    # Заливка фона темно-серый
    screen.fill((30, 30, 30))
    
    # Получаем данные от объекта плеера
    current_track = player.get_current_track()
    pos = player.get_pos()
    
    # Готовим текст для отрисовки (render)
    track_text = font.render(f"Track: {current_track}", True, (255, 255, 255))
    time_text = font.render(f"Time: {pos} sec", True, (0, 255, 0))
    hint_text = font.render("P: Play/Pause | S: Stop | N: Next | B: Back | Q: Quit", True, (200, 200, 200))
    
    # Рисуем текст в определенных координатах 
    screen.blit(track_text, (20, 50))
    screen.blit(time_text, (20, 100))
    screen.blit(hint_text, (20, 250))

    # Слушаем действия пользователя
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Обработка нажатий на клавиатуре
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                # Если музыка еще не загружена — включаем её
                if not player.is_loaded:
                    player.play()
                    is_paused = False
                # Если стоит на паузе — продолжаем играть
                elif is_paused:
                    player.unpause()
                    is_paused = False
                # Если играет — ставим на паузу
                else:
                    player.pause()
                    is_paused = True
            
            elif event.key == pygame.K_s:
                player.stop()
                is_paused = False
                
            elif event.key == pygame.K_n:
                player.next()
                is_paused = False
                
            elif event.key == pygame.K_b:
                player.prev()
                is_paused = False
                
            elif event.key == pygame.K_q:
                # Выход из программы
                running = False

    # Обновляем кадр
    pygame.display.flip()
    # Ограничиваем до 30 кадров в секунду
    clock.tick(30)

pygame.quit()