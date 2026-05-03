import pygame
import sys
import random
import os

pygame.init()

# ---------------- SETTINGS ----------------
WIDTH, HEIGHT = 500, 600
FPS = 60

PLAYER_SPEED = 6
BASE_ENEMY_SPEED = 5
BASE_COIN_SPEED = 5

COINS_TO_LEVEL_UP = 10
MAX_ENEMIES = 4

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (200,0,0)
GOLD = (255,215,0)
SILVER = (180,180,180)
BRONZE = (160,90,40)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer FINAL")
clock = pygame.time.Clock()

font_small = pygame.font.SysFont("Verdana", 18)
font_big = pygame.font.SysFont("Verdana", 48)

# ---------------- GAME STATE ----------------
score = 0
coins = 0
level = 0
enemy_speed = BASE_ENEMY_SPEED
coin_speed = BASE_COIN_SPEED
game_state = "menu"

# ---------------- LOAD IMAGES ----------------
BASE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(BASE, "images")

def load(name, size):
    try:
        img = pygame.image.load(os.path.join(IMG, name)).convert_alpha()
        return pygame.transform.scale(img, size)
    except:
        surf = pygame.Surface(size)
        surf.fill((150,150,150))
        return surf

bg = load("AnimatedStreet.png", (WIDTH, HEIGHT))
player_img = load("Player.png", (70,90))
enemy_img = load("Enemy.png", (70,90))

# ---------------- CLASSES ----------------
class Player(pygame.sprite.Sprite):
    """Player car."""
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect(center=(WIDTH//2,520))

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= PLAYER_SPEED

        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += PLAYER_SPEED


class Enemy(pygame.sprite.Sprite):
    """Enemy car."""
    def __init__(self):
        super().__init__()
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.reset()

    def reset(self):
        self.rect.centerx = random.randint(50, WIDTH-50)
        self.rect.y = random.randint(-150,-60)

    def move(self):
        global score
        self.rect.y += enemy_speed

        if self.rect.top > HEIGHT:
            score += 1
            self.reset()


class Coin:
    """Coin with random weight."""
    def __init__(self):
        self.rect = pygame.Rect(-100,-100,40,40)
        self.active = False

    def spawn(self):
        # Probability changes with level
        types = (
            [("bronze",1,BRONZE)] * max(1,5-level) +
            [("silver",2,SILVER)] * (3+level) +
            [("gold",3,GOLD)] * (1+level)
        )

        self.name, self.value, self.color = random.choice(types)

        self.rect.centerx = random.randint(40, WIDTH-40)
        self.rect.y = -30
        self.active = True

    def move(self):
        if self.active:
            self.rect.y += coin_speed
            if self.rect.top > HEIGHT:
                self.active = False

    def draw(self):
        if self.active:
            pygame.draw.circle(screen, self.color, self.rect.center, 20)
            pygame.draw.circle(screen, BLACK, self.rect.center, 20, 2)

            txt = font_small.render(str(self.value), True, BLACK)
            screen.blit(txt, txt.get_rect(center=self.rect.center))


# ---------------- FUNCTIONS ----------------
def update_level():
    """Update level and difficulty."""
    global level, enemy_speed, coin_speed

    new_level = coins // COINS_TO_LEVEL_UP

    if new_level > level:
        level = new_level

        enemy_speed = BASE_ENEMY_SPEED + level
        coin_speed = BASE_COIN_SPEED + level * 0.5

        # Add new enemy
        if len(enemies) < MAX_ENEMIES:
            enemies.add(Enemy())


def draw_hud():
    screen.blit(font_small.render(f"Score: {score}", True, BLACK), (80,30))
    screen.blit(font_small.render(f"Coins: {coins}", True, BLACK), (80,55))
    screen.blit(font_small.render(f"Level: {level}", True, BLACK), (80,80))
    screen.blit(font_small.render(f"Speed: {enemy_speed}", True, BLACK), (80,105))


def draw_menu():
    screen.fill(BLACK)

    screen.blit(font_big.render("RACER", True, WHITE), (140,200))
    screen.blit(font_small.render("ENTER - Start", True, WHITE), (170,300))
    screen.blit(font_small.render("ESC - Exit", True, WHITE), (175,340))

    pygame.display.update()


def game_over():
    global game_state

    screen.fill(RED)
    screen.blit(font_big.render("GAME OVER", True, BLACK), (90,250))
    screen.blit(font_small.render(f"Coins: {coins}", True, BLACK), (200,320))

    pygame.display.update()
    pygame.time.delay(2000)

    game_state = "menu"


# ---------------- OBJECTS ----------------
player = Player()
enemies = pygame.sprite.Group()
enemies.add(Enemy())
coin = Coin()

# Timer
SPAWN = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN, 2000)

# ---------------- MAIN LOOP ----------------
while True:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if game_state == "menu":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    score = 0
                    coins = 0
                    level = 0
                    enemy_speed = BASE_ENEMY_SPEED
                    coin_speed = BASE_COIN_SPEED

                    enemies.empty()
                    enemies.add(Enemy())

                    game_state = "playing"

                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        elif game_state == "playing":

            if event.type == SPAWN:
                if not coin.active:
                    coin.spawn()

                    # Dynamic spawn rate
                    delay = max(600, 2000 - level*150)
                    pygame.time.set_timer(SPAWN, delay)

    if game_state == "menu":
        draw_menu()
        continue

    # --- GAME LOGIC ---
    player.move()

    for enemy in enemies:
        enemy.move()

    coin.move()

    # Collision enemy
    if pygame.sprite.spritecollideany(player, enemies):
        game_over()
        continue

    # Collision coin
    if coin.active and player.rect.colliderect(coin.rect):
        coins += coin.value
        coin.active = False
        update_level()

    # --- DRAW ---
    screen.blit(bg, (0,0))
    screen.blit(player.image, player.rect)

    for enemy in enemies:
        screen.blit(enemy.image, enemy.rect)

    coin.draw()
    draw_hud()

    pygame.display.update()
    clock.tick(FPS)