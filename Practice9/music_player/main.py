import pygame
from player import MusicPlayer

pygame.init()
pygame.mixer.init()

# Настройки окна
WIDTH, HEIGHT = 500, 350
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("KBTU Music Player")

# Шрифты
font_main = pygame.font.SysFont("Arial", 24, bold=True)
font_sub = pygame.font.SysFont("Arial", 18)
font_hint = pygame.font.SysFont("Arial", 14)

# Инициализация плеера (укажи свою папку!)
player = MusicPlayer("music/sample_tracks") 

running = True
is_paused = False

while running:
    screen.fill((25, 25, 25)) # Темный фон как в Spotify
    
    # 1. Получаем данные
    artist, title = player.get_info()
    current_time = player.get_pos()
    total_time = player.duration
    
    # 2. Отрисовка текста (Track Info)
    artist_surf = font_sub.render(artist, True, (180, 180, 180))
    title_surf = font_main.render(title, True, (255, 255, 255))
    screen.blit(artist_surf, (20, 40))
    screen.blit(title_surf, (20, 70))

    # 3. Визуализация прогресса (Playback Progress)
    # Рисуем серую подложку (фон полоски)
    bar_x, bar_y, bar_width, bar_height = 20, 150, 460, 6
    pygame.draw.rect(screen, (60, 60, 60), (bar_x, bar_y, bar_width, bar_height), border_radius=3)
    
    # Считаем ширину зеленой полоски
    if total_time > 0:
        progress = (current_time / total_time) * bar_width
        pygame.draw.rect(screen, (30, 215, 96), (bar_x, bar_y, progress, bar_height), border_radius=3)

    # Время цифрами
    time_str = f"{int(current_time // 60):02}:{int(current_time % 60):02} / {int(total_time // 60):02}:{int(total_time % 60):02}"
    time_surf = font_hint.render(time_str, True, (150, 150, 150))
    screen.blit(time_surf, (20, 165))

    # Подсказки по кнопкам
    hint = font_hint.render("P: Play/Pause | S: Stop | N: Next | B: Back", True, (100, 100, 100))
    screen.blit(hint, (20, 300))

    # 4. Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                if not player.is_loaded:
                    player.play()
                    is_paused = False
                elif is_paused:
                    player.unpause()
                    is_paused = False
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

    pygame.display.flip()
    pygame.time.Clock().tick(30)

pygame.quit()