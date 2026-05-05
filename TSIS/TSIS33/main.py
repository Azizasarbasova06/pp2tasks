import pygame
from pathlib import Path
from ui import WIDTH, HEIGHT, BG, WHITE, YELLOW, BIG, FONT, SMALL, Button, draw_text, draw_title, draw_screen_background
from persistence import load_settings, save_settings, load_leaderboard
from racer import RacerGame

pygame.init()
try:
    pygame.mixer.init()
except Exception:
    pass

def play_ui_click():
    if not settings.get("sound", True) or not pygame.mixer.get_init():
        return
    try:
        path = Path("assets") / "click.wav"
        if path.exists():
            pygame.mixer.Sound(str(path)).play()
    except Exception:
        pass

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS3 Racer")
clock = pygame.time.Clock()

STATE_MENU = "menu"
STATE_NAME = "name"
STATE_GAME = "game"
STATE_GAME_OVER = "game_over"
STATE_LEADERBOARD = "leaderboard"
STATE_SETTINGS = "settings"

settings = load_settings()
state = STATE_MENU
player_name = ""
name_input = ""
game = None

def menu_screen():
    global state
    buttons = [
        Button((WIDTH//2 - 120, 220, 240, 58), "Play"),
        Button((WIDTH//2 - 120, 300, 240, 58), "Leaderboard"),
        Button((WIDTH//2 - 120, 380, 240, 58), "Settings"),
        Button((WIDTH//2 - 120, 460, 240, 58), "Quit"),
    ]
    while True:
        draw_screen_background(screen)
        draw_title(screen, "TSIS3 RACER")
        draw_text(screen, "Advanced Driving, Leaderboard & Power-Ups", WIDTH//2, 155, FONT, WHITE, center=True)
        for b in buttons:
            b.draw(screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if buttons[0].clicked(event):
                play_ui_click()
                return STATE_NAME
            if buttons[1].clicked(event):
                play_ui_click()
                return STATE_LEADERBOARD
            if buttons[2].clicked(event):
                play_ui_click()
                return STATE_SETTINGS
            if buttons[3].clicked(event):
                play_ui_click()
                return "quit"
        clock.tick(60)

def name_screen():
    global name_input

    # Каждый раз очищаем поле ввода.
    # "Player" теперь не пишется сразу, а используется только если имя пустое.
    name_input = ""

    start_btn = Button((WIDTH//2 - 120, 430, 240, 58), "Start")
    back_btn = Button((WIDTH//2 - 120, 510, 240, 58), "Back")
    active = True

    while True:
        draw_screen_background(screen)
        draw_title(screen, "ENTER USERNAME")
        draw_text(
            screen,
            "Click the box, type your name, then press Enter or Start",
            WIDTH//2,
            170,
            FONT,
            WHITE,
            center=True
        )

        box = pygame.Rect(WIDTH//2 - 210, 260, 420, 60)
        pygame.draw.rect(screen, (35, 38, 56), box, border_radius=10)
        pygame.draw.rect(screen, YELLOW if active else WHITE, box, 2, border_radius=10)

        if name_input:
            shown = name_input
            color = WHITE
        else:
            shown = "Type your name here..."
            color = (145, 145, 160)

        draw_text(screen, shown, box.centerx, box.y + 15, FONT, color, center=True)

        # мигающий курсор
        if active and pygame.time.get_ticks() % 1000 < 500:
            cursor_x = box.centerx + FONT.size(name_input if name_input else "")[0] // 2 + 6
            pygame.draw.line(screen, WHITE, (cursor_x, box.y + 14), (cursor_x, box.y + 45), 2)

        draw_text(
            screen,
            "If empty, the game will use name: Player",
            WIDTH//2,
            350,
            SMALL,
            WHITE,
            center=True
        )

        start_btn.draw(screen)
        back_btn.draw(screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit", None

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                active = box.collidepoint(event.pos)

            if event.type == pygame.KEYDOWN and active:
                if event.key == pygame.K_BACKSPACE:
                    name_input = name_input[:-1]
                elif event.key == pygame.K_RETURN:
                    play_ui_click()
                    return STATE_GAME, (name_input.strip() or "Player")
                elif event.key == pygame.K_ESCAPE:
                    return STATE_MENU, None
                else:
                    ch = event.unicode
                    if ch and ch.isprintable() and len(name_input) < 16:
                        name_input += ch

            if start_btn.clicked(event):
                play_ui_click()
                return STATE_GAME, (name_input.strip() or "Player")

            if back_btn.clicked(event):
                play_ui_click()
                return STATE_MENU, None

        clock.tick(60)

def settings_screen():
    global settings
    colors = ["blue", "red", "green", "yellow", "purple"]
    difficulties = ["Easy", "Normal", "Hard"]

    sound_btn = Button((WIDTH//2 - 160, 210, 320, 55), "")
    color_btn = Button((WIDTH//2 - 160, 290, 320, 55), "")
    diff_btn = Button((WIDTH//2 - 160, 370, 320, 55), "")
    back_btn = Button((WIDTH//2 - 160, 500, 320, 55), "Back")

    while True:
        sound_btn.text = f"Sound: {'ON' if settings.get('sound') else 'OFF'}"
        color_btn.text = f"Car Color: {settings.get('car_color', 'blue')}"
        diff_btn.text = f"Difficulty: {settings.get('difficulty', 'Normal')}"

        draw_screen_background(screen)
        draw_title(screen, "SETTINGS")
        draw_text(screen, "Settings are saved to settings.json", WIDTH//2, 155, SMALL, WHITE, center=True)
        for b in [sound_btn, color_btn, diff_btn, back_btn]:
            b.draw(screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_settings(settings)
                return "quit"
            if sound_btn.clicked(event):
                settings["sound"] = not settings.get("sound", True)
                play_ui_click()
                save_settings(settings)
            if color_btn.clicked(event):
                play_ui_click()
                i = colors.index(settings.get("car_color", "blue")) if settings.get("car_color", "blue") in colors else 0
                settings["car_color"] = colors[(i + 1) % len(colors)]
                save_settings(settings)
            if diff_btn.clicked(event):
                play_ui_click()
                i = difficulties.index(settings.get("difficulty", "Normal")) if settings.get("difficulty", "Normal") in difficulties else 1
                settings["difficulty"] = difficulties[(i + 1) % len(difficulties)]
                save_settings(settings)
            if back_btn.clicked(event):
                play_ui_click()
                save_settings(settings)
                return STATE_MENU
        clock.tick(60)

def leaderboard_screen():
    back_btn = Button((WIDTH//2 - 100, HEIGHT - 90, 200, 55), "Back")
    while True:
        draw_screen_background(screen)
        draw_title(screen, "TOP 10 LEADERBOARD")
        data = load_leaderboard()

        headers = ["#", "Name", "Score", "Distance", "Coins", "Mode"]
        xs = [120, 220, 390, 520, 650, 760]
        y = 190
        for x, h in zip(xs, headers):
            draw_text(screen, h, x, y, FONT, YELLOW, center=True)

        if not data:
            draw_text(screen, "No scores saved yet.", WIDTH//2, 330, FONT, WHITE, center=True)
        else:
            y = 245
            for i, row in enumerate(data[:10], 1):
                values = [
                    i,
                    row.get("name", "Player"),
                    row.get("score", 0),
                    f"{row.get('distance', 0)} m",
                    row.get("coins", 0),
                    row.get("mode", "Normal")
                ]
                for x, val in zip(xs, values):
                    draw_text(screen, val, x, y, SMALL, WHITE, center=True)
                y += 38

        back_btn.draw(screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if back_btn.clicked(event):
                play_ui_click()
                return STATE_MENU
        clock.tick(60)

def game_over_screen(game):
    game.save_result_once()
    retry_btn = Button((WIDTH//2 - 125, 430, 250, 58), "Retry")
    menu_btn = Button((WIDTH//2 - 125, 510, 250, 58), "Main Menu")

    while True:
        draw_screen_background(screen)
        title = "FINISH!" if game.finished else "GAME OVER"
        draw_title(screen, title)
        draw_text(screen, f"Player: {game.player_name}", WIDTH//2, 180, FONT, WHITE, center=True)
        draw_text(screen, f"Score: {int(game.score)}", WIDTH//2, 230, FONT, WHITE, center=True)
        draw_text(screen, f"Distance: {int(game.distance)} m", WIDTH//2, 270, FONT, WHITE, center=True)
        draw_text(screen, f"Coins: {game.coins}", WIDTH//2, 310, FONT, WHITE, center=True)
        draw_text(screen, "Result saved to leaderboard.json", WIDTH//2, 360, SMALL, YELLOW, center=True)
        retry_btn.draw(screen)
        menu_btn.draw(screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if retry_btn.clicked(event):
                play_ui_click()
                return STATE_GAME
            if menu_btn.clicked(event):
                play_ui_click()
                return STATE_MENU
        clock.tick(60)

def play_game(game):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.save_result_once()
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game.player.move_left()
                elif event.key == pygame.K_RIGHT:
                    game.player.move_right()
                elif event.key == pygame.K_ESCAPE:
                    game.save_result_once()
                    return STATE_MENU

        game.update()
        game.draw(screen)
        pygame.display.flip()

        if game.game_over or game.finished:
            return STATE_GAME_OVER

        clock.tick(60)

running = True
while running:
    if state == STATE_MENU:
        state = menu_screen()
        if state == "quit":
            running = False

    elif state == STATE_NAME:
        state, maybe_name = name_screen()
        if state == "quit":
            running = False
        elif maybe_name:
            player_name = maybe_name
            game = RacerGame(player_name, settings)

    elif state == STATE_GAME:
        if game is None or game.game_over or game.finished:
            game = RacerGame(player_name or "Player", settings)
        state = play_game(game)
        if state == "quit":
            running = False

    elif state == STATE_GAME_OVER:
        state = game_over_screen(game)
        if state == "quit":
            running = False
        elif state == STATE_GAME:
            game = RacerGame(player_name or "Player", settings)

    elif state == STATE_LEADERBOARD:
        state = leaderboard_screen()
        if state == "quit":
            running = False

    elif state == STATE_SETTINGS:
        state = settings_screen()
        if state == "quit":
            running = False

pygame.quit()
