import pygame
import datetime

class MickeyClock:
    def __init__(self, width, height):
        self.center = (width // 2, height // 2)
        
        # 1. Загружаем фон
        try:
            self.main_img = pygame.image.load("images/mickeyclock.jpeg").convert_alpha()
            self.main_img = pygame.transform.scale(self.main_img, (width, height))
        except:
            self.main_img = pygame.Surface((width, height))
            self.main_img.fill((255, 255, 255))

        # 2. Создаем руки как отдельные поверхности (Surfaces)
        # Правая рука (минуты)
        self.right_hand_surf = pygame.Surface((width, height), pygame.SRCALPHA)
        # Рисуем руку, направленную СТРОГО ВВЕРХ (на 12 часов) — это наша точка 0 градусов
        pygame.draw.line(self.right_hand_surf, (0, 0, 0), (width//2, height//2), (width//2, height//2 - 150), 10)

        # Левая рука (секунды)
        self.left_hand_surf = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.line(self.left_hand_surf, (255, 0, 0), (width//2, height//2), (width//2, height//2 - 200), 4)

    def draw(self, screen):
        # Отрисовка фона
        screen.blit(self.main_img, (0, 0))

        # Получаем текущее системное время 
        now = datetime.datetime.now()
        minutes = now.minute
        seconds = now.second

        # 3. Расчет углов (Calculate rotation angles)
        # В Pygame положительный угол вращает ПРОТИВ часовой стрелки.
        # Чтобы стрелки шли ПО часовой, мы используем отрицательные углы (-6 градусов за единицу).
        angle_min = -minutes * 6
        angle_sec = -seconds * 6

        # 4. Вращение (Requirements: pygame.transform.rotate)
        self.render_rotated_hand(screen, self.right_hand_surf, angle_min)
        self.render_rotated_hand(screen, self.left_hand_surf, angle_sec)

    def render_rotated_hand(self, screen, hand_surface, angle):
        # Метод из задания: pygame.transform.rotate()
        rotated_img = pygame.transform.rotate(hand_surface, angle)
        # Центрируем повернутое изображение, чтобы ось вращения не смещалась
        rect = rotated_img.get_rect(center=self.center)
        screen.blit(rotated_img, rect)