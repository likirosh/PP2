import pygame
import random
import json
import os
from db import save_result, get_personal_best

pygame.init()

WIDTH, HEIGHT = 800, 600
CELL = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake TSIS4")
clock = pygame.time.Clock()

font       = pygame.font.SysFont("Verdana", 22)
small_font = pygame.font.SysFont("Verdana", 16)
big_font   = pygame.font.SysFont("Verdana", 45)

WHITE    = (255, 255, 255)
BLACK    = (0,   0,   0)
GRAY     = (210, 210, 210)
DARK_GRAY= (80,  80,  80)
RED      = (220, 0,   0)
DARK_RED = (120, 0,   0)
ORANGE   = (255, 140, 0)
PURPLE   = (160, 32,  240)
BLUE     = (0,   120, 255)
YELLOW   = (230, 210, 0)
CYAN     = (0,   200, 200)
BROWN    = (100, 60,  20)

SETTINGS_FILE = "settings.json"

def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        data = {"snake_color": [220, 0, 0], "grid": True}
        save_settings(data)
        return data
    with open(SETTINGS_FILE, "r") as f:
        return json.load(f)

def save_settings(data):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(data, f, indent=4)

settings = load_settings()


def draw_text_center(text, y, size="normal", color=WHITE):
    img = (big_font if size == "big" else font).render(text, True, color)
    screen.blit(img, img.get_rect(center=(WIDTH // 2, y)))


class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text

    def draw(self):
        pygame.draw.rect(screen, DARK_GRAY, self.rect, border_radius=8)
        pygame.draw.rect(screen, WHITE, self.rect, 2, border_radius=8)
        t = font.render(self.text, True, WHITE)
        screen.blit(t, t.get_rect(center=self.rect.center))

    def clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)


class Food:
    FOOD_TIME = 7000  

    def __init__(self):
        self.weight    = 1
        self.color     = RED
        self.pos       = (0, 0)
        self.spawn_time = 0

    def new_position(self, snake, obstacles):
        self.weight = random.choice([1, 2, 3])
        self.color  = {1: RED, 2: ORANGE, 3: PURPLE}[self.weight]
        while True:
            x = random.randrange(CELL, WIDTH  - CELL, CELL)
            y = random.randrange(CELL, HEIGHT - CELL, CELL)
            if (x, y) not in snake and (x, y) not in obstacles:
                self.pos = (x, y)
                break
        self.spawn_time = pygame.time.get_ticks()

    def time_left_ms(self):
        return max(0, self.FOOD_TIME - (pygame.time.get_ticks() - self.spawn_time))

    def expired(self):
        return self.time_left_ms() == 0

    def draw(self):
        cx = self.pos[0] + CELL // 2
        cy = self.pos[1] + CELL // 2
        r  = CELL // 2 + (self.weight - 1) * 3   
        pygame.draw.circle(screen, self.color, (cx, cy), r)

        frac   = self.time_left_ms() / self.FOOD_TIME
        end_a  = int(-90 + frac * 360)   
        if frac > 0:
            arc_r  = pygame.Rect(cx - r - 4, cy - r - 4, (r + 4) * 2, (r + 4) * 2)
            arc_col= YELLOW if frac > 0.4 else RED
            pygame.draw.arc(screen, arc_col, arc_r,
                            pygame.math.Vector2(0, 1).angle_to((0, 1)) * 0,
                            0, 3)
            import math
            step = 6
            for deg in range(-90, end_a, step):
                rad = math.radians(deg)
                px  = cx + int((r + 5) * math.cos(rad))
                py  = cy + int((r + 5) * math.sin(rad))
                pygame.draw.circle(screen, arc_col, (px, py), 2)

        lbl = small_font.render(f"+{self.weight}", True, WHITE)
        screen.blit(lbl, lbl.get_rect(center=(cx, cy)))


class Poison:
    def __init__(self):
        self.pos = (0, 0)

    def new_position(self, snake, obstacles):
        while True:
            x = random.randrange(CELL, WIDTH  - CELL, CELL)
            y = random.randrange(CELL, HEIGHT - CELL, CELL)
            if (x, y) not in snake and (x, y) not in obstacles:
                self.pos = (x, y)
                break

    def draw(self):
        cx = self.pos[0] + CELL // 2
        cy = self.pos[1] + CELL // 2
        pygame.draw.circle(screen, DARK_RED, (cx, cy), CELL // 2)
        pygame.draw.line(screen, WHITE, (cx-5, cy-5), (cx+5, cy+5), 2)
        pygame.draw.line(screen, WHITE, (cx+5, cy-5), (cx-5, cy+5), 2)


class PowerUp:
    def __init__(self):
        self.kind       = None
        self.rect       = pygame.Rect(0, 0, CELL, CELL)
        self.spawn_time = 0
        self.life_time  = 8000
        self.active     = False

    def spawn(self, snake, obstacles):
        self.kind       = random.choice(["speed", "slow", "shield"])
        self.active     = True
        self.spawn_time = pygame.time.get_ticks()
        while True:
            x = random.randrange(CELL, WIDTH  - CELL, CELL)
            y = random.randrange(CELL, HEIGHT - CELL, CELL)
            if (x, y) not in snake and (x, y) not in obstacles:
                self.rect.topleft = (x, y)
                break

    def expired(self):
        return self.active and pygame.time.get_ticks() - self.spawn_time >= self.life_time

    def draw(self):
        if not self.active:
            return
        col = {"speed": BLUE, "slow": YELLOW, "shield": CYAN}[self.kind]
        cx, cy = self.rect.centerx, self.rect.centery
        pts = [(cx, cy-10), (cx+10, cy), (cx, cy+10), (cx-10, cy)]
        pygame.draw.polygon(screen, col, pts)
        pygame.draw.polygon(screen, BLACK, pts, 1)


class Game:
    def __init__(self, username):
        self.username      = username
        self.personal_best = get_personal_best(username)
        self.reset()

    def reset(self):
        self.snake      = [(400, 300), (380, 300), (360, 300)]
        self.dx         = CELL
        self.dy         = 0
        self.score      = 0
        self.level      = 1
        self.food_count = 0
        self.base_speed = 8
        self.speed      = self.base_speed
        self.obstacles  = []

        self.food  = Food()
        self.food.new_position(self.snake, self.obstacles)

        self.poison = Poison()
        self.poison.new_position(self.snake, self.obstacles)

        self.power            = PowerUp()
        self.last_power_spawn = pygame.time.get_ticks()
        self.speed_boost_until= 0
        self.slow_until       = 0
        self.shield           = False
        self.game_over        = False
        self.saved            = False

    def generate_obstacles(self):
        self.obstacles = []
        count     = min(8 + self.level * 2, 35)
        forbidden = set(self.snake)
        hx, hy    = self.snake[0]
        for dx, dy in [(CELL,0),(-CELL,0),(0,CELL),(0,-CELL)]:
            forbidden.add((hx+dx, hy+dy))
        while len(self.obstacles) < count:
            x = random.randrange(CELL*2, WIDTH  - CELL*2, CELL)
            y = random.randrange(CELL*2, HEIGHT - CELL*2, CELL)
            if (x,y) not in forbidden and (x,y) not in self.obstacles:
                self.obstacles.append((x, y))

    def handle_key(self, key):
        if key == pygame.K_UP    and self.dy == 0:   self.dx=0;    self.dy=-CELL
        elif key == pygame.K_DOWN  and self.dy == 0: self.dx=0;    self.dy=CELL
        elif key == pygame.K_LEFT  and self.dx == 0: self.dx=-CELL; self.dy=0
        elif key == pygame.K_RIGHT and self.dx == 0: self.dx=CELL;  self.dy=0

    def update_power_effects(self):
        now        = pygame.time.get_ticks()
        self.speed = self.base_speed
        if now < self.speed_boost_until: self.speed = self.base_speed + 5
        if now < self.slow_until:        self.speed = max(4, self.base_speed - 4)

    def update(self):
        if self.game_over:
            if not self.saved:
                save_result(self.username, self.score, self.level)
                self.personal_best = max(self.personal_best, self.score)
                self.saved = True
            return

        now = pygame.time.get_ticks()

        if self.food.expired():
            self.food.new_position(self.snake, self.obstacles)

        if self.power.expired():
            self.power.active = False
        if not self.power.active and now - self.last_power_spawn >= 7000:
            self.power.spawn(self.snake, self.obstacles)
            self.last_power_spawn = now

        self.update_power_effects()

        hx, hy   = self.snake[0]
        nx, ny   = hx + self.dx, hy + self.dy

        nx = nx % WIDTH
        ny = ny % HEIGHT
        nx = (nx // CELL) * CELL
        ny = (ny // CELL) * CELL

        new_head = (nx, ny)

        if new_head in self.snake or new_head in self.obstacles:
            if self.shield:
                self.shield = False
                return
            else:
                self.game_over = True
                return

        self.snake.insert(0, new_head)

        ate_food   = new_head == self.food.pos
        ate_poison = new_head == self.poison.pos
        ate_power  = self.power.active and new_head == self.power.rect.topleft

        if ate_food:
            self.score      += self.food.weight
            self.food_count += 1
            self.food.new_position(self.snake, self.obstacles)
            if self.food_count == 3:
                self.level      += 1
                self.base_speed += 2
                self.food_count  = 0
                if self.level >= 3:
                    self.generate_obstacles()
                    self.food.new_position(self.snake, self.obstacles)
                    self.poison.new_position(self.snake, self.obstacles)
        elif ate_poison:
            for _ in range(2):
                if len(self.snake) > 1:
                    self.snake.pop()
            self.poison.new_position(self.snake, self.obstacles)
            if len(self.snake) <= 1:
                self.game_over = True
        else:
            self.snake.pop()   

        if ate_power:
            if   self.power.kind == "speed":  self.speed_boost_until = now + 5000
            elif self.power.kind == "slow":   self.slow_until        = now + 5000
            elif self.power.kind == "shield": self.shield            = True
            self.power.active = False

    def draw_grid(self):
        for x in range(0, WIDTH, CELL):
            pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, CELL):
            pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))

    def draw(self):
        screen.fill(BLACK)
        if settings["grid"]:
            self.draw_grid()

        for block in self.obstacles:
            pygame.draw.rect(screen, BROWN, (*block, CELL, CELL))

        self.food.draw()
        self.poison.draw()
        self.power.draw()

        snake_color = tuple(settings["snake_color"])
        outline_col = tuple(max(0, c - 60) for c in snake_color)
        for i, (x, y) in enumerate(self.snake):
            cx, cy = x + CELL//2, y + CELL//2
            r = CELL // 2
            if i == 0:
                pygame.draw.circle(screen, snake_color, (cx, cy), r + 1)
                pygame.draw.circle(screen, outline_col, (cx, cy), r + 1, 2)
            else:
                pygame.draw.circle(screen, snake_color, (cx, cy), r)
                pygame.draw.circle(screen, outline_col, (cx, cy), r, 1)

        secs_left = self.food.time_left_ms() // 1000 + 1
        texts = [
            f"Player: {self.username}",
            f"Score:  {self.score}",
            f"Level:  {self.level}",
            f"Best:   {self.personal_best}",
            f"Food:   +{self.food.weight}  ⏱{secs_left}s",
            f"Shield: {'YES' if self.shield else 'NO'}",
        ]
        y = 25
        for t in texts:
            img = small_font.render(t, True, WHITE)
            screen.blit(img, (25, y))
            y += 24