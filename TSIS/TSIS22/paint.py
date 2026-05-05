import pygame
from datetime import datetime
from pathlib import Path

from tools import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    TOOLBAR_HEIGHT,
    COLORS,
    BRUSH_SIZES,
    Tool,
    Button,
    flood_fill,
    draw_shape,
    save_canvas,
)


pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("TSIS2 Paint")

font = pygame.font.SysFont("arial", 18)
small_font = pygame.font.SysFont("arial", 14)
text_font = pygame.font.SysFont("arial", 28)

canvas = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT - TOOLBAR_HEIGHT))
canvas.fill((255, 255, 255))

clock = pygame.time.Clock()

current_tool = Tool.PENCIL
current_color = (0, 0, 0)
current_brush_size = BRUSH_SIZES["medium"]

drawing = False
start_pos = None
last_pos = None
preview_pos = None

text_active = False
text_pos = None
text_buffer = ""

status_message = "Ready"


tool_buttons = [
    Button(10, 10, 82, 30, "Pencil", Tool.PENCIL),
    Button(100, 10, 70, 30, "Line", Tool.LINE),
    Button(178, 10, 70, 30, "Rect", Tool.RECTANGLE),
    Button(256, 10, 70, 30, "Circle", Tool.CIRCLE),
    Button(334, 10, 70, 30, "Square", Tool.SQUARE),
    Button(412, 10, 72, 30, "R.Tri", Tool.RIGHT_TRIANGLE),
    Button(492, 10, 72, 30, "E.Tri", Tool.EQUILATERAL_TRIANGLE),
    Button(572, 10, 82, 30, "Rhombus", Tool.RHOMBUS),
    Button(662, 10, 70, 30, "Eraser", Tool.ERASER),
    Button(740, 10, 60, 30, "Fill", Tool.FILL),
    Button(808, 10, 60, 30, "Text", Tool.TEXT),
]

size_buttons = [
    Button(885, 10, 35, 30, "1", 2),
    Button(925, 10, 35, 30, "2", 5),
    Button(965, 10, 35, 30, "3", 10),
]

color_buttons = []
x = 10
for color in COLORS:
    color_buttons.append(Button(x, 50, 30, 30, "", color))
    x += 38


def to_canvas_pos(pos):
    return pos[0], pos[1] - TOOLBAR_HEIGHT


def on_canvas(pos):
    return pos[1] >= TOOLBAR_HEIGHT


def draw_toolbar():
    pygame.draw.rect(screen, (235, 235, 235), (0, 0, WINDOW_WIDTH, TOOLBAR_HEIGHT))
    pygame.draw.line(screen, (180, 180, 180), (0, TOOLBAR_HEIGHT - 1), (WINDOW_WIDTH, TOOLBAR_HEIGHT - 1), 2)

    for button in tool_buttons:
        selected = button.value == current_tool
        button.draw(screen, font, selected=selected)

    for button in size_buttons:
        selected = button.value == current_brush_size
        button.draw(screen, font, selected=selected)

    for button in color_buttons:
        selected = button.value == current_color
        button.draw_color(screen, selected=selected)

    pygame.draw.rect(screen, current_color, (850, 52, 42, 26))
    pygame.draw.rect(screen, (0, 0, 0), (850, 52, 42, 26), 2)

    pygame.draw.circle(screen, (0, 0, 0), (935, 65), current_brush_size)
    pygame.draw.circle(screen, current_color, (935, 65), max(1, current_brush_size - 1))

    help_text = "Keys: 1/2/3 size | Ctrl+S save | Text: Enter confirm, Esc cancel"
    status = f"{current_tool.value} | brush {current_brush_size}px | {status_message}"
    screen.blit(small_font.render(help_text, True, (30, 30, 30)), (10, 86))
    screen.blit(small_font.render(status, True, (30, 30, 30)), (600, 86))


def draw_text_preview():
    if not text_active or text_pos is None:
        return

    x, y = text_pos
    preview_text = text_buffer + "|"
    rendered = text_font.render(preview_text, True, current_color)
    screen.blit(rendered, (x, y + TOOLBAR_HEIGHT))


def draw_live_preview():
    if not drawing or start_pos is None or preview_pos is None:
        return

    if current_tool in {
        Tool.LINE,
        Tool.RECTANGLE,
        Tool.CIRCLE,
        Tool.SQUARE,
        Tool.RIGHT_TRIANGLE,
        Tool.EQUILATERAL_TRIANGLE,
        Tool.RHOMBUS,
    }:
        draw_shape(
            screen,
            current_tool,
            current_color,
            current_brush_size,
            (start_pos[0], start_pos[1] + TOOLBAR_HEIGHT),
            (preview_pos[0], preview_pos[1] + TOOLBAR_HEIGHT),
        )


def handle_toolbar_click(pos):
    global current_tool, current_color, current_brush_size

    for button in tool_buttons:
        if button.collidepoint(pos):
            current_tool = button.value
            return True

    for button in size_buttons:
        if button.collidepoint(pos):
            current_brush_size = button.value
            return True

    for button in color_buttons:
        if button.collidepoint(pos):
            current_color = button.value
            return True

    return False


running = True

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s and (event.mod & pygame.KMOD_CTRL):
                filename = save_canvas(canvas)
                status_message = f"Saved {filename}"

            elif event.key == pygame.K_1:
                current_brush_size = BRUSH_SIZES["small"]
            elif event.key == pygame.K_2:
                current_brush_size = BRUSH_SIZES["medium"]
            elif event.key == pygame.K_3:
                current_brush_size = BRUSH_SIZES["large"]

            elif text_active:
                if event.key == pygame.K_RETURN:
                    if text_buffer:
                        rendered = text_font.render(text_buffer, True, current_color)
                        canvas.blit(rendered, text_pos)
                    text_active = False
                    text_pos = None
                    text_buffer = ""
                    status_message = "Text confirmed"

                elif event.key == pygame.K_ESCAPE:
                    text_active = False
                    text_pos = None
                    text_buffer = ""
                    status_message = "Text cancelled"

                elif event.key == pygame.K_BACKSPACE:
                    text_buffer = text_buffer[:-1]

                else:
                    if event.unicode and event.unicode.isprintable():
                        text_buffer += event.unicode

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button != 1:
                continue

            pos = event.pos

            if pos[1] < TOOLBAR_HEIGHT:
                handle_toolbar_click(pos)
                continue

            canvas_pos = to_canvas_pos(pos)

            if current_tool == Tool.FILL:
                flood_fill(canvas, canvas_pos, current_color)
                status_message = "Flood fill applied"

            elif current_tool == Tool.TEXT:
                text_active = True
                text_pos = canvas_pos
                text_buffer = ""
                status_message = "Typing text"

            elif current_tool in {Tool.PENCIL, Tool.ERASER}:
                drawing = True
                last_pos = canvas_pos
                draw_color = (255, 255, 255) if current_tool == Tool.ERASER else current_color
                pygame.draw.circle(canvas, draw_color, canvas_pos, current_brush_size // 2)

            else:
                drawing = True
                start_pos = canvas_pos
                preview_pos = canvas_pos

        elif event.type == pygame.MOUSEMOTION:
            pos = event.pos

            if not on_canvas(pos):
                continue

            canvas_pos = to_canvas_pos(pos)

            if drawing and current_tool in {Tool.PENCIL, Tool.ERASER} and last_pos is not None:
                draw_color = (255, 255, 255) if current_tool == Tool.ERASER else current_color
                pygame.draw.line(canvas, draw_color, last_pos, canvas_pos, current_brush_size)
                pygame.draw.circle(canvas, draw_color, canvas_pos, current_brush_size // 2)
                last_pos = canvas_pos

            elif drawing:
                preview_pos = canvas_pos

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button != 1:
                continue

            pos = event.pos

            if not drawing:
                continue

            if current_tool in {Tool.PENCIL, Tool.ERASER}:
                drawing = False
                last_pos = None

            elif on_canvas(pos):
                end_pos = to_canvas_pos(pos)
                draw_shape(canvas, current_tool, current_color, current_brush_size, start_pos, end_pos)
                drawing = False
                start_pos = None
                preview_pos = None

    screen.fill((255, 255, 255))
    draw_toolbar()
    screen.blit(canvas, (0, TOOLBAR_HEIGHT))
    draw_live_preview()
    draw_text_preview()

    pygame.display.flip()

pygame.quit()
