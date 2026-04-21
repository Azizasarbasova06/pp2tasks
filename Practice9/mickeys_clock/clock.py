import pygame
import datetime
import sys

class MickeyClock:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        # Центр экрана, вокруг которого будем всё вращать
        self.center = (width // 2, height // 2)
        
        # 1. Загружаем фон
        try:
            # Используем convert_alpha() для поддержки прозрачности, если фон PNG
            self.main_img = pygame.image.load("images/mickey.jpeg").convert_alpha()
            self.main_img = pygame.transform.scale(self.main_img, (width, height))
        except:
            # Если картинки нет, создаем белый фон
            self.main_img = pygame.Surface((width, height))
            self.main_img.fill((255, 255, 255))
            print("Ошибка: mickey.jpeg не найден!")

        # 2. ЗАГРУЖАЕМ ТВОЮ НОВУЮ РУКУ (Requirement: Use Mickey's hand graphics)
        try:
            # Загружаем твой новый файл (используем тот, что ты скинула последним)
            self.hand_orig = pygame.image.load("images/righthand-removebg-preview.png").convert_alpha()
            
            # --- ИСПРАВЛЕНИЕ: МЫ БОЛЬШЕ НЕ ВРАЩАЕМ ЕЁ ЗДЕСЬ ---
            # Это создавало проблемы с размером.
            
            # --- ИСПРАВЛЕНИЕ: УВЕЛИЧИВАЕМ РАЗМЕР ---
            # Твои часы 800x800, поэтому 50x180 было слишком мало.
            # Давай попробуем ширину 100 и высоту 300.
            # Это должно сделать руку заметной.
            self.hand_orig = pygame.transform.scale(self.hand_orig, (70, 200))
            
        except:
            print("Ошибка: Картинки рук (images/righthand-removebg-preview.png) не найдены!")
            pygame.quit()
            sys.exit()

    def draw(self, screen):
        # Отрисовка фона (циферблата)
        screen.blit(self.main_img, (0, 0))

        # Получаем текущее системное время (Real-time synchronization)
        now = datetime.datetime.now()
        minutes = now.minute
        seconds = now.second

        # 3. РАСЧЕТ УГЛОВ (Calculate rotation angles)
        # В Pygame "+" - вращение ПРОТИВ часовой стрелки, поэтому используем минус,
        # чтобы стрелки шли ПО часовой.
        # angle = -(время * 6)
        angle_min = -minutes * 6
        angle_sec = -seconds * 6

        # 4. ВРАЩЕНИЕ И ОТРЕСОВКА (Requirements: pygame.transform.rotate)
        # Вращаем и рисуем обе руки. Поскольку мы используем одну и ту же 
        # картинку для обеих рук, они будут одинакового размера.
        self.render_hand(screen, self.hand_orig, angle_min) # Минутная
        self.render_hand(screen, self.hand_orig, angle_sec) # Секундная

    def render_hand(self, screen, hand_surface, angle):
        # 1. Поворачиваем картинку
        rotated_hand = pygame.transform.rotate(hand_surface, angle)
        
        # 2. РАСЧЕТ ТОЧКИ ВРАЩЕНИЯ:
        # Чтобы рука не "летала", нам нужно сместить центр вращения к основанию руки.
        # Мы создаем вектор, который указывает от центра картинки к её нижнему краю.
        # Попробуй менять число 2 (например на 1.5 или 2.5), если рука слишком высоко или низко.
        offset = pygame.math.Vector2(0, -hand_surface.get_height() // 2)
        
        # Поворачиваем вектор смещения вслед за рукой
        rotated_offset = offset.rotate(-angle)
        
        # 3. Устанавливаем положение: 
        # Центр часов (self.center) + повернутый вектор смещения.
        rect = rotated_hand.get_rect(center=self.center + rotated_offset)
        
        # 4. Рисуем
        screen.blit(rotated_hand, rect)