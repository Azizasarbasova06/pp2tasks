import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 600, 600
CELL_SIZE = 30
COLS = WIDTH // CELL_SIZE
ROWS = HEIGHT // CELL_SIZE

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 130, 0)
RED = (220, 0, 0)
GRAY = (120, 120, 120)
BLUE = (50, 120, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()

font = pygame.font.SysFont("Verdana", 24)
big_font = pygame.font.SysFont("Verdana", 48)

# Состояние игры
game_state = "menu"   # menu / playing / paused

# Начальные параметры
speed = 7
score = 0
level = 1

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
direction = RIGHT

snake = [(5, 10), (4, 10), (3, 10)]
food = None


def reset_game():
    global snake, direction, score, level, speed, food
    snake = [(5, 10), (4, 10), (3, 10)]
    direction = RIGHT
    score = 0
    level = 1
    speed = 7
    food = generate_food()


def draw_text(text, font_obj, color, x, y):
    screen.blit(font_obj.render(text, True, color), (x, y))


def draw_cell(color, position):
    x, y = position
    rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, BLACK, rect, 1)


def draw_walls():
    for x in range(COLS):
        draw_cell(GRAY, (x, 0))
        draw_cell(GRAY, (x, ROWS - 1))
    for y in range(ROWS):
        draw_cell(GRAY, (0, y))
        draw_cell(GRAY, (COLS - 1, y))


def is_wall(pos):
    x, y = pos
    return x == 0 or x == COLS - 1 or y == 0 or y == ROWS - 1


def generate_food():
    while True:
        pos = (random.randint(1, COLS - 2), random.randint(1, ROWS - 2))
        if pos not in snake and not is_wall(pos):
            return pos


def draw_menu():
    screen.fill(BLACK)
    draw_text("SNAKE", big_font, WHITE, 200, 200)
    draw_text("ENTER - Start", font, WHITE, 200, 300)
    draw_text("ESC - Exit", font, WHITE, 200, 340)
    pygame.display.update()


def draw_pause():
    draw_text("PAUSED", big_font, RED, 200, 250)


def game_over():
    global game_state
    screen.fill(WHITE)
    draw_text("Game Over", big_font, RED, 170, 250)
    draw_text(f"Score: {score}", font, BLACK, 240, 320)
    pygame.display.update()
    pygame.time.delay(2000)
    game_state = "menu"


# первая еда
food = generate_food()

# главный цикл
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:

            if game_state == "menu":
                if event.key == pygame.K_RETURN:
                    reset_game()
                    game_state = "playing"
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            elif game_state == "playing":
                if event.key == pygame.K_ESCAPE:
                    game_state = "paused"

                if event.key == pygame.K_UP and direction != DOWN:
                    direction = UP
                elif event.key == pygame.K_DOWN and direction != UP:
                    direction = DOWN
                elif event.key == pygame.K_LEFT and direction != RIGHT:
                    direction = LEFT
                elif event.key == pygame.K_RIGHT and direction != LEFT:
                    direction = RIGHT

            elif game_state == "paused":
                if event.key == pygame.K_ESCAPE:
                    game_state = "playing"

    # МЕНЮ
    if game_state == "menu":
        draw_menu()
        continue

    # ПАУЗА
    if game_state == "paused":
        draw_pause()
        pygame.display.update()
        continue

    # === ИГРА ===

    head = snake[0]
    new_head = (head[0] + direction[0], head[1] + direction[1])

    if new_head[0] < 0 or new_head[0] >= COLS or new_head[1] < 0 or new_head[1] >= ROWS:
        game_over()

    if is_wall(new_head) or new_head in snake:
        game_over()

    snake.insert(0, new_head)

    if new_head == food:
        score += 1
        if score % 3 == 0:
            level += 1
            speed += 2
        food = generate_food()
    else:
        snake.pop()

    screen.fill(WHITE)
    draw_walls()
    draw_cell(RED, food)

    for i, segment in enumerate(snake):
        draw_cell(DARK_GREEN if i == 0 else GREEN, segment)

    draw_text(f"Score: {score}", font, BLUE, 10, 10)
    draw_text(f"Level: {level}", font, BLUE, 10, 40)

    pygame.display.update()
    clock.tick(speed)