import pygame
import sys
import math

pygame.init()

WIDTH, HEIGHT = 900, 600
TOOLBAR_HEIGHT = 90

# COLORS
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
pygame.display.set_caption("Paint PRO")
clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 18)
small_font = pygame.font.SysFont("Arial", 14)

canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill(WHITE)

tool = "brush"
current_color = BLACK
brush_size = 5
eraser_size = 25

drawing = False
start_pos = None
last_pos = None

# COLOR BUTTONS
color_buttons = [
    (BLACK, pygame.Rect(10, 10, 35, 35)),
    (RED, pygame.Rect(50, 10, 35, 35)),
    (GREEN, pygame.Rect(90, 10, 35, 35)),
    (BLUE, pygame.Rect(130, 10, 35, 35)),
    (YELLOW, pygame.Rect(170, 10, 35, 35)),
    (PURPLE, pygame.Rect(210, 10, 35, 35)),
    (ORANGE, pygame.Rect(250, 10, 35, 35)),
]

# TOOL BUTTONS
brush_btn = pygame.Rect(310, 10, 80, 30)
rect_btn = pygame.Rect(400, 10, 80, 30)
circle_btn = pygame.Rect(490, 10, 80, 30)
square_btn = pygame.Rect(580, 10, 80, 30)

right_tri_btn = pygame.Rect(310, 50, 110, 30)
eq_tri_btn = pygame.Rect(430, 50, 110, 30)
rhombus_btn = pygame.Rect(550, 50, 110, 30)

eraser_btn = pygame.Rect(670, 10, 80, 30)

size_up_btn = pygame.Rect(770, 10, 40, 30)
size_down_btn = pygame.Rect(820, 10, 40, 30)

# DRAW BUTTON
def draw_button(rect, text, active=False):
    pygame.draw.rect(screen, DARK_GRAY if active else WHITE, rect)
    pygame.draw.rect(screen, BLACK, rect, 2)
    txt = small_font.render(text, True, BLACK)
    screen.blit(txt, txt.get_rect(center=rect.center))

# SHAPES
def get_rect(start, end):
    return pygame.Rect(min(start[0], end[0]),
                       min(start[1], end[1]),
                       abs(start[0]-end[0]),
                       abs(start[1]-end[1]))

def get_square(start, end):
    size = max(abs(end[0]-start[0]), abs(end[1]-start[1]))
    return pygame.Rect(start[0], start[1], size, size)

def get_right_triangle(start, end):
    return [start, (start[0], end[1]), end]

def get_equilateral_triangle(start, end):
    size = abs(end[0]-start[0])
    h = int(size * math.sqrt(3)/2)
    return [
        (start[0], start[1]+h),
        (start[0]+size//2, start[1]),
        (start[0]+size, start[1]+h)
    ]

def get_rhombus(start, end):
    cx = (start[0]+end[0])//2
    cy = (start[1]+end[1])//2
    return [(cx,start[1]), (end[0],cy), (cx,end[1]), (start[0],cy)]

def draw_brush(surface, color, start, end, size):
    dx = end[0]-start[0]
    dy = end[1]-start[1]
    steps = max(abs(dx), abs(dy))
    for i in range(steps+1):
        x = int(start[0] + dx*i/steps)
        y = int(start[1] + dy*i/steps)
        pygame.draw.circle(surface, color, (x,y), size)

# LOOP
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # HOTKEYS
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                brush_size += 1
                eraser_size += 2
            elif event.key == pygame.K_DOWN:
                brush_size = max(1, brush_size - 1)
                eraser_size = max(5, eraser_size - 2)

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos

            if pos[1] <= TOOLBAR_HEIGHT:
                # COLORS
                for c, r in color_buttons:
                    if r.collidepoint(pos):
                        current_color = c

                # TOOLS
                if brush_btn.collidepoint(pos): tool = "brush"
                elif rect_btn.collidepoint(pos): tool = "rectangle"
                elif circle_btn.collidepoint(pos): tool = "circle"
                elif square_btn.collidepoint(pos): tool = "square"
                elif right_tri_btn.collidepoint(pos): tool = "right_triangle"
                elif eq_tri_btn.collidepoint(pos): tool = "equ_triangle"
                elif rhombus_btn.collidepoint(pos): tool = "rhombus"
                elif eraser_btn.collidepoint(pos): tool = "eraser"

                # SIZE
                elif size_up_btn.collidepoint(pos):
                    brush_size += 1
                    eraser_size += 2

                elif size_down_btn.collidepoint(pos):
                    brush_size = max(1, brush_size - 1)
                    eraser_size = max(5, eraser_size - 2)

            else:
                drawing = True
                start_pos = pos
                last_pos = pos

        if event.type == pygame.MOUSEBUTTONUP:
            if drawing:
                end = event.pos

                if tool == "rectangle":
                    pygame.draw.rect(canvas, current_color, get_rect(start_pos, end), 3)

                elif tool == "circle":
                    r = int(((end[0]-start_pos[0])**2 + (end[1]-start_pos[1])**2)**0.5)
                    pygame.draw.circle(canvas, current_color, start_pos, r, 3)

                elif tool == "square":
                    pygame.draw.rect(canvas, current_color, get_square(start_pos, end), 3)

                elif tool == "right_triangle":
                    pygame.draw.polygon(canvas, current_color, get_right_triangle(start_pos, end), 3)

                elif tool == "equ_triangle":
                    pygame.draw.polygon(canvas, current_color, get_equilateral_triangle(start_pos, end), 3)

                elif tool == "rhombus":
                    pygame.draw.polygon(canvas, current_color, get_rhombus(start_pos, end), 3)

            drawing = False

        if event.type == pygame.MOUSEMOTION and drawing:
            if tool == "brush":
                draw_brush(canvas, current_color, last_pos, event.pos, brush_size)
                last_pos = event.pos

            elif tool == "eraser":
                draw_brush(canvas, WHITE, last_pos, event.pos, eraser_size)
                last_pos = event.pos

    screen.blit(canvas, (0, 0))

    # PREVIEW
    if drawing:
        cur = pygame.mouse.get_pos()

        if tool == "rectangle":
            pygame.draw.rect(screen, current_color, get_rect(start_pos, cur), 2)

        elif tool == "circle":
            r = int(((cur[0]-start_pos[0])**2 + (cur[1]-start_pos[1])**2)**0.5)
            pygame.draw.circle(screen, current_color, start_pos, r, 2)

        elif tool == "square":
            pygame.draw.rect(screen, current_color, get_square(start_pos, cur), 2)

        elif tool == "right_triangle":
            pygame.draw.polygon(screen, current_color, get_right_triangle(start_pos, cur), 2)

        elif tool == "equ_triangle":
            pygame.draw.polygon(screen, current_color, get_equilateral_triangle(start_pos, cur), 2)

        elif tool == "rhombus":
            pygame.draw.polygon(screen, current_color, get_rhombus(start_pos, cur), 2)

    # TOOLBAR
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, TOOLBAR_HEIGHT))

    for c, r in color_buttons:
        pygame.draw.rect(screen, c, r)
        pygame.draw.rect(screen, BLACK, r, 2)

    draw_button(brush_btn, "Brush", tool=="brush")
    draw_button(rect_btn, "Rect", tool=="rectangle")
    draw_button(circle_btn, "Circle", tool=="circle")
    draw_button(square_btn, "Square", tool=="square")

    draw_button(right_tri_btn, "RightTri", tool=="right_triangle")
    draw_button(eq_tri_btn, "EquTri", tool=="equ_triangle")
    draw_button(rhombus_btn, "Rhombus", tool=="rhombus")

    draw_button(eraser_btn, "Eraser", tool=="eraser")

    draw_button(size_up_btn, "+")
    draw_button(size_down_btn, "-")

    # SIZE INFO
    info = font.render(f"Size: {brush_size}", True, BLACK)
    screen.blit(info, (750, 50))

    pygame.display.flip()
    clock.tick(60)