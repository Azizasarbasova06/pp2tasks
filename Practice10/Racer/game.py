import pygame
import sys
import random
import os

pygame.init()

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 600
FPS = 60
SPEED = 5

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GRAY = (180, 180, 180)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Racer")
clock = pygame.time.Clock()

font_small = pygame.font.SysFont("Verdana", 20)
font_big = pygame.font.SysFont("Verdana", 48)

score = 0
coins_collected = 0

game_state = "menu"   # menu / playing / paused

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(BASE_DIR, "images")


def load_image(filename, size=None):
    path = os.path.join(IMAGES_DIR, filename)
    try:
        img = pygame.image.load(path).convert_alpha()
        if size:
            img = pygame.transform.scale(img, size)
        return img
    except:
        surf = pygame.Surface(size or (50, 50))
        surf.fill(GRAY)
        return surf


background = load_image("AnimatedStreet.png", (SCREEN_WIDTH, SCREEN_HEIGHT))
player_img = load_image("Player.png", (70, 90))
enemy_img = load_image("Enemy.png", (70, 90))
coin_img = load_image("Coin.png", (50, 50))


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect(center=(200, 520))

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= 6
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += 6


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.reset()

    def reset(self):
        self.rect.centerx = random.randint(50, SCREEN_WIDTH - 50)
        self.rect.y = random.randint(-150, -60)

    def move(self):
        global score
        self.rect.y += SPEED
        if self.rect.top > SCREEN_HEIGHT:
            score += 1
            self.reset()


class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = coin_img
        self.rect = self.image.get_rect()
        self.active = False
        self.hide()

    def spawn(self):
        self.rect.centerx = random.randint(40, SCREEN_WIDTH - 40)
        self.rect.y = -30
        self.active = True

    def hide(self):
        self.rect.x = -100
        self.active = False

    def move(self):
        if self.active:
            self.rect.y += SPEED
            if self.rect.top > SCREEN_HEIGHT:
                self.hide()


player = Player()
enemy = Enemy()
coin = Coin()

enemies = pygame.sprite.Group(enemy)

# Таймеры
INC_SPEED = pygame.USEREVENT + 1
SPAWN_COIN = pygame.USEREVENT + 2
pygame.time.set_timer(INC_SPEED, 1000)
pygame.time.set_timer(SPAWN_COIN, 2500)


def draw_menu():
    screen.fill(BLACK)
    title = font_big.render("RACER", True, WHITE)
    start = font_small.render("ENTER - Start", True, WHITE)
    exit_t = font_small.render("ESC - Exit", True, WHITE)

    screen.blit(title, (120, 200))
    screen.blit(start, (130, 300))
    screen.blit(exit_t, (130, 340))
    pygame.display.update()


def draw_pause():
    text = font_big.render("PAUSED", True, RED)
    screen.blit(text, (100, 250))


def game_over():
    global game_state
    screen.fill(RED)
    text = font_big.render("Game Over", True, BLACK)
    screen.blit(text, (80, 250))
    pygame.display.update()
    pygame.time.delay(2000)
    game_state = "menu"


# главный цикл
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:

            if game_state == "menu":
                if event.key == pygame.K_RETURN:
                    game_state = "playing"
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            elif game_state == "playing":
                if event.key == pygame.K_ESCAPE:
                    game_state = "paused"

            elif game_state == "paused":
                if event.key == pygame.K_ESCAPE:
                    game_state = "playing"

        if game_state == "playing":
            if event.type == INC_SPEED:
                SPEED += 0.2
            if event.type == SPAWN_COIN:
                if not coin.active:
                    coin.spawn()

    if game_state == "menu":
        draw_menu()
        continue

    if game_state == "paused":
        draw_pause()
        pygame.display.update()
        continue

    # ИГРА
    player.move()
    enemy.move()
    coin.move()

    if pygame.sprite.spritecollideany(player, enemies):
        game_over()

    if coin.active and player.rect.colliderect(coin.rect):
        coins_collected += 1
        coin.hide()

    screen.blit(background, (0, 0))
    screen.blit(player.image, player.rect)
    screen.blit(enemy.image, enemy.rect)

    if coin.active:
        screen.blit(coin.image, coin.rect)

    score_text = font_small.render(f"Score: {int(score)}", True, BLACK)
    coins_text = font_small.render(f"Coins: {coins_collected}", True, BLACK)

    screen.blit(score_text, (10, 10))
    screen.blit(coins_text, (250, 10))

    pygame.display.update()
    clock.tick(FPS)