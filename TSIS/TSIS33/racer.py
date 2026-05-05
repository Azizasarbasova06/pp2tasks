import random
import time
import pygame
from pathlib import Path
from ui import WIDTH, HEIGHT, FONT, SMALL, BIG, WHITE, YELLOW, GREEN, RED, PANEL, draw_text
from persistence import save_score

ROAD_X = 230
ROAD_W = 540
LANES = [ROAD_X + 105, ROAD_X + 270, ROAD_X + 435]
PLAYER_Y = HEIGHT - 110
FINISH_DISTANCE = 5000

CAR_COLORS = {
    "blue": (38, 128, 235),
    "red": (220, 65, 65),
    "green": (48, 170, 90),
    "yellow": (235, 190, 45),
    "purple": (155, 95, 220)
}

DIFFICULTY = {
    "Easy":   {"speed": 5.0, "traffic": 0.018, "obstacle": 0.012, "power": 0.010},
    "Normal": {"speed": 6.2, "traffic": 0.026, "obstacle": 0.016, "power": 0.009},
    "Hard":   {"speed": 7.4, "traffic": 0.036, "obstacle": 0.022, "power": 0.007},
}

def load_sound(filename):
    try:
        path = Path("assets") / filename
        if path.exists() and pygame.mixer.get_init():
            return pygame.mixer.Sound(str(path))
    except Exception:
        return None
    return None

def safe_lane(player_lane, allow_same=False):
    choices = list(range(len(LANES)))
    if not allow_same and player_lane in choices and len(choices) > 1:
        choices.remove(player_lane)
    return random.choice(choices)

class Player:
    def __init__(self, color_name):
        self.lane = 1
        self.x = LANES[self.lane]
        self.y = PLAYER_Y
        self.color = CAR_COLORS.get(color_name, CAR_COLORS["blue"])
        self.shield = False

    @property
    def rect(self):
        return pygame.Rect(self.x - 27, self.y - 45, 54, 90)

    def move_left(self):
        if self.lane > 0:
            self.lane -= 1
            self.x = LANES[self.lane]

    def move_right(self):
        if self.lane < len(LANES) - 1:
            self.lane += 1
            self.x = LANES[self.lane]

    def draw(self, screen):
        r = self.rect
        pygame.draw.rect(screen, self.color, r, border_radius=8)
        pygame.draw.rect(screen, (15, 25, 45), r, 3, border_radius=8)
        pygame.draw.rect(screen, (180, 225, 255), (r.x + 10, r.y + 10, r.w - 20, 18), border_radius=5)
        pygame.draw.rect(screen, (20, 20, 25), (r.x + 8, r.y + 58, 12, 20))
        pygame.draw.rect(screen, (20, 20, 25), (r.right - 20, r.y + 58, 12, 20))
        if self.shield:
            pygame.draw.ellipse(screen, (100, 210, 255), r.inflate(18, 20), 3)

class FallingObject:
    def __init__(self, lane, y, kind, value=0):
        self.lane = lane
        self.x = LANES[lane]
        self.y = y
        self.kind = kind
        self.value = value
        self.created = time.time()

    @property
    def rect(self):
        if self.kind in ("traffic", "barrier"):
            return pygame.Rect(self.x - 30, self.y - 45, 60, 90)
        if self.kind in ("oil", "pothole", "speed_bump", "nitro_strip"):
            return pygame.Rect(self.x - 40, self.y - 22, 80, 44)
        return pygame.Rect(self.x - 24, self.y - 24, 48, 48)

    def draw(self, screen):
        r = self.rect
        if self.kind == "traffic":
            pygame.draw.rect(screen, (230, 185, 30), r, border_radius=8)
            pygame.draw.rect(screen, (30, 30, 35), r, 3, border_radius=8)
            pygame.draw.rect(screen, (210, 235, 255), (r.x + 10, r.y + 8, r.w - 20, 18), border_radius=5)
        elif self.kind == "barrier":
            pygame.draw.rect(screen, (230, 80, 50), r, border_radius=7)
            for i in range(0, r.w, 18):
                pygame.draw.line(screen, WHITE, (r.x + i, r.y + 10), (r.x + i + 15, r.y + 40), 4)
        elif self.kind == "oil":
            pygame.draw.ellipse(screen, (25, 25, 30), r)
            pygame.draw.ellipse(screen, (70, 70, 90), r, 2)
        elif self.kind == "pothole":
            pygame.draw.ellipse(screen, (55, 40, 30), r)
            pygame.draw.ellipse(screen, (20, 15, 15), r.inflate(-15, -12))
        elif self.kind == "speed_bump":
            pygame.draw.rect(screen, (190, 120, 40), r, border_radius=12)
            pygame.draw.line(screen, YELLOW, (r.x + 5, r.centery), (r.right - 5, r.centery), 5)
        elif self.kind == "nitro_strip":
            pygame.draw.rect(screen, (60, 190, 255), r, border_radius=12)
            draw_text(screen, "N2O", r.centerx, r.centery - 12, SMALL, WHITE, center=True)
        elif self.kind == "coin":
            pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y)), 20)
            pygame.draw.circle(screen, (210, 155, 20), (int(self.x), int(self.y)), 20, 3)
            draw_text(screen, self.value, self.x, self.y - 12, SMALL, (30, 30, 30), center=True)
        elif self.kind in ("Nitro", "Shield", "Repair"):
            colors = {"Nitro": (60, 190, 255), "Shield": (100, 220, 160), "Repair": (240, 90, 90)}
            pygame.draw.circle(screen, colors[self.kind], (int(self.x), int(self.y)), 24)
            pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), 24, 2)
            draw_text(screen, self.kind[0], self.x, self.y - 14, FONT, WHITE, center=True)

class RacerGame:
    def __init__(self, player_name, settings):
        self.player_name = player_name or "Player"
        self.settings = settings
        self.mode = settings.get("difficulty", "Normal")
        d = DIFFICULTY.get(self.mode, DIFFICULTY["Normal"])
        self.base_speed = d["speed"]
        self.speed = self.base_speed
        self.traffic_rate = d["traffic"]
        self.obstacle_rate = d["obstacle"]
        self.power_rate = d["power"]

        self.sound_enabled = bool(settings.get("sound", True))
        self.sounds = {
            "coin": load_sound("coin.wav"),
            "power": load_sound("power.wav"),
            "crash": load_sound("crash.wav"),
            "click": load_sound("click.wav"),
        }

        self.player = Player(settings.get("car_color", "blue"))
        self.objects = []
        self.score = 0
        self.coins = 0
        self.distance = 0
        self.finished = False
        self.game_over = False
        self.saved = False
        self.active_power = None
        self.power_end = 0
        self.nitro_multiplier = 1.0
        self.line_offset = 0
        self.spawn_cooldown = 0

    def current_difficulty_boost(self):
        return 1.0 + min(self.distance / 3000, 1.5)

    def spawn_object(self):
        boost = self.current_difficulty_boost()
        player_lane = self.player.lane

        if random.random() < self.traffic_rate * boost:
            lane = safe_lane(player_lane, allow_same=False)
            self.objects.append(FallingObject(lane, -70, "traffic"))

        if random.random() < self.obstacle_rate * boost:
            lane = safe_lane(player_lane, allow_same=False)
            kind = random.choice(["barrier", "oil", "pothole", "speed_bump"])
            self.objects.append(FallingObject(lane, -80, kind))

        if random.random() < 0.020:
            lane = random.randrange(3)
            value = random.choices([1, 2, 3, 5], weights=[45, 30, 18, 7])[0]
            self.objects.append(FallingObject(lane, -50, "coin", value))

        if random.random() < self.power_rate and self.active_power is None:
            lane = random.randrange(3)
            kind = random.choice(["Nitro", "Shield", "Repair"])
            self.objects.append(FallingObject(lane, -60, kind))

        # Dynamic road event: nitro strip sometimes appears as a road feature.
        if random.random() < 0.005:
            lane = random.randrange(3)
            self.objects.append(FallingObject(lane, -40, "nitro_strip"))

    def play_sound(self, name):
        if not self.sound_enabled:
            return
        sound = self.sounds.get(name)
        if sound:
            try:
                sound.play()
            except Exception:
                pass

    def apply_power(self, kind):
        self.active_power = kind
        now = time.time()
        if kind == "Nitro":
            self.power_end = now + 4
            self.nitro_multiplier = 1.55
        elif kind == "Shield":
            self.player.shield = True
            self.power_end = 0
        elif kind == "Repair":
            # Instant repair: clears the nearest dangerous object.
            dangerous = [o for o in self.objects if o.kind in ("traffic", "barrier", "oil", "pothole", "speed_bump")]
            if dangerous:
                nearest = max(dangerous, key=lambda o: o.y)
                self.objects.remove(nearest)
            self.score += 50
            self.active_power = None

    def clear_power_if_needed(self):
        if self.active_power == "Nitro" and time.time() >= self.power_end:
            self.active_power = None
            self.nitro_multiplier = 1.0
        if self.active_power == "Shield" and not self.player.shield:
            self.active_power = None

    def handle_collision(self, obj):
        if obj.kind == "coin":
            self.coins += obj.value
            self.score += obj.value * 10
            self.play_sound("coin")
            self.objects.remove(obj)
            return

        if obj.kind in ("Nitro", "Shield", "Repair"):
            if self.active_power is None or obj.kind == "Repair":
                self.apply_power(obj.kind)
                self.play_sound("power")
            self.objects.remove(obj)
            return

        if obj.kind == "nitro_strip":
            self.active_power = "Nitro"
            self.power_end = time.time() + 3
            self.nitro_multiplier = 1.4
            self.play_sound("power")
            self.objects.remove(obj)
            return

        if obj.kind in ("oil", "pothole", "speed_bump"):
            self.speed = max(3.2, self.speed - 1.5)
            self.score = max(0, self.score - 10)
            self.objects.remove(obj)
            return

        if obj.kind in ("traffic", "barrier"):
            if self.player.shield:
                self.player.shield = False
                self.objects.remove(obj)
            else:
                self.play_sound("crash")
                self.game_over = True

    def update(self):
        if self.game_over or self.finished:
            return

        self.clear_power_if_needed()
        self.speed = min(self.base_speed + self.distance / 900, 12) * self.nitro_multiplier
        self.distance += self.speed * 0.32
        self.score += int(self.speed * 0.04)

        if self.distance >= FINISH_DISTANCE:
            self.finished = True
            self.score += 500

        self.line_offset = (self.line_offset + self.speed) % 75
        self.spawn_object()

        for obj in list(self.objects):
            obj.y += self.speed
            if obj.kind in ("Nitro", "Shield", "Repair") and time.time() - obj.created > 7:
                self.objects.remove(obj)
                continue
            if obj.y > HEIGHT + 100:
                self.objects.remove(obj)
                continue
            if obj.rect.colliderect(self.player.rect):
                self.handle_collision(obj)

    def save_result_once(self):
        if self.saved:
            return
        entry = {
            "name": self.player_name,
            "score": int(self.score),
            "distance": int(self.distance),
            "coins": int(self.coins),
            "mode": self.mode
        }
        save_score(entry)
        self.saved = True

    def draw_road(self, screen):
        screen.fill(GREEN)
        road = pygame.Rect(ROAD_X, 0, ROAD_W, HEIGHT)
        pygame.draw.rect(screen, (43, 43, 50), road)
        pygame.draw.line(screen, WHITE, (ROAD_X, 0), (ROAD_X, HEIGHT), 6)
        pygame.draw.line(screen, WHITE, (ROAD_X + ROAD_W, 0), (ROAD_X + ROAD_W, HEIGHT), 6)

        for x in [ROAD_X + 180, ROAD_X + 360]:
            y = -70 + self.line_offset
            while y < HEIGHT:
                pygame.draw.rect(screen, WHITE, (x - 4, y, 8, 42))
                y += 75

        finish_y = int(90 - self.distance)
        if -30 < finish_y < HEIGHT:
            pygame.draw.rect(screen, WHITE, (ROAD_X + 120, finish_y, ROAD_W - 240, 18), border_radius=6)

    def draw_hud(self, screen):
        panel = pygame.Rect(25, 25, 190, 230)
        pygame.draw.rect(screen, PANEL, panel, border_radius=10)
        pygame.draw.rect(screen, (170, 170, 195), panel, 2, border_radius=10)

        left = max(0, FINISH_DISTANCE - self.distance)
        lines = [
            f"Player: {self.player_name}",
            f"Score: {int(self.score)}",
            f"Coins: {self.coins}",
            f"Distance: {int(self.distance)} m",
            f"Left: {int(left)} m",
            f"Speed: {self.speed:.1f}",
        ]
        if self.active_power == "Nitro":
            remaining = max(0, self.power_end - time.time())
            lines.append(f"Power: Nitro {remaining:.1f}s")
        elif self.active_power == "Shield":
            lines.append("Power: Shield")
        else:
            lines.append("Power: None")

        y = 35
        for line in lines:
            color = YELLOW if line.startswith("Power") else WHITE
            draw_text(screen, line, 36, y, SMALL, color)
            y += 30

    def draw(self, screen):
        self.draw_road(screen)
        for obj in self.objects:
            obj.draw(screen)
        self.player.draw(screen)
        self.draw_hud(screen)
