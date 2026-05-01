
import pygame
import random
import sys

WIDTH, HEIGHT = 400, 600
ROAD_LEFT  = 30    
ROAD_RIGHT = 370


DIFF = {
    "easy":   (3, 2, 5, 4,   1500, 6000),
    "normal": (5, 3, 4, 5,   1000, 4000),
    "hard":   (6, 4, 3, 6.5,  700, 2500),
}

CAR_TINTS = {
    "blue":  None,       
    "red":   (220, 60, 60),
    "green": (60, 200, 80),
}

POWERUP_TIMEOUT = 8000  
NITRO_DURATION  = 4000
SHIELD_DURATION = 999999  
_assets = {}

def load_assets():
    raw_player = pygame.image.load("assets/Player.png").convert_alpha()
    _assets["player_base"] = raw_player
    _assets["enemy"]  = pygame.image.load("assets/Enemy.png").convert_alpha()
    _assets["coin"]   = pygame.transform.smoothscale(
        pygame.image.load("assets/coin.png").convert_alpha(), (28, 28))
    _assets["road"]   = pygame.image.load("assets/AnimatedStreet.png").convert()

    for name, color, letter in [
        ("nitro",  (255, 160,  20), "N"),
        ("shield", ( 60, 160, 255), "S"),
        ("repair", ( 60, 200, 100), "R"),
    ]:
        s = pygame.Surface((32, 32), pygame.SRCALPHA)
        pygame.draw.circle(s, color, (16, 16), 15)
        pygame.draw.circle(s, (255,255,255), (16,16), 15, 2)
        f = pygame.font.SysFont("consolas", 18, bold=True)
        t = f.render(letter, True, (10, 10, 10))
        s.blit(t, t.get_rect(center=(16,16)))
        _assets[f"pu_{name}"] = s

def tinted_player(color_name):
    base = _assets["player_base"].copy()
    if CAR_TINTS[color_name] is None:
        return base
    tint = pygame.Surface(base.get_size(), pygame.SRCALPHA)
    tint.fill((*CAR_TINTS[color_name], 140))
    base.blit(tint, (0,0), special_flags=pygame.BLEND_RGBA_MULT)
    return base



class Player(pygame.sprite.Sprite):
    def __init__(self, color_name):
        super().__init__()
        self.image  = tinted_player(color_name)
        self.rect   = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom  = HEIGHT - 10
        self.speed  = 5
        self.shield = False
        self.nitro  = False

    def update(self):
        keys = pygame.key.get_pressed()
        spd  = self.speed * (1.6 if self.nitro else 1)
        if keys[pygame.K_LEFT]:  self.rect.move_ip(-spd, 0)
        if keys[pygame.K_RIGHT]: self.rect.move_ip( spd, 0)
        if self.rect.left  < ROAD_LEFT:  self.rect.left  = ROAD_LEFT
        if self.rect.right > ROAD_RIGHT: self.rect.right = ROAD_RIGHT


class Enemy(pygame.sprite.Sprite):
    def __init__(self, speed_ref, player_rect, stagger_y=0):
        super().__init__()
        self.image     = _assets["enemy"]
        self.rect      = self.image.get_rect()
        self.speed_ref = speed_ref  
        self._safe_reset(player_rect)
        self.rect.bottom = -stagger_y

    def _safe_reset(self, player_rect=None):
        for _ in range(20):
            x = random.randint(ROAD_LEFT, ROAD_RIGHT - self.rect.width)
            self.rect.left   = x
            self.rect.bottom = random.randint(-120, -20)
            if player_rect is None or not self.rect.inflate(10,10).colliderect(player_rect):
                return

    def update(self):
        self.rect.move_ip(0, self.speed_ref[0])
        if self.rect.top > HEIGHT:
            self._safe_reset()


class Obstacle(pygame.sprite.Sprite):
    KINDS = ["oil", "pothole", "barrier"]

    def __init__(self, speed_ref, player_rect):
        super().__init__()
        self.kind      = random.choice(self.KINDS)
        self.speed_ref = speed_ref
        self.image     = self._make_image()
        self.rect      = self.image.get_rect()
        self._safe_reset(player_rect)

    def _make_image(self):
        if self.kind == "oil":
            s = pygame.Surface((50, 30), pygame.SRCALPHA)
            pygame.draw.ellipse(s, (20, 20, 80, 200), (0, 0, 50, 30))
            pygame.draw.ellipse(s, (60, 60, 180, 120), (5, 5, 40, 20))
            return s
        elif self.kind == "pothole":
            s = pygame.Surface((38, 24), pygame.SRCALPHA)
            pygame.draw.ellipse(s, (40, 30, 20, 230), (0, 0, 38, 24))
            pygame.draw.ellipse(s, (25, 18, 10, 180), (4, 4, 30, 16))
            return s
        else: 
            s = pygame.Surface((60, 18), pygame.SRCALPHA)
            pygame.draw.rect(s, (220, 60, 30), (0, 0, 60, 18), border_radius=4)
            for i in range(0, 60, 12):
                pygame.draw.rect(s, (240, 220, 0), (i, 0, 6, 18))
            return s

    def _safe_reset(self, player_rect=None):
        for _ in range(20):
            x = random.randint(ROAD_LEFT, ROAD_RIGHT - self.rect.width)
            self.rect.left   = x
            self.rect.bottom = random.randint(-200, -40)
            if player_rect is None or not self.rect.inflate(10,10).colliderect(player_rect):
                return

    def update(self):
        self.rect.move_ip(0, self.speed_ref[0])
        if self.rect.top > HEIGHT:
            self._safe_reset()


class Coin(pygame.sprite.Sprite):
    def __init__(self, speed_ref, player_rect):
        super().__init__()
        self.image     = _assets["coin"]
        self.rect      = self.image.get_rect()
        self.speed_ref = speed_ref
        self._safe_reset(player_rect)

    def _safe_reset(self, player_rect=None):
        for _ in range(20):
            x = random.randint(ROAD_LEFT, ROAD_RIGHT - self.rect.width)
            self.rect.left   = x
            self.rect.bottom = random.randint(-300, -30)
            if player_rect is None or not self.rect.colliderect(player_rect):
                return

    def update(self):
        self.rect.move_ip(0, self.speed_ref[0])
        if self.rect.top > HEIGHT:
            self._safe_reset()


class PowerUp(pygame.sprite.Sprite):
    def __init__(self, kind, speed_ref, player_rect):
        super().__init__()
        self.kind      = kind   
        self.image     = _assets[f"pu_{kind}"]
        self.rect      = self.image.get_rect()
        self.speed_ref = speed_ref
        self.born      = pygame.time.get_ticks()
        x = random.randint(ROAD_LEFT, ROAD_RIGHT - self.rect.width)
        self.rect.left   = x
        self.rect.bottom = random.randint(-200, -40)

    def update(self):
        self.rect.move_ip(0, self.speed_ref[0])
        if (self.rect.top > HEIGHT or
                pygame.time.get_ticks() - self.born > POWERUP_TIMEOUT):
            self.kill()



def draw_hud(screen, score, distance, coins, speed,
             active_pu, pu_end_time, shield_active, font):
    bar = pygame.Surface((WIDTH, 46), pygame.SRCALPHA)
    bar.fill((0, 0, 0, 140))
    screen.blit(bar, (0, 0))

    left = font.render(f"Score:{score}  Dist:{distance}m  Coins:{coins}", True, (230,230,240))
    screen.blit(left, (6, 6))

    spd  = font.render(f"Speed:{speed:.1f}", True, (255,200,60))
    screen.blit(spd, (6, 26))

    if active_pu:
        remaining = max(0, (pu_end_time - pygame.time.get_ticks()) // 1000)
        pu_col = {"nitro": (255,160,20), "shield": (60,160,255), "repair": (60,200,100)}
        col    = pu_col.get(active_pu, (200,200,200))
        label  = font.render(f"{active_pu.upper()} {'∞' if active_pu=='shield' else str(remaining)+'s'}", True, col)
        screen.blit(label, (WIDTH - label.get_width() - 6, 6))

    if shield_active:
        pygame.draw.rect(screen, (60,160,255), (0,0,WIDTH,46), 2)


def draw_nitro_strip(screen, y):
    alpha = 80 + int(60 * abs((pygame.time.get_ticks() % 600) / 300 - 1))
    s = pygame.Surface((ROAD_RIGHT - ROAD_LEFT, 12), pygame.SRCALPHA)
    s.fill((255, 200, 0, alpha))
    screen.blit(s, (ROAD_LEFT, y))



def run_game(screen, clock, settings):
    diff_name = settings.get("difficulty", "normal")
    max_enemies, max_obs, coin_n, speed_start, inc_ms, spawn_ms = DIFF[diff_name]

    speed_ref = [speed_start]  

    player = Player(settings.get("car_color", "blue"))

    enemies       = pygame.sprite.Group(Enemy(speed_ref, player.rect, 200))
    obstacles     = pygame.sprite.Group(Obstacle(speed_ref, player.rect))
    coins_group   = pygame.sprite.Group(
        *[Coin(speed_ref, player.rect) for _ in range(coin_n)]
    )
    powerup_group = pygame.sprite.Group()
    all_sprites   = pygame.sprite.Group(player, *enemies, *obstacles, *coins_group)

    font      = pygame.font.SysFont("consolas", 13)
    road_y    = 0     
    SCORE     = 0
    coins_col = 0
    distance  = 0
    dist_acc  = 0.0   

    active_pu  = None
    pu_end     = 0

    nitro_strip_y = -999

    INC_SPEED     = pygame.USEREVENT + 1
    SPAWN_PU      = pygame.USEREVENT + 2
    ROAD_EVENT    = pygame.USEREVENT + 3
    SPAWN_TRAFFIC = pygame.USEREVENT + 4  
    pygame.time.set_timer(INC_SPEED,     inc_ms)
    pygame.time.set_timer(SPAWN_PU,      7000)
    pygame.time.set_timer(ROAD_EVENT,    12000)
    pygame.time.set_timer(SPAWN_TRAFFIC, spawn_ms)

    running = True
    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.time.set_timer(INC_SPEED, 0)
                pygame.time.set_timer(SPAWN_PU, 0)
                pygame.time.set_timer(ROAD_EVENT, 0)
                pygame.time.set_timer(SPAWN_TRAFFIC, 0)
                pygame.quit(); sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

            if event.type == INC_SPEED:
                speed_ref[0] = min(speed_ref[0] + 0.4, 18)

            if event.type == SPAWN_TRAFFIC:
                if len(enemies) < max_enemies:
                    e = Enemy(speed_ref, player.rect)
                    enemies.add(e)
                    all_sprites.add(e)
                elif len(obstacles) < max_obs:
                    o = Obstacle(speed_ref, player.rect)
                    obstacles.add(o)
                    all_sprites.add(o)

            if event.type == SPAWN_PU:
                if len(powerup_group) == 0:
                    kind = random.choice(["nitro", "shield", "repair"])
                    pu   = PowerUp(kind, speed_ref, player.rect)
                    powerup_group.add(pu)
                    all_sprites.add(pu)

            if event.type == ROAD_EVENT:
                nitro_strip_y = random.randint(100, HEIGHT - 100)

        player.update()
        enemies.update()
        obstacles.update()
        coins_group.update()
        powerup_group.update()

        if active_pu and pygame.time.get_ticks() > pu_end:
            if active_pu == "nitro":
                player.nitro  = False
            active_pu = None

        dist_acc += speed_ref[0] / 20.0
        if dist_acc >= 1:
            distance  += int(dist_acc)
            dist_acc  -= int(dist_acc)
        SCORE = distance + coins_col * 10

        road_y = (road_y + speed_ref[0]) % _assets["road"].get_height()

        # coins
        hit_coins = pygame.sprite.spritecollide(player, coins_group, False)
        for c in hit_coins:
            coins_col += 1
            c._safe_reset(player.rect)

        hit_pu = pygame.sprite.spritecollide(player, powerup_group, True)
        for pu in hit_pu:
            if active_pu == "nitro":
                player.nitro = False
            active_pu = pu.kind
            if pu.kind == "nitro":
                player.nitro = True
                pu_end = pygame.time.get_ticks() + NITRO_DURATION
            elif pu.kind == "shield":
                player.shield = True
                pu_end = pygame.time.get_ticks() + SHIELD_DURATION
            elif pu.kind == "repair":
                obs_list = list(obstacles)
                if obs_list:
                    obs_list[0]._safe_reset(player.rect)
                active_pu = None

        if abs(player.rect.centery - nitro_strip_y) < 20:
            if not (active_pu == "nitro"):
                player.nitro  = True
                active_pu     = "nitro"
                pu_end        = pygame.time.get_ticks() + NITRO_DURATION
            nitro_strip_y = -999

        if pygame.sprite.spritecollideany(player, enemies):
            if player.shield:
                player.shield = False
                active_pu     = None
                for e in enemies:
                    if e.rect.colliderect(player.rect):
                        e._safe_reset(player.rect)
            else:
                pygame.time.set_timer(INC_SPEED, 0)
                pygame.time.set_timer(SPAWN_PU, 0)
                pygame.time.set_timer(ROAD_EVENT, 0)
                pygame.time.set_timer(SPAWN_TRAFFIC, 0)
                return SCORE, distance, coins_col

        if pygame.sprite.spritecollideany(player, obstacles):
            if player.shield:
                player.shield = False
                active_pu     = None
            else:
                pygame.time.set_timer(INC_SPEED, 0)
                pygame.time.set_timer(SPAWN_PU, 0)
                pygame.time.set_timer(ROAD_EVENT, 0)
                pygame.time.set_timer(SPAWN_TRAFFIC, 0)
                return SCORE, distance, coins_col

        road_h = _assets["road"].get_height()
        screen.blit(_assets["road"], (0, road_y - road_h))
        screen.blit(_assets["road"], (0, road_y))

        if 0 < nitro_strip_y < HEIGHT:
            draw_nitro_strip(screen, nitro_strip_y)

        if player.shield:
            glow = pygame.Surface(
                (player.rect.width+12, player.rect.height+12), pygame.SRCALPHA)
            pygame.draw.ellipse(glow, (60,160,255,80), glow.get_rect())
            screen.blit(glow, (player.rect.x-6, player.rect.y-6))

        enemies.draw(screen)
        obstacles.draw(screen)
        coins_group.draw(screen)
        powerup_group.draw(screen)
        screen.blit(player.image, player.rect)

        draw_hud(screen, SCORE, distance, coins_col, speed_ref[0],
                 active_pu, pu_end, player.shield, font)

        pygame.display.flip()

    pygame.time.set_timer(INC_SPEED, 0)
    pygame.time.set_timer(SPAWN_PU, 0)
    pygame.time.set_timer(ROAD_EVENT, 0)
    pygame.time.set_timer(SPAWN_TRAFFIC, 0)
    return SCORE, distance, coins_col