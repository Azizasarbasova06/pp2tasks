import pygame
from enum import Enum
from datetime import datetime
from pathlib import Path
from collections import deque


WINDOW_WIDTH = 1100
WINDOW_HEIGHT = 750
TOOLBAR_HEIGHT = 115

BRUSH_SIZES = {
    "small": 2,
    "medium": 5,
    "large": 10,
}

COLORS = [
    (0, 0, 0),
    (80, 80, 80),
    (255, 255, 255),
    (255, 0, 0),
    (255, 128, 0),
    (255, 255, 0),
    (0, 180, 0),
    (0, 120, 255),
    (0, 0, 180),
    (140, 0, 200),
    (255, 0, 150),
    (120, 70, 30),
]


class Tool(Enum):
    PENCIL = "Pencil"
    LINE = "Line"
    RECTANGLE = "Rectangle"
    CIRCLE = "Circle"
    SQUARE = "Square"
    RIGHT_TRIANGLE = "Right triangle"
    EQUILATERAL_TRIANGLE = "Equilateral triangle"
    RHOMBUS = "Rhombus"
    ERASER = "Eraser"
    FILL = "Fill"
    TEXT = "Text"


class Button:
    def __init__(self, x, y, width, height, label, value):
        self.rect = pygame.Rect(x, y, width, height)
        self.label = label
        self.value = value

    def collidepoint(self, pos):
        return self.rect.collidepoint(pos)

    def draw(self, surface, font, selected=False):
        fill = (205, 225, 255) if selected else (250, 250, 250)
        border = (20, 90, 180) if selected else (120, 120, 120)

        pygame.draw.rect(surface, fill, self.rect, border_radius=6)
        pygame.draw.rect(surface, border, self.rect, 2, border_radius=6)

        text = font.render(self.label, True, (20, 20, 20))
        text_rect = text.get_rect(center=self.rect.center)
        surface.blit(text, text_rect)

    def draw_color(self, surface, selected=False):
        pygame.draw.rect(surface, self.value, self.rect)
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 3 if selected else 1)


def normalize_rect(start, end):
    x1, y1 = start
    x2, y2 = end
    return pygame.Rect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))


def draw_shape(surface, tool, color, brush_size, start, end):
    if start is None or end is None:
        return

    if tool == Tool.LINE:
        pygame.draw.line(surface, color, start, end, brush_size)

    elif tool == Tool.RECTANGLE:
        rect = normalize_rect(start, end)
        pygame.draw.rect(surface, color, rect, brush_size)

    elif tool == Tool.CIRCLE:
        rect = normalize_rect(start, end)
        if rect.width > 0 and rect.height > 0:
            pygame.draw.ellipse(surface, color, rect, brush_size)

    elif tool == Tool.SQUARE:
        x1, y1 = start
        x2, y2 = end
        side = min(abs(x2 - x1), abs(y2 - y1))
        x = x1 if x2 >= x1 else x1 - side
        y = y1 if y2 >= y1 else y1 - side
        rect = pygame.Rect(x, y, side, side)
        pygame.draw.rect(surface, color, rect, brush_size)

    elif tool == Tool.RIGHT_TRIANGLE:
        x1, y1 = start
        x2, y2 = end
        points = [(x1, y1), (x1, y2), (x2, y2)]
        pygame.draw.polygon(surface, color, points, brush_size)

    elif tool == Tool.EQUILATERAL_TRIANGLE:
        x1, y1 = start
        x2, y2 = end
        width = x2 - x1
        height = abs(width) * 0.866
        direction = 1 if y2 >= y1 else -1

        top = (x1 + width / 2, y1)
        left = (x1, y1 + direction * height)
        right = (x2, y1 + direction * height)
        points = [(int(top[0]), int(top[1])), (int(left[0]), int(left[1])), (int(right[0]), int(right[1]))]
        pygame.draw.polygon(surface, color, points, brush_size)

    elif tool == Tool.RHOMBUS:
        x1, y1 = start
        x2, y2 = end
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2
        points = [(cx, y1), (x2, cy), (cx, y2), (x1, cy)]
        pygame.draw.polygon(surface, color, points, brush_size)


def flood_fill(surface, start_pos, fill_color):
    width, height = surface.get_size()
    x, y = start_pos

    if not (0 <= x < width and 0 <= y < height):
        return

    target_color = surface.get_at((x, y))
    fill_color = pygame.Color(*fill_color)

    if target_color == fill_color:
        return

    queue = deque([(x, y)])
    visited = set()

    while queue:
        px, py = queue.popleft()

        if (px, py) in visited:
            continue

        if not (0 <= px < width and 0 <= py < height):
            continue

        if surface.get_at((px, py)) != target_color:
            continue

        surface.set_at((px, py), fill_color)
        visited.add((px, py))

        queue.append((px + 1, py))
        queue.append((px - 1, py))
        queue.append((px, py + 1))
        queue.append((px, py - 1))


def save_canvas(canvas):
    saves_dir = Path("saves")
    saves_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = saves_dir / f"paint_{timestamp}.png"

    pygame.image.save(canvas, str(filename))
    return str(filename)
