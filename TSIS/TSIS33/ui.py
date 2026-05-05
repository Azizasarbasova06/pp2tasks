import pygame

WIDTH, HEIGHT = 900, 720
BG = (18, 19, 30)
PANEL = (32, 34, 49)
WHITE = (235, 235, 235)
YELLOW = (255, 215, 64)
GRAY = (90, 94, 115)
GREEN = (35, 135, 60)
RED = (220, 65, 65)

pygame.font.init()
FONT = pygame.font.SysFont("arial", 26)
SMALL = pygame.font.SysFont("arial", 20)
BIG = pygame.font.SysFont("arial", 44, bold=True)

class Button:
    def __init__(self, rect, text):
        self.rect = pygame.Rect(rect)
        self.text = text

    def draw(self, screen):
        pygame.draw.rect(screen, (62, 67, 92), self.rect, border_radius=12)
        pygame.draw.rect(screen, (160, 165, 190), self.rect, 2, border_radius=12)
        surf = FONT.render(self.text, True, WHITE)
        screen.blit(surf, surf.get_rect(center=self.rect.center))

    def clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos)

def draw_text(screen, text, x, y, font=FONT, color=WHITE, center=False):
    surf = font.render(str(text), True, color)
    rect = surf.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(surf, rect)
    return rect

def draw_title(screen, title):
    draw_text(screen, title, WIDTH // 2, 95, BIG, YELLOW, center=True)

def draw_screen_background(screen):
    screen.fill(BG)
