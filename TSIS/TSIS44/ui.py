import pygame

from settings_manager import COLOR_OPTIONS


WIDTH = 900
HEIGHT = 700


class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text

    def collidepoint(self, pos):
        return self.rect.collidepoint(pos)

    def draw(self, screen, font, selected=False):
        fill = (55, 115, 80) if selected else (45, 55, 70)
        border = (240, 220, 80) if selected else (150, 160, 170)

        pygame.draw.rect(screen, fill, self.rect, border_radius=10)
        pygame.draw.rect(screen, border, self.rect, 2, border_radius=10)

        rendered = font.render(self.text, True, (255, 255, 255))
        screen.blit(rendered, rendered.get_rect(center=self.rect.center))


def draw_text(screen, text, x, y, font, color=(255, 255, 255)):
    screen.blit(font.render(str(text), True, color), (x, y))


def draw_center_text(screen, text, y, font, color=(255, 255, 255)):
    rendered = font.render(str(text), True, color)
    screen.blit(rendered, rendered.get_rect(center=(WIDTH // 2, y)))


def username_screen(screen, clock):
    title_font = pygame.font.SysFont("arial", 34, bold=True)
    font = pygame.font.SysFont("arial", 24)

    username = ""

    while True:
        screen.fill((22, 28, 35))
        draw_center_text(screen, "Enter username", 180, title_font, (240, 220, 80))
        draw_center_text(screen, "Press Enter to continue or Escape to cancel", 230, font, (220, 220, 220))

        box = pygame.Rect(WIDTH // 2 - 180, 290, 360, 54)
        pygame.draw.rect(screen, (245, 245, 245), box, border_radius=8)
        pygame.draw.rect(screen, (240, 220, 80), box, 2, border_radius=8)

        rendered = font.render(username + "|", True, (30, 30, 30))
        screen.blit(rendered, (box.x + 14, box.y + 14))

        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return None

                if event.key == pygame.K_RETURN:
                    return username.strip() or "Player"

                if event.key == pygame.K_BACKSPACE:
                    username = username[:-1]

                elif event.unicode and event.unicode.isprintable() and len(username) < 16:
                    username += event.unicode


def main_menu(screen, clock):
    title_font = pygame.font.SysFont("arial", 40, bold=True)
    font = pygame.font.SysFont("arial", 24)

    buttons = [
        Button(WIDTH // 2 - 110, 230, 220, 52, "Play"),
        Button(WIDTH // 2 - 110, 300, 220, 52, "Leaderboard"),
        Button(WIDTH // 2 - 110, 370, 220, 52, "Settings"),
        Button(WIDTH // 2 - 110, 440, 220, 52, "Quit"),
    ]

    while True:
        screen.fill((22, 28, 35))
        draw_center_text(screen, "TSIS4 SNAKE", 110, title_font, (240, 220, 80))
        draw_center_text(screen, "Database Integration & Advanced Gameplay", 160, font, (230, 230, 230))

        for button in buttons:
            button.draw(screen, font)

        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button in buttons:
                    if button.collidepoint(event.pos):
                        return button.text.lower()


def game_over_screen(screen, clock, result):
    title_font = pygame.font.SysFont("arial", 38, bold=True)
    font = pygame.font.SysFont("arial", 24)

    retry = Button(WIDTH // 2 - 190, 510, 160, 52, "Retry")
    menu = Button(WIDTH // 2 + 30, 510, 160, 52, "Main Menu")

    while True:
        screen.fill((35, 25, 30))

        draw_center_text(screen, "GAME OVER", 120, title_font, (240, 90, 90))
        draw_center_text(screen, f"Score: {result['score']}", 210, font)
        draw_center_text(screen, f"Level reached: {result['level']}", 250, font)
        draw_center_text(screen, f"Personal best: {result['personal_best']}", 290, font)

        retry.draw(screen, font)
        menu.draw(screen, font)

        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "menu"

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if retry.collidepoint(event.pos):
                    return "retry"
                if menu.collidepoint(event.pos):
                    return "menu"


def leaderboard_screen(screen, clock, rows):
    title_font = pygame.font.SysFont("arial", 34, bold=True)
    font = pygame.font.SysFont("arial", 21)
    small_font = pygame.font.SysFont("arial", 18)

    back = Button(WIDTH // 2 - 80, 610, 160, 48, "Back")

    while True:
        screen.fill((22, 28, 35))
        draw_center_text(screen, "TOP 10 LEADERBOARD", 70, title_font, (240, 220, 80))

        headers = ["#", "Username", "Score", "Level", "Date"]
        xs = [90, 160, 350, 480, 580]

        for x, header in zip(xs, headers):
            draw_text(screen, header, x, 125, font, (240, 220, 80))

        if not rows:
            draw_center_text(screen, "No database scores yet.", 260, font)
        else:
            y = 165
            for index, row in enumerate(rows, start=1):
                values = [
                    index,
                    row["username"],
                    row["score"],
                    row["level_reached"],
                    row["played_at"],
                ]
                for x, value in zip(xs, values):
                    draw_text(screen, value, x, y, small_font)
                y += 38

        back.draw(screen, font)
        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if back.collidepoint(event.pos):
                    return


def settings_screen(screen, clock, settings):
    title_font = pygame.font.SysFont("arial", 34, bold=True)
    font = pygame.font.SysFont("arial", 22)

    local = settings.copy()
    local["snake_color"] = list(local["snake_color"])

    grid_button = Button(WIDTH // 2 - 120, 160, 240, 48, "")
    sound_button = Button(WIDTH // 2 - 120, 230, 240, 48, "")

    color_buttons = []
    start_x = 150
    for index, name in enumerate(COLOR_OPTIONS.keys()):
        color_buttons.append(Button(start_x + index * 125, 370, 105, 44, name))

    save_back = Button(WIDTH // 2 - 120, 570, 240, 52, "Save & Back")

    while True:
        screen.fill((22, 28, 35))
        draw_center_text(screen, "SETTINGS", 70, title_font, (240, 220, 80))

        grid_button.text = "Grid: ON" if local["grid_overlay"] else "Grid: OFF"
        sound_button.text = "Sound: ON" if local["sound"] else "Sound: OFF"

        grid_button.draw(screen, font, selected=local["grid_overlay"])
        sound_button.draw(screen, font, selected=local["sound"])

        draw_center_text(screen, "Snake Color", 330, font)
        for button in color_buttons:
            color = COLOR_OPTIONS[button.text]
            selected = color == local["snake_color"]
            button.draw(screen, font, selected=selected)
            pygame.draw.rect(screen, color, (button.rect.x + 8, button.rect.y + 10, 18, 24))

        save_back.draw(screen, font)

        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return local

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if grid_button.collidepoint(event.pos):
                    local["grid_overlay"] = not local["grid_overlay"]

                elif sound_button.collidepoint(event.pos):
                    local["sound"] = not local["sound"]

                else:
                    for button in color_buttons:
                        if button.collidepoint(event.pos):
                            local["snake_color"] = COLOR_OPTIONS[button.text]

                if save_back.collidepoint(event.pos):
                    return local
