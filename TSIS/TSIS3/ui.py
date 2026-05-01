import pygame
from persistence import load_leaderboard, save_settings

BG      = (30,  30,  30)
PANEL   = (45,  45,  55)
ACCENT  = (80,  180, 255)
ACCENT2 = (255, 200,  50)
WHITE   = (230, 230, 240)
DIM     = (130, 130, 150)
RED     = (220,  60,  60)
GREEN   = (60,  200, 100)
BORDER  = (70,   70,  90)

def lerp(a, b, t):
    return tuple(int(a[i] + (b[i]-a[i])*t) for i in range(3))

def rrect(surf, color, rect, r=8, bw=0, bc=None):
    pygame.draw.rect(surf, color, rect, border_radius=r)
    if bw and bc:
        pygame.draw.rect(surf, bc, rect, bw, border_radius=r)

class Button:
    def __init__(self, rect, label, color=ACCENT, tc=(10,10,20)):
        self.rect    = pygame.Rect(rect)
        self.label   = label
        self.color   = color
        self.tc      = tc
        self.hovered = False
    def draw(self, surf, font):
        col = lerp(self.color, WHITE, 0.25) if self.hovered else self.color
        rrect(surf, col, self.rect, 10)
        t = font.render(self.label, True, self.tc)
        surf.blit(t, t.get_rect(center=self.rect.center))
    def update(self, mx, my):
        self.hovered = self.rect.collidepoint(mx, my)
    def clicked(self, mx, my):
        return self.rect.collidepoint(mx, my)

def username_screen(screen, clock, bg_img):
    W, H = screen.get_size()
    ft   = pygame.font.SysFont("consolas", 34, bold=True)
    fb   = pygame.font.SysFont("consolas", 22)
    fs   = pygame.font.SysFont("consolas", 15)
    name = ""
    btn  = Button((W//2-80, H//2+70, 160, 44), "START", GREEN, (10,10,10))
    while True:
        mx, my = pygame.mouse.get_pos()
        btn.update(mx, my)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); raise SystemExit
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name.strip():
                    return name.strip()
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif event.unicode.isprintable() and len(name) < 16:
                    name += event.unicode
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if btn.clicked(mx, my) and name.strip():
                    return name.strip()
        screen.blit(bg_img, (0, 0))
        overlay = pygame.Surface((W, H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        screen.blit(overlay, (0, 0))
        t = ft.render("ENTER YOUR NAME", True, ACCENT)
        screen.blit(t, t.get_rect(center=(W//2, H//2-80)))
        box = pygame.Rect(W//2-140, H//2-20, 280, 48)
        rrect(screen, PANEL, box, 8, 1, ACCENT)
        cursor = "|" if pygame.time.get_ticks() % 900 < 450 else " "
        nt = fb.render(name + cursor, True, WHITE)
        screen.blit(nt, nt.get_rect(center=box.center))
        hint = fs.render("max 16 chars · Enter to confirm", True, DIM)
        screen.blit(hint, hint.get_rect(center=(W//2, H//2+44)))
        btn.draw(screen, fb)
        pygame.display.flip()
        clock.tick(60)

def main_menu(screen, clock, bg_img):
    W, H = screen.get_size()
    ft   = pygame.font.SysFont("consolas", 52, bold=True)
    fb   = pygame.font.SysFont("consolas", 22)
    bw, bh, cx = 220, 50, W//2-110
    buttons = [
        Button((cx, 230, bw, bh), "PLAY",        GREEN),
        Button((cx, 300, bw, bh), "LEADERBOARD", ACCENT),
        Button((cx, 370, bw, bh), "SETTINGS",    ACCENT),
        Button((cx, 440, bw, bh), "QUIT",        RED),
    ]
    actions = ["play", "leaderboard", "settings", "quit"]
    while True:
        mx, my = pygame.mouse.get_pos()
        for b in buttons: b.update(mx, my)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for b, a in zip(buttons, actions):
                    if b.clicked(mx, my): return a
        screen.blit(bg_img, (0, 0))
        overlay = pygame.Surface((W, H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 140))
        screen.blit(overlay, (0, 0))
        t = ft.render("RACER", True, ACCENT2)
        screen.blit(t, t.get_rect(center=(W//2, 140)))
        sub = fb.render("TSIS3  ·  Pygame", True, DIM)
        screen.blit(sub, sub.get_rect(center=(W//2, 192)))
        for b in buttons: b.draw(screen, fb)
        pygame.display.flip()
        clock.tick(60)

def settings_screen(screen, clock, settings, bg_img):
    W, H = screen.get_size()
    ft   = pygame.font.SysFont("consolas", 34, bold=True)
    fb   = pygame.font.SysFont("consolas", 20)
    fs   = pygame.font.SysFont("consolas", 15)
    btn_back = Button((W//2-90, H-80, 180, 44), "BACK", ACCENT)
    car_colors   = ["blue", "red", "green"]
    difficulties = ["easy", "normal", "hard"]
    rows = [
        ("Sound",      200),
        ("Car Color",  265),
        ("Difficulty", 330),
    ]
    while True:
        mx, my = pygame.mouse.get_pos()
        btn_back.update(mx, my)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_settings(settings); return settings
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                save_settings(settings); return settings
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if btn_back.clicked(mx, my):
                    save_settings(settings); return settings
                if pygame.Rect(W//2+20, 200, 130, 36).collidepoint(mx, my):
                    settings["sound"] = not settings["sound"]
                if pygame.Rect(W//2+20, 265, 130, 36).collidepoint(mx, my):
                    idx = car_colors.index(settings["car_color"])
                    settings["car_color"] = car_colors[(idx+1) % len(car_colors)]
                if pygame.Rect(W//2+20, 330, 130, 36).collidepoint(mx, my):
                    idx = difficulties.index(settings["difficulty"])
                    settings["difficulty"] = difficulties[(idx+1) % len(difficulties)]
        screen.blit(bg_img, (0, 0))
        overlay = pygame.Surface((W, H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))
        t = ft.render("SETTINGS", True, ACCENT)
        screen.blit(t, t.get_rect(center=(W//2, 120)))
        values = [
            "ON" if settings["sound"] else "OFF",
            settings["car_color"].upper(),
            settings["difficulty"].upper(),
        ]
        for (label, y), value in zip(rows, values):
            lbl = fb.render(label, True, WHITE)
            screen.blit(lbl, (W//2-180, y+8))
            col = GREEN if value in ("ON","EASY") else (RED if value=="HARD" else ACCENT)
            rrect(screen, PANEL, (W//2+20, y, 130, 36), 8, 1, col)
            vt = fb.render(value, True, col)
            screen.blit(vt, vt.get_rect(center=(W//2+85, y+18)))
        hint = fs.render("click a value to toggle", True, DIM)
        screen.blit(hint, hint.get_rect(center=(W//2, 385)))
        btn_back.draw(screen, fb)
        pygame.display.flip()
        clock.tick(60)

def leaderboard_screen(screen, clock, bg_img):
    W, H = screen.get_size()
    ft   = pygame.font.SysFont("consolas", 32, bold=True)
    fb   = pygame.font.SysFont("consolas", 18)
    fs   = pygame.font.SysFont("consolas", 14)
    btn_back = Button((W//2-90, H-70, 180, 44), "BACK", ACCENT)
    board = load_leaderboard()
    while True:
        mx, my = pygame.mouse.get_pos()
        btn_back.update(mx, my)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: return
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if btn_back.clicked(mx, my): return
        screen.blit(bg_img, (0, 0))
        overlay = pygame.Surface((W, H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 155))
        screen.blit(overlay, (0, 0))
        t = ft.render("TOP 10 LEADERBOARD", True, ACCENT2)
        screen.blit(t, t.get_rect(center=(W//2, 55)))
        hdr = fs.render(f"{'#':<3} {'NAME':<14} {'SCORE':>7} {'DIST':>7}", True, DIM)
        screen.blit(hdr, (30, 100))
        pygame.draw.line(screen, BORDER, (30, 118), (W-30, 118), 1)
        for i, e in enumerate(board):
            y   = 126 + i*34
            col = ACCENT2 if i==0 else (WHITE if i<3 else DIM)
            row = fb.render(f"{i+1:<3} {e['name']:<14} {e['score']:>7} {e['distance']:>5}m", True, col)
            screen.blit(row, (30, y))
        if not board:
            empty = fb.render("no scores yet — play a game!", True, DIM)
            screen.blit(empty, empty.get_rect(center=(W//2, 240)))
        btn_back.draw(screen, fb)
        pygame.display.flip()
        clock.tick(60)

def game_over_screen(screen, clock, score, distance, coins, bg_img):
    W, H = screen.get_size()
    ft   = pygame.font.SysFont("consolas", 46, bold=True)
    fb   = pygame.font.SysFont("consolas", 20)
    fs   = pygame.font.SysFont("consolas", 17)
    bw, bh = 170, 46
    btn_retry = Button((W//2-bw-8, H//2+100, bw, bh), "RETRY",     GREEN)
    btn_menu  = Button((W//2+8,    H//2+100, bw, bh), "MAIN MENU", ACCENT)
    overlay   = pygame.Surface((W, H), pygame.SRCALPHA)
    for alpha in range(0, 170, 8):
        overlay.fill((0, 0, 0, alpha))
        screen.blit(bg_img, (0, 0))
        screen.blit(overlay, (0, 0))
        pygame.display.flip()
        clock.tick(60)
    while True:
        mx, my = pygame.mouse.get_pos()
        btn_retry.update(mx, my)
        btn_menu .update(mx, my)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if btn_retry.clicked(mx, my): return "retry"
                if btn_menu .clicked(mx, my): return "menu"
        screen.blit(bg_img, (0, 0))
        overlay.fill((0, 0, 0, 168))
        screen.blit(overlay, (0, 0))
        t = ft.render("GAME OVER", True, RED)
        screen.blit(t, t.get_rect(center=(W//2, H//2-110)))
        for j, line in enumerate([
            f"Score    : {score}",
            f"Distance : {distance} m",
            f"Coins    : {coins}",
        ]):
            st = fs.render(line, True, WHITE)
            screen.blit(st, st.get_rect(center=(W//2, H//2-30+j*34)))
        btn_retry.draw(screen, fb)
        btn_menu .draw(screen, fb)
        pygame.display.flip()
        clock.tick(60)