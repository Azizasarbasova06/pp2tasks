import pygame
import sys

pygame.init()

WIDTH = 900
HEIGHT = 600
TOOLBAR_HEIGHT = 90

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (210, 210, 210)
DARK_GRAY = (150, 150, 150)
RED = (255, 0, 0)
GREEN = (0, 180, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 215, 0)
PURPLE = (160, 32, 240)
ORANGE = (255, 140, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")
clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 18)
small_font = pygame.font.SysFont("Arial", 15)

canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill(WHITE)

tool = "brush"
current_color = BLACK
brush_size = 5
eraser_size = 25

drawing = False
last_pos = None
start_pos = None

history = []

color_buttons = [
    (BLACK, pygame.Rect(10, 10, 35, 35)),
    (RED, pygame.Rect(50, 10, 35, 35)),
    (GREEN, pygame.Rect(90, 10, 35, 35)),
    (BLUE, pygame.Rect(130, 10, 35, 35)),
    (YELLOW, pygame.Rect(170, 10, 35, 35)),
    (PURPLE, pygame.Rect(210, 10, 35, 35)),
    (ORANGE, pygame.Rect(250, 10, 35, 35)),
]

brush_button = pygame.Rect(310, 10, 80, 35)
rect_button = pygame.Rect(400, 10, 100, 35)
circle_button = pygame.Rect(510, 10, 80, 35)
triangle_button = pygame.Rect(600, 10, 100, 35)
eraser_button = pygame.Rect(710, 10, 80, 35)
fill_button = pygame.Rect(800, 10, 70, 35)

clear_button = pygame.Rect(800, 50, 70, 30)
save_button = pygame.Rect(310, 50, 80, 30)
undo_button = pygame.Rect(400, 50, 80, 30)
size_up_button = pygame.Rect(500, 50, 40, 30)
size_down_button = pygame.Rect(550, 50, 40, 30)


def draw_tool_button(rect, text, active=False):
    color = DARK_GRAY if active else WHITE
    pygame.draw.rect(screen, color, rect, border_radius=6)
    pygame.draw.rect(screen, BLACK, rect, 2, border_radius=6)

    text_surface = small_font.render(text, True, BLACK)
    screen.blit(text_surface, text_surface.get_rect(center=rect.center))


def draw_toolbar():
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, TOOLBAR_HEIGHT))
    pygame.draw.line(screen, BLACK, (0, TOOLBAR_HEIGHT), (WIDTH, TOOLBAR_HEIGHT), 2)

    for color, rect in color_buttons:
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)

    draw_tool_button(brush_button, "Brush", tool == "brush")
    draw_tool_button(rect_button, "Rect", tool == "rectangle")
    draw_tool_button(circle_button, "Circle", tool == "circle")
    draw_tool_button(triangle_button, "Triangle", tool == "triangle")
    draw_tool_button(eraser_button, "Eraser", tool == "eraser")
    draw_tool_button(fill_button, "Fill", tool == "fill")

    draw_tool_button(clear_button, "Clear")
    draw_tool_button(save_button, "Save")
    draw_tool_button(undo_button, "Undo")
    draw_tool_button(size_up_button, "+")
    draw_tool_button(size_down_button, "-")

    info = font.render(f"{tool} | size {brush_size}", True, BLACK)
    screen.blit(info, (10, 60))


def save_history():
    if len(history) > 20:
        history.pop(0)
    history.append(canvas.copy())


def draw_brush(surface, color, start, end, size):
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    steps = max(abs(dx), abs(dy))

    for i in range(steps + 1):
        x = int(start[0] + dx * i / steps)
        y = int(start[1] + dy * i / steps)
        pygame.draw.circle(surface, color, (x, y), size)


def get_rect(start, end):
    return pygame.Rect(
        min(start[0], end[0]),
        min(start[1], end[1]),
        abs(start[0] - end[0]),
        abs(start[1] - end[1])
    )


def get_triangle(start, end):
    return [
        (start[0], end[1]),                 # левый низ
        ((start[0] + end[0]) // 2, start[1]),  # верх
        (end[0], end[1])                   # правый низ
    ]


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                brush_size += 1
            elif event.key == pygame.K_DOWN:
                brush_size = max(1, brush_size - 1)
            elif event.key == pygame.K_s:
                pygame.image.save(canvas, "drawing.png")
            elif event.key == pygame.K_z and history:
                canvas = history.pop()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos

            if mouse_pos[1] <= TOOLBAR_HEIGHT:
                for color, rect in color_buttons:
                    if rect.collidepoint(mouse_pos):
                        current_color = color

                if brush_button.collidepoint(mouse_pos):
                    tool = "brush"
                elif rect_button.collidepoint(mouse_pos):
                    tool = "rectangle"
                elif circle_button.collidepoint(mouse_pos):
                    tool = "circle"
                elif triangle_button.collidepoint(mouse_pos):
                    tool = "triangle"
                elif eraser_button.collidepoint(mouse_pos):
                    tool = "eraser"
                elif fill_button.collidepoint(mouse_pos):
                    tool = "fill"
                elif clear_button.collidepoint(mouse_pos):
                    save_history()
                    canvas.fill(WHITE)
                elif save_button.collidepoint(mouse_pos):
                    pygame.image.save(canvas, "drawing.png")
                elif undo_button.collidepoint(mouse_pos) and history:
                    canvas = history.pop()
                elif size_up_button.collidepoint(mouse_pos):
                    brush_size += 1
                elif size_down_button.collidepoint(mouse_pos):
                    brush_size = max(1, brush_size - 1)

            else:
                save_history()
                drawing = True
                start_pos = mouse_pos
                last_pos = mouse_pos

                if tool == "fill":
                    canvas.fill(current_color)
                    drawing = False

        if event.type == pygame.MOUSEBUTTONUP:
            if drawing and start_pos:
                end_pos = event.pos

                if tool == "rectangle":
                    pygame.draw.rect(canvas, current_color, get_rect(start_pos, end_pos), 3)

                elif tool == "circle":
                    radius = int(((end_pos[0]-start_pos[0])**2 + (end_pos[1]-start_pos[1])**2)**0.5)
                    pygame.draw.circle(canvas, current_color, start_pos, radius, 3)

                elif tool == "triangle":
                    pygame.draw.polygon(canvas, current_color, get_triangle(start_pos, end_pos), 3)

            drawing = False
            start_pos = None

        if event.type == pygame.MOUSEMOTION and drawing:
            if tool == "brush":
                draw_brush(canvas, current_color, last_pos, event.pos, brush_size)
                last_pos = event.pos
            elif tool == "eraser":
                draw_brush(canvas, WHITE, last_pos, event.pos, eraser_size)
                last_pos = event.pos

    screen.blit(canvas, (0, 0))

    if drawing and start_pos:
        current_pos = pygame.mouse.get_pos()

        if tool == "rectangle":
            pygame.draw.rect(screen, current_color, get_rect(start_pos, current_pos), 2)
        elif tool == "circle":
            radius = int(((current_pos[0]-start_pos[0])**2 + (current_pos[1]-start_pos[1])**2)**0.5)
            pygame.draw.circle(screen, current_color, start_pos, radius, 2)
        elif tool == "triangle":
            pygame.draw.polygon(screen, current_color, get_triangle(start_pos, current_pos), 2)

    draw_toolbar()
    pygame.display.flip()
    clock.tick(60)