import pygame
import sys

# Initialize pygame
pygame.init()

# Window size
WIDTH = 900
HEIGHT = 600
TOOLBAR_HEIGHT = 90

# Colors
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

# Window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")
clock = pygame.time.Clock()

# Fonts
font = pygame.font.SysFont("Arial", 18)
small_font = pygame.font.SysFont("Arial", 15)

# Canvas for drawing
canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill(WHITE)

# Current settings
tool = "brush"
current_color = BLACK
brush_size = 5
eraser_size = 25

drawing = False
last_pos = None
start_pos = None

# For undo
history = []

# Color buttons
color_buttons = [
    (BLACK, pygame.Rect(10, 10, 35, 35)),
    (RED, pygame.Rect(50, 10, 35, 35)),
    (GREEN, pygame.Rect(90, 10, 35, 35)),
    (BLUE, pygame.Rect(130, 10, 35, 35)),
    (YELLOW, pygame.Rect(170, 10, 35, 35)),
    (PURPLE, pygame.Rect(210, 10, 35, 35)),
    (ORANGE, pygame.Rect(250, 10, 35, 35)),
]

# Tool buttons
brush_button = pygame.Rect(310, 10, 80, 35)
rect_button = pygame.Rect(400, 10, 100, 35)
circle_button = pygame.Rect(510, 10, 80, 35)
eraser_button = pygame.Rect(600, 10, 80, 35)
fill_button = pygame.Rect(690, 10, 70, 35)
clear_button = pygame.Rect(770, 10, 70, 35)

save_button = pygame.Rect(310, 50, 80, 30)
undo_button = pygame.Rect(400, 50, 80, 30)
size_up_button = pygame.Rect(500, 50, 40, 30)
size_down_button = pygame.Rect(550, 50, 40, 30)


def draw_tool_button(rect, text, active=False):
    """Draws a button for tools."""
    color = DARK_GRAY if active else WHITE
    pygame.draw.rect(screen, color, rect, border_radius=6)
    pygame.draw.rect(screen, BLACK, rect, 2, border_radius=6)

    text_surface = small_font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)


def draw_toolbar():
    """Draws toolbar with colors, tools and information."""
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, TOOLBAR_HEIGHT))
    pygame.draw.line(screen, BLACK, (0, TOOLBAR_HEIGHT), (WIDTH, TOOLBAR_HEIGHT), 2)

    # Color buttons
    for color, rect in color_buttons:
        pygame.draw.rect(screen, color, rect, border_radius=4)
        if color == current_color:
            pygame.draw.rect(screen, BLACK, rect, 4, border_radius=4)
        else:
            pygame.draw.rect(screen, BLACK, rect, 1, border_radius=4)

    # Tools
    draw_tool_button(brush_button, "Brush", tool == "brush")
    draw_tool_button(rect_button, "Rectangle", tool == "rectangle")
    draw_tool_button(circle_button, "Circle", tool == "circle")
    draw_tool_button(eraser_button, "Eraser", tool == "eraser")
    draw_tool_button(fill_button, "Fill", tool == "fill")
    draw_tool_button(clear_button, "Clear")

    # Extra buttons
    draw_tool_button(save_button, "Save")
    draw_tool_button(undo_button, "Undo")
    draw_tool_button(size_up_button, "+")
    draw_tool_button(size_down_button, "-")

    # Information
    info = font.render(f"Tool: {tool} | Size: {brush_size}", True, BLACK)
    screen.blit(info, (610, 53))

    help_text = small_font.render("UP/DOWN: size | S: save | Z: undo", True, BLACK)
    screen.blit(help_text, (10, 58))


def save_history():
    """Saves canvas state for undo."""
    if len(history) > 20:
        history.pop(0)
    history.append(canvas.copy())


def draw_brush(surface, color, start, end, size):
    """Draws smooth line between two points."""
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    steps = max(abs(dx), abs(dy))

    if steps == 0:
        pygame.draw.circle(surface, color, start, size)
        return

    for i in range(steps + 1):
        x = int(start[0] + dx * i / steps)
        y = int(start[1] + dy * i / steps)
        pygame.draw.circle(surface, color, (x, y), size)


def get_rect(start, end):
    """Creates rectangle from start and end mouse positions."""
    x1 = min(start[0], end[0])
    y1 = min(start[1], end[1])
    x2 = max(start[0], end[0])
    y2 = max(start[1], end[1])
    return pygame.Rect(x1, y1, x2 - x1, y2 - y1)


def get_radius(start, end):
    """Calculates radius for circle."""
    return int(((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2) ** 0.5)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Keyboard shortcuts
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                brush_size += 1

            elif event.key == pygame.K_DOWN:
                brush_size = max(1, brush_size - 1)

            elif event.key == pygame.K_s:
                pygame.image.save(canvas, "drawing.png")

            elif event.key == pygame.K_z and history:
                canvas = history.pop()

        # Mouse click
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos

            # Toolbar click
            if mouse_pos[1] <= TOOLBAR_HEIGHT:
                for color, rect in color_buttons:
                    if rect.collidepoint(mouse_pos):
                        current_color = color
                        tool = "brush"

                if brush_button.collidepoint(mouse_pos):
                    tool = "brush"
                elif rect_button.collidepoint(mouse_pos):
                    tool = "rectangle"
                elif circle_button.collidepoint(mouse_pos):
                    tool = "circle"
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

            # Canvas click
            else:
                save_history()
                drawing = True
                start_pos = mouse_pos
                last_pos = mouse_pos

                if tool == "brush":
                    pygame.draw.circle(canvas, current_color, mouse_pos, brush_size)

                elif tool == "eraser":
                    pygame.draw.circle(canvas, WHITE, mouse_pos, eraser_size)

                elif tool == "fill":
                    canvas.fill(current_color)
                    drawing = False

        # Mouse release
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = event.pos

            if drawing and start_pos is not None:
                if tool == "rectangle":
                    rect = get_rect(start_pos, mouse_pos)
                    pygame.draw.rect(canvas, current_color, rect, 3)

                elif tool == "circle":
                    radius = get_radius(start_pos, mouse_pos)
                    pygame.draw.circle(canvas, current_color, start_pos, radius, 3)

            drawing = False
            last_pos = None
            start_pos = None

        # Mouse movement
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = event.pos

            if drawing and mouse_pos[1] > TOOLBAR_HEIGHT:
                if tool == "brush" and last_pos is not None:
                    draw_brush(canvas, current_color, last_pos, mouse_pos, brush_size)
                    last_pos = mouse_pos

                elif tool == "eraser" and last_pos is not None:
                    draw_brush(canvas, WHITE, last_pos, mouse_pos, eraser_size)
                    last_pos = mouse_pos

    # Draw canvas
    screen.blit(canvas, (0, 0))

    # Preview for rectangle and circle
    if drawing and start_pos is not None:
        current_pos = pygame.mouse.get_pos()

        if current_pos[1] > TOOLBAR_HEIGHT:
            if tool == "rectangle":
                rect = get_rect(start_pos, current_pos)
                pygame.draw.rect(screen, current_color, rect, 3)

            elif tool == "circle":
                radius = get_radius(start_pos, current_pos)
                pygame.draw.circle(screen, current_color, start_pos, radius, 3)

    # Draw toolbar
    draw_toolbar()

    # Cursor preview
    mouse_pos = pygame.mouse.get_pos()
    if mouse_pos[1] > TOOLBAR_HEIGHT:
        if tool == "brush":
            pygame.draw.circle(screen, current_color, mouse_pos, brush_size, 1)
        elif tool == "eraser":
            pygame.draw.circle(screen, BLACK, mouse_pos, eraser_size, 1)

    pygame.display.flip()
    clock.tick(60)