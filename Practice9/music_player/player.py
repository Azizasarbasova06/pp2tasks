import pygame
import os

class MusicPlayer:
    def __init__(self, music_dir):
        self.music_dir = music_dir
        self.is_loaded = False
        self.playlist = []
        if os.path.exists(music_dir):
            self.playlist = [f for f in os.listdir(music_dir) if f.endswith(('.mp3', '.wav'))]
        
        self.current_index = 0
        self.duration = 0 # Длительность текущего трека

    def play(self):
        if self.playlist:
            track_path = os.path.join(self.music_dir, self.playlist[self.current_index])
            pygame.mixer.music.load(track_path)
            pygame.mixer.music.play()
            self.is_loaded = True
            
            # Получаем длительность трека для прогресс-бара
            sound = pygame.mixer.Sound(track_path)
            self.duration = sound.get_length()

    def stop(self):
        pygame.mixer.music.stop()
        self.is_loaded = False

    def pause(self):
        if self.is_loaded: pygame.mixer.music.pause()

    def unpause(self):
        if self.is_loaded: pygame.mixer.music.unpause()

    def next(self):
        if self.playlist:
            self.current_index = (self.current_index + 1) % len(self.playlist)
            self.play()

    def prev(self):
        if self.playlist:
            self.current_index = (self.current_index - 1) % len(self.playlist)
            self.play()

    def get_info(self):
        """Разделяет имя файла на Артиста и Название"""
        if not self.playlist:
            return "No Artist", "No Track"
        
        filename = self.playlist[self.current_index].replace(".mp3", "").replace(".wav", "")
        if " - " in filename:
            return filename.split(" - ", 1)
        return "Unknown Artist", filename

    def get_pos(self):
        if self.is_loaded:
            pos = pygame.mixer.music.get_pos()
            return pos / 1000 if pos > 0 else 0
        return 0