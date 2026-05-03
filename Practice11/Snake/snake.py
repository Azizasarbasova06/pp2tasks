import pygame
import sys
import random

pygame.init()

# ---------------- SCREEN SETTINGS ----------------
WIDTH, HEIGHT = 600, 600
CELL_SIZE = 30
COLS = WIDTH // CELL_SIZE
ROWS = HEIGHT // CELL_SIZE

# ---------------- COLORS ----------------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 130, 0)
RED = (220, 0, 0)
GRAY = (120, 120, 120)
BLUE = (50, 120, 255)
YELLOW = (255, 215, 0)
PURPLE = (160, 32, 240)

# ---------------- INIT ----------------
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake FINAL")
clock = pygame.time.Clock()

font = pygame.font.SysFont("Verdana", 24)
big_font = pygame.font.SysFont("Verdana", 48)

# ---------------- GAME STATE ----------------
game_state = "menu"   # menu / playing / paused

# ---------------- GAME VARIABLES ----------------
speed = 7
score = 0
level = 1

# ---------------- FOOD VARIABLES ----------------
food = None
food_color = RED
food_weight = 1
food_spawn_time = 0
FOOD_LIFETIME = 5000   # milliseconds (5 seconds)

# ---------------- DIRECTIONS ----------------
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
direction = RIGHT

# ---------------- INITIAL SNAKE ----------------
snake = [(5, 10), (4, 10), (3, 10)]


# ---------------- RESET FUNCTION ----------------
def reset_game():
    """
    Resets all game variables:
    - snake position
    - direction
    - score, level, speed
    - generates new food
    """
    global snake, direction, score, level, speed
    global food, food_color, food_weight, food_spawn_time

    snake = [(5, 10), (4, 10), (3, 10)]
    direction = RIGHT
    score = 0
    level = 1
    speed = 7

    food, food_color, food_weight = generate_food()
    food_spawn_time = pygame.time.get_ticks()


# ---------------- DRAW HELPERS ----------------
def draw_text(text, font_obj, color, x, y):
    """Draws text on screen."""
    screen.blit(font_obj.render(text, True, color), (x, y))


def draw_cell(color, position):
    """Draws one grid cell."""
    x, y = position
    rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, BLACK, rect, 1)


def draw_walls():
    """Draws borders (walls) around the field."""
    for x in range(COLS):
        draw_cell(GRAY, (x, 0))
        draw_cell(GRAY, (x, ROWS - 1))

    for y in range(ROWS):
        draw_cell(GRAY, (0, y))
        draw_cell(GRAY, (COLS - 1, y))


def is_wall(pos):
    """Checks if given position is a wall."""
    x, y = pos
    return x == 0 or x == COLS - 1 or y == 0 or y == ROWS - 1


# ---------------- FOOD GENERATION ----------------
def generate_food():
    """
    Generates random food:
    - must not be inside snake
    - must not be on walls

    Food types:
    red = 1 point
    yellow = 2 points
    purple = 3 points
    """
    while True:
        pos = (random.randint(1, COLS - 2), random.randint(1, ROWS - 2))

        if pos not in snake and not is_wall(pos):

            food_type = random.choice([
                (RED, 1),
                (YELLOW, 2),
                (PURPLE, 3)
            ])

            return pos, food_type[0], food_type[1]


# ---------------- UI SCREENS ----------------
def draw_menu():
    """Main menu."""
    screen.fill(BLACK)

    draw_text("SNAKE", big_font, WHITE, WIDTH//2 - 100, 200)
    draw_text("ENTER - Start", font, WHITE, WIDTH//2 - 100, 300)
    draw_text("ESC - Exit", font, WHITE, WIDTH//2 - 100, 340)

    pygame.display.update()


def draw_pause():
    """Pause overlay."""
    draw_text("PAUSED", big_font, RED, WIDTH//2 - 120, HEIGHT//2 - 30)


def game_over():
    """Game over screen."""
    global game_state

    screen.fill(WHITE)

    draw_text("GAME OVER", big_font, RED, WIDTH//2 - 150, 250)
    draw_text(f"Score: {score}", font, BLACK, WIDTH//2 - 70, 320)

    pygame.display.update()
    pygame.time.delay(2000)

    game_state = "menu"


def draw_hud():
    """Top-left HUD info."""
    draw_text(f"Score: {score}", font, BLUE, 40, 30)
    draw_text(f"Level: {level}", font, BLUE, 40, 60)
    draw_text(f"Food: +{food_weight}", font, BLUE, 40, 90)


# ---------------- INITIAL FOOD ----------------
food, food_color, food_weight = generate_food()
food_spawn_time = pygame.time.get_ticks()


# ---------------- MAIN LOOP ----------------
while True:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:

            # MENU
            if game_state == "menu":
                if event.key == pygame.K_RETURN:
                    reset_game()
                    game_state = "playing"

                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            # PLAYING
            elif game_state == "playing":
                if event.key == pygame.K_ESCAPE:
                    game_state = "paused"

                elif event.key == pygame.K_UP and direction != DOWN:
                    direction = UP
                elif event.key == pygame.K_DOWN and direction != UP:
                    direction = DOWN
                elif event.key == pygame.K_LEFT and direction != RIGHT:
                    direction = LEFT
                elif event.key == pygame.K_RIGHT and direction != LEFT:
                    direction = RIGHT

            # PAUSE
            elif game_state == "paused":
                if event.key == pygame.K_ESCAPE:
                    game_state = "playing"

    # MENU
    if game_state == "menu":
        draw_menu()
        continue

    # PAUSE
    if game_state == "paused":
        draw_pause()
        pygame.display.update()
        continue

    # ---------------- FOOD TIMER ----------------
    current_time = pygame.time.get_ticks()

    # Food disappears if not eaten in time
    if current_time - food_spawn_time > FOOD_LIFETIME:
        food, food_color, food_weight = generate_food()
        food_spawn_time = pygame.time.get_ticks()

    # ---------------- SNAKE MOVEMENT ----------------
    head = snake[0]
    new_head = (head[0] + direction[0], head[1] + direction[1])

    # Border collision
    if new_head[0] < 0 or new_head[0] >= COLS or new_head[1] < 0 or new_head[1] >= ROWS:
        game_over()
        continue

    # Wall or self collision
    if is_wall(new_head) or new_head in snake:
        game_over()
        continue

    snake.insert(0, new_head)

    # ---------------- FOOD COLLISION ----------------
    if new_head == food:
        score += food_weight

        # Level system: every 5 points → level up
        if score // 5 + 1 > level:
            level += 1
            speed += 1   # gradual speed increase

        food, food_color, food_weight = generate_food()
        food_spawn_time = pygame.time.get_ticks()

    else:
        snake.pop()

    # ---------------- DRAW ----------------
    screen.fill(WHITE)
    draw_walls()

    draw_cell(food_color, food)

    for i, segment in enumerate(snake):
        draw_cell(DARK_GREEN if i == 0 else GREEN, segment)

    draw_hud()

    pygame.display.update()
    clock.tick(speed)