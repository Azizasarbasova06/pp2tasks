import pygame
import os

class MusicPlayer:
    def __init__(self, music_dir):
        # Сохраняем путь к папке с музыкой
        self.music_dir = music_dir
        # is_loaded помогает нам понять, загружена ли песня в память
        self.is_loaded = False 
        
        # Проверяем, существует ли такая папка на компьютере
        if os.path.exists(music_dir):
            # Список всех файлов, которые заканчиваются на .mp3 или .wav
            self.playlist = [f for f in os.listdir(music_dir) if f.endswith(('.mp3', '.wav'))]
        else:
            self.playlist = []
        
        # Индекс текущего трека (0 — это первая песня в списке)
        self.current_index = 0
        
    def play(self):
        """Загрузка и запуск выбранного трека"""
        if self.playlist:
            # Собираем полный путь к файлу: папка + имя файла
            track_path = os.path.join(self.music_dir, self.playlist[self.current_index])
            # Загружаем файл в микшер Pygame
            pygame.mixer.music.load(track_path)
            # Начинаем воспроизведение
            pygame.mixer.music.play()
            self.is_loaded = True

    def stop(self):
        """Полная остановка музыки"""
        pygame.mixer.music.stop()
        self.is_loaded = False

    def pause(self):
        """Временная приостановка"""
        if self.is_loaded:
            pygame.mixer.music.pause()

    def unpause(self):
        """Продолжение после паузы"""
        if self.is_loaded:
            pygame.mixer.music.unpause()

    def next(self):
        """Переход к следующей песне"""
        if self.playlist:
            # % len(self.playlist) позволяет списку зацикливаться (после последней будет первая)
            self.current_index = (self.current_index + 1) % len(self.playlist)
            self.play()

    def prev(self):
        """Переход к предыдущей песне"""
        if self.playlist:
            # Если индекс станет -1, Python сам выберет последний элемент списка
            self.current_index = (self.current_index - 1) % len(self.playlist)
            self.play()

    def get_current_track(self):
        """Возвращает имя текущего файла для текста на экране"""
        if self.playlist:
            return self.playlist[self.current_index]
        return "No tracks found"

    def get_pos(self):
        """Считает, сколько секунд прошло с начала трека"""
        if self.is_loaded:
            pos = pygame.mixer.music.get_pos()
            # Делим на 1000, так как Pygame считает в миллисекундах
            return pos // 1000 if pos > 0 else 0
        return 0