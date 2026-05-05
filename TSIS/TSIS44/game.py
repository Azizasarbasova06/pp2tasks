import random
from collections import deque

import pygame

from ui import WIDTH, HEIGHT, draw_text, draw_center_text


CELL_SIZE = 20
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE

TOP_MARGIN_CELLS = 3

NORMAL_FOOD = "normal"
POISON_FOOD = "poison"

POWER_SPEED = "Speed boost"
POWER_SLOW = "Slow motion"
POWER_SHIELD = "Shield"


class SnakeGame:
    def __init__(self, screen, clock, settings, username, personal_best):
        self.screen = screen
        self.clock = clock
        self.settings = settings
        self.username = username
        self.personal_best = personal_best

        self.font = pygame.font.SysFont("arial", 20)
        self.big_font = pygame.font.SysFont("arial", 32, bold=True)

        self.snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)
        self.next_direction = (1, 0)

        self.score = 0
        self.level = 1
        self.food_eaten = 0
        self.speed = 8

        self.food = None
        self.poison = None
        self.powerup = None
        self.active_power = None
        self.power_end_time = 0
        self.shield = False

        self.obstacles = set()

        self.running = True
        self.game_over = False

        self.spawn_food()
        self.spawn_poison()

    def occupied_cells(self):
        occupied = set(self.snake)
        occupied.update(self.obstacles)

        if self.food:
            occupied.add(self.food["pos"])
        if self.poison:
            occupied.add(self.poison["pos"])
        if self.powerup:
            occupied.add(self.powerup["pos"])

        return occupied

    def random_empty_cell(self, exclude_current_items=False):
        occupied = set(self.snake)
        occupied.update(self.obstacles)

        if exclude_current_items:
            if self.food:
                occupied.add(self.food["pos"])
            if self.poison:
                occupied.add(self.poison["pos"])
            if self.powerup:
                occupied.add(self.powerup["pos"])

        while True:
            cell = (
                random.randint(1, GRID_WIDTH - 2),
                random.randint(TOP_MARGIN_CELLS + 1, GRID_HEIGHT - 2),
            )
            if cell not in occupied:
                return cell

    def spawn_food(self):
        value = random.choices([1, 3, 5], weights=[70, 23, 7])[0]
        self.food = {
            "pos": self.random_empty_cell(True),
            "value": value,
            "expires_at": pygame.time.get_ticks() + random.randint(5000, 9000),
        }

    def spawn_poison(self):
        if random.random() < 0.75:
            self.poison = {
                "pos": self.random_empty_cell(True),
                "expires_at": pygame.time.get_ticks() + random.randint(6000, 10000),
            }

    def spawn_powerup(self):
        if self.powerup is not None:
            return

        kind = random.choice([POWER_SPEED, POWER_SLOW, POWER_SHIELD])
        self.powerup = {
            "pos": self.random_empty_cell(True),
            "kind": kind,
            "expires_at": pygame.time.get_ticks() + 8000,
        }

    def regenerate_obstacles_for_level(self):
        if self.level < 3:
            self.obstacles = set()
            return

        snake_head = self.snake[0]
        protected = {
            snake_head,
            (snake_head[0] + 1, snake_head[1]),
            (snake_head[0] - 1, snake_head[1]),
            (snake_head[0], snake_head[1] + 1),
            (snake_head[0], snake_head[1] - 1),
            (snake_head[0] + 2, snake_head[1]),
            (snake_head[0] - 2, snake_head[1]),
            (snake_head[0], snake_head[1] + 2),
            (snake_head[0], snake_head[1] - 2),
        }

        count = min(6 + self.level * 2, 35)
        obstacles = set()

        attempts = 0
        while len(obstacles) < count and attempts < 2000:
            attempts += 1
            cell = (
                random.randint(2, GRID_WIDTH - 3),
                random.randint(TOP_MARGIN_CELLS + 2, GRID_HEIGHT - 3),
            )

            if cell in protected or cell in self.snake:
                continue

            obstacles.add(cell)

            if not self.path_has_escape(snake_head, obstacles):
                obstacles.remove(cell)

        self.obstacles = obstacles

    def path_has_escape(self, start, obstacles):
        targets_needed = 12
        visited = set()
        queue = deque([start])

        while queue and len(visited) < targets_needed:
            cell = queue.popleft()

            if cell in visited:
                continue

            x, y = cell
            if (
                x <= 0
                or x >= GRID_WIDTH - 1
                or y <= TOP_MARGIN_CELLS
                or y >= GRID_HEIGHT - 1
                or cell in obstacles
            ):
                continue

            visited.add(cell)

            queue.append((x + 1, y))
            queue.append((x - 1, y))
            queue.append((x, y + 1))
            queue.append((x, y - 1))

        return len(visited) >= targets_needed

    def activate_powerup(self, kind):
        now = pygame.time.get_ticks()

        if kind == POWER_SPEED:
            self.active_power = POWER_SPEED
            self.power_end_time = now + 5000

        elif kind == POWER_SLOW:
            self.active_power = POWER_SLOW
            self.power_end_time = now + 5000

        elif kind == POWER_SHIELD:
            self.active_power = POWER_SHIELD
            self.shield = True
            self.power_end_time = 0

    def effective_speed(self):
        speed = self.speed

        if self.active_power == POWER_SPEED:
            speed += 5
        elif self.active_power == POWER_SLOW:
            speed = max(4, speed - 4)

        return speed

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.game_over = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    self.game_over = True

                elif event.key in (pygame.K_UP, pygame.K_w):
                    if self.direction != (0, 1):
                        self.next_direction = (0, -1)

                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    if self.direction != (0, -1):
                        self.next_direction = (0, 1)

                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    if self.direction != (1, 0):
                        self.next_direction = (-1, 0)

                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    if self.direction != (-1, 0):
                        self.next_direction = (1, 0)

    def collision_is_fatal(self):
        if self.shield:
            self.shield = False
            self.active_power = None
            return False
        return True

    def move(self):
        self.direction = self.next_direction

        head_x, head_y = self.snake[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        hit_wall = (
            new_head[0] <= 0
            or new_head[0] >= GRID_WIDTH - 1
            or new_head[1] <= TOP_MARGIN_CELLS
            or new_head[1] >= GRID_HEIGHT - 1
        )

        hit_self = new_head in self.snake
        hit_obstacle = new_head in self.obstacles

        if hit_wall or hit_self or hit_obstacle:
            if self.collision_is_fatal():
                self.running = False
                self.game_over = True
                return

            # Shield saves one collision by cancelling this movement.
            return

        self.snake.insert(0, new_head)

        ate_food = self.food and new_head == self.food["pos"]
        ate_poison = self.poison and new_head == self.poison["pos"]
        ate_powerup = self.powerup and new_head == self.powerup["pos"]

        if ate_food:
            self.score += self.food["value"] * 10
            self.food_eaten += 1

            if self.food_eaten % 4 == 0:
                self.level += 1
                self.speed += 1
                self.regenerate_obstacles_for_level()

            self.spawn_food()

        elif ate_poison:
            self.poison = None
            self.snake = self.snake[:max(1, len(self.snake) - 2)]
            self.score = max(0, self.score - 15)

            if len(self.snake) <= 1:
                self.running = False
                self.game_over = True
                return

            self.spawn_poison()

        elif ate_powerup:
            self.activate_powerup(self.powerup["kind"])
            self.powerup = None
            self.snake.pop()

        else:
            self.snake.pop()

    def update_timers(self):
        now = pygame.time.get_ticks()

        if self.food and now >= self.food["expires_at"]:
            self.spawn_food()

        if self.poison and now >= self.poison["expires_at"]:
            self.poison = None
            if random.random() < 0.65:
                self.spawn_poison()

        if self.powerup and now >= self.powerup["expires_at"]:
            self.powerup = None

        if self.active_power in {POWER_SPEED, POWER_SLOW} and now >= self.power_end_time:
            self.active_power = None
            self.power_end_time = 0

        if self.powerup is None and self.active_power is None and random.random() < 0.015:
            self.spawn_powerup()

        if self.poison is None and random.random() < 0.01:
            self.spawn_poison()

    def draw_grid(self):
        if not self.settings["grid_overlay"]:
            return

        for x in range(0, WIDTH, CELL_SIZE):
            pygame.draw.line(self.screen, (35, 42, 48), (x, TOP_MARGIN_CELLS * CELL_SIZE), (x, HEIGHT))
        for y in range(TOP_MARGIN_CELLS * CELL_SIZE, HEIGHT, CELL_SIZE):
            pygame.draw.line(self.screen, (35, 42, 48), (0, y), (WIDTH, y))

    def cell_rect(self, cell):
        return pygame.Rect(cell[0] * CELL_SIZE, cell[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)

    def draw(self):
        self.screen.fill((18, 22, 28))

        pygame.draw.rect(self.screen, (28, 35, 42), (0, TOP_MARGIN_CELLS * CELL_SIZE, WIDTH, HEIGHT - TOP_MARGIN_CELLS * CELL_SIZE))
        pygame.draw.rect(self.screen, (210, 210, 220), (0, TOP_MARGIN_CELLS * CELL_SIZE, WIDTH, HEIGHT - TOP_MARGIN_CELLS * CELL_SIZE), 2)

        self.draw_grid()

        for obstacle in self.obstacles:
            pygame.draw.rect(self.screen, (100, 105, 115), self.cell_rect(obstacle))
            pygame.draw.rect(self.screen, (50, 55, 65), self.cell_rect(obstacle), 2)

        if self.food:
            color = (255, 210, 50) if self.food["value"] == 1 else (255, 150, 50) if self.food["value"] == 3 else (120, 210, 255)
            pygame.draw.ellipse(self.screen, color, self.cell_rect(self.food["pos"]))
            draw_text(self.screen, self.food["value"], self.food["pos"][0] * CELL_SIZE + 5, self.food["pos"][1] * CELL_SIZE + 1, self.font, (30, 30, 30))

        if self.poison:
            pygame.draw.ellipse(self.screen, (110, 0, 20), self.cell_rect(self.poison["pos"]))
            pygame.draw.ellipse(self.screen, (40, 0, 5), self.cell_rect(self.poison["pos"]), 2)

        if self.powerup:
            color = {
                POWER_SPEED: (255, 80, 80),
                POWER_SLOW: (90, 180, 255),
                POWER_SHIELD: (120, 230, 255),
            }[self.powerup["kind"]]
            rect = self.cell_rect(self.powerup["pos"])
            pygame.draw.rect(self.screen, color, rect, border_radius=5)
            label = {
                POWER_SPEED: "B",
                POWER_SLOW: "S",
                POWER_SHIELD: "D",
            }[self.powerup["kind"]]
            draw_text(self.screen, label, rect.x + 5, rect.y + 1, self.font, (20, 20, 25))

        snake_color = tuple(self.settings["snake_color"])
        for index, segment in enumerate(self.snake):
            rect = self.cell_rect(segment)
            color = (min(255, snake_color[0] + 35), min(255, snake_color[1] + 35), min(255, snake_color[2] + 35)) if index == 0 else snake_color
            pygame.draw.rect(self.screen, color, rect, border_radius=5)
            pygame.draw.rect(self.screen, (10, 15, 20), rect, 1, border_radius=5)

        if self.shield and self.snake:
            rect = self.cell_rect(self.snake[0]).inflate(10, 10)
            pygame.draw.ellipse(self.screen, (120, 220, 255), rect, 2)

        self.draw_hud()

        pygame.display.flip()

    def draw_hud(self):
        pygame.draw.rect(self.screen, (22, 28, 35), (0, 0, WIDTH, TOP_MARGIN_CELLS * CELL_SIZE))
        pygame.draw.line(self.screen, (180, 180, 190), (0, TOP_MARGIN_CELLS * CELL_SIZE - 1), (WIDTH, TOP_MARGIN_CELLS * CELL_SIZE - 1), 2)

        draw_text(self.screen, f"Player: {self.username}", 15, 10, self.font)
        draw_text(self.screen, f"Score: {self.score}", 180, 10, self.font)
        draw_text(self.screen, f"Level: {self.level}", 310, 10, self.font)
        draw_text(self.screen, f"Best: {self.personal_best}", 425, 10, self.font)

        power = "None"
        if self.active_power == POWER_SPEED:
            left = max(0, (self.power_end_time - pygame.time.get_ticks()) // 1000)
            power = f"Speed boost {left}s"
        elif self.active_power == POWER_SLOW:
            left = max(0, (self.power_end_time - pygame.time.get_ticks()) // 1000)
            power = f"Slow motion {left}s"
        elif self.shield:
            power = "Shield ready"

        draw_text(self.screen, f"Power: {power}", 560, 10, self.font, (240, 220, 80))
        draw_text(self.screen, "Arrows/WASD move | Esc quits run", 15, 35, self.font, (200, 200, 210))

    def run(self):
        while self.running:
            self.clock.tick(self.effective_speed())
            self.handle_input()
            self.move()
            self.update_timers()
            self.draw()

        return {
            "score": self.score,
            "level": self.level,
            "personal_best": max(self.personal_best, self.score),
        }
