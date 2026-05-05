import pygame

from db import init_db, get_personal_best, get_top_10, save_game_result
from game import SnakeGame
from settings_manager import load_settings, save_settings
from ui import (
    WIDTH,
    HEIGHT,
    main_menu,
    username_screen,
    game_over_screen,
    leaderboard_screen,
    settings_screen,
)


def play_game(screen, clock, settings):
    username = username_screen(screen, clock)
    if username is None:
        return settings

    personal_best = get_personal_best(username)

    while True:
        game = SnakeGame(screen, clock, settings, username, personal_best)
        result = game.run()

        save_game_result(username, result["score"], result["level"])
        personal_best = max(personal_best, result["score"])
        result["personal_best"] = personal_best

        action = game_over_screen(screen, clock, result)
        if action != "retry":
            break

    return settings


def main():
    pygame.init()
    pygame.font.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("TSIS4 Snake")
    clock = pygame.time.Clock()

    init_db()
    settings = load_settings()

    running = True
    while running:
        action = main_menu(screen, clock)

        if action == "play":
            settings = play_game(screen, clock, settings)

        elif action == "leaderboard":
            rows = get_top_10()
            leaderboard_screen(screen, clock, rows)

        elif action == "settings":
            settings = settings_screen(screen, clock, settings)
            save_settings(settings)

        elif action == "quit":
            running = False

    pygame.quit()


if __name__ == "__main__":
    main()
