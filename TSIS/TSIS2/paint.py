import pygame
import sys
from datetime import datetime
from tools import COLORS, BRUSH_SIZES, BRUSH_LABELS

WIDTH, HEIGHT = 1200, 750
TOOLBAR_W = 220
CANVAS_X  = TOOLBAR_W
CANVAS_W  = WIDTH - TOOLBAR_W
FPS       = 60

BG        = (18,  18,  24)
PANEL_BG  = (26,  26,  36)
PANEL_DRK = (15,  15,  20)
ACCENT    = (100, 200, 255)
ACCENT2   = (255, 120, 180)
TEXT_COL  = (220, 220, 235)
TEXT_DIM  = (120, 120, 140)
BORDER    = (45,  45,  60)
HOVER     = (40,  40,  58)
ACTIVE_BG = (30,  80,  130)


def lerp_color(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))

def rrect(surf, color, rect, r, bw=0, bc=None):
    pygame.draw.rect(surf, color, rect, border_radius=r)
    if bw and bc:
        pygame.draw.rect(surf, bc, rect, bw, border_radius=r)

def section(surf, font, text, x, y):
    surf.blit(font.render(text.upper(), True, TEXT_DIM), (x, y))
    pygame.draw.line(surf, BORDER, (x, y + 18), (TOOLBAR_W - 14, y + 18), 1)

def calc_rect(x1, y1, x2, y2):
    return pygame.Rect(min(x1,x2), min(y1,y2), abs(x1-x2), abs(y1-y2))

TOOL_DEFS = [
    ("pencil", "P", "Pencil",    "P"),
    ("line",   "/", "Line",      "L"),
    ("rect",   "R", "Rectangle", "R"),
    ("circle", "O", "Circle",    "C"),
    ("fill",   "F", "Fill",      "F"),
    ("text",   "T", "Text",      "T"),
]

def tool_rect(i):
    return pygame.Rect(10 + (i % 2) * 101, 48 + (i // 2) * 54, 96, 46)

def color_rect(i):
    return pygame.Rect(10 + (i % 4) * 48, 230 + (i // 4) * 46, 40, 40)

def brush_rect(i):
    return pygame.Rect(10, 394 + i * 50, TOOLBAR_W - 20, 42)

ACTION_RECTS = {
    "clear": pygame.Rect(10,                          HEIGHT-100, (TOOLBAR_W-25)//2, 36),
    "save":  pygame.Rect(10+(TOOLBAR_W-25)//2+5,      HEIGHT-100, (TOOLBAR_W-25)//2, 36),
}

def flood_fill(canvas, sx, sy, fill_color):
    from collections import deque
    w, h = canvas.get_size()
    if not (0 <= sx < w and 0 <= sy < h):
        return
    target = canvas.get_at((sx, sy))[:3]
    fill   = fill_color[:3]
    if target == fill:
        return
    q    = deque([(sx, sy)])
    seen = {(sx, sy)}
    while q:
        x, y = q.popleft()
        canvas.set_at((x, y), fill)
        for nx, ny in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
            if 0 <= nx < w and 0 <= ny < h and (nx,ny) not in seen:
                if canvas.get_at((nx, ny))[:3] == target:
                    seen.add((nx, ny))
                    q.append((nx, ny))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Studio Paint  · TSIS2")
    clock  = pygame.time.Clock()

    font_sm  = pygame.font.SysFont("consolas", 11)
    font_med = pygame.font.SysFont("consolas", 13)
    font_lg  = pygame.font.SysFont("consolas", 15, bold=True)

    canvas     = pygame.Surface((CANVAS_W, HEIGHT))
    base_layer = pygame.Surface((CANVAS_W, HEIGHT))   
    canvas.fill((255, 255, 255))
    base_layer.fill((255, 255, 255))

    tool_name  = "pencil"
    color_idx  = 0
    brush_idx  = 1
    draw_color = COLORS[color_idx]
    brush_size = BRUSH_SIZES[brush_idx]

    LMBpressed = False
    startX = startY = 0   
    prevX  = prevY  = 0   

    text_active = False
    text_pos    = (0, 0)
    text_buffer = ""
    text_blink  = 0

    hov_tool = hov_color = hov_brush = hov_action = None

    status_msg   = "Ready"
    status_timer = 0

    def set_status(msg, frames=180):
        nonlocal status_msg, status_timer
        status_msg, status_timer = msg, frames

    def save_canvas():
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        fname = f"canvas_{ts}.png"
        pygame.image.save(canvas, fname)
        set_status(f"Saved -> {fname}")

    def in_canvas(mx, my):
        return CANVAS_X <= mx < WIDTH and 0 <= my < HEIGHT

    def cv(mx, my):
        return mx - CANVAS_X, my

    def text_font():
        size = {2: 14, 5: 20, 10: 32}.get(brush_size, 20)
        return pygame.font.SysFont("consolas", size)

    def text_commit():
        nonlocal text_active, text_buffer
        if text_buffer:
            canvas.blit(text_font().render(text_buffer, True, draw_color), text_pos)
            base_layer.blit(canvas, (0, 0))
        text_active = False
        text_buffer = ""

    def draw_toolbar():
        pygame.draw.rect(screen, PANEL_BG, (0, 0, TOOLBAR_W, HEIGHT))
        pygame.draw.line(screen, BORDER, (TOOLBAR_W-1, 0), (TOOLBAR_W-1, HEIGHT), 2)

        screen.blit(font_lg.render("STUDIO PAINT", True, ACCENT), (10, 12))
        pygame.draw.line(screen, ACCENT, (10, 32), (TOOLBAR_W-14, 32), 1)

        section(screen, font_sm, "Tools", 10, 38)
        for i, (tname, icon, label, key) in enumerate(TOOL_DEFS):
            r   = tool_rect(i)
            act = (tool_name == tname)
            hov = (hov_tool == tname)
            rrect(screen, ACTIVE_BG if act else (HOVER if hov else PANEL_DRK),
                  r, 8, 1, ACCENT if act else BORDER)
            screen.blit(font_med.render(icon,      True, ACCENT if act else TEXT_COL), (r.x+8,  r.y+8))
            screen.blit(font_sm .render(label,     True, ACCENT if act else TEXT_COL), (r.x+28, r.y+6))
            screen.blit(font_sm .render(f"[{key}]",True, TEXT_DIM),                   (r.x+28, r.y+20))

        section(screen, font_sm, "Color", 10, 218)
        for i, col in enumerate(COLORS):
            r   = color_rect(i)
            act = (i == color_idx)
            hov = (hov_color == i)
            pygame.draw.rect(screen, col, r, border_radius=6)
            if act:
                pygame.draw.rect(screen, ACCENT,        r,            2, border_radius=6)
                pygame.draw.rect(screen, (255,255,255), r.inflate(-4,-4), 1, border_radius=4)
            elif hov:
                pygame.draw.rect(screen, TEXT_COL, r, 1, border_radius=6)

        section(screen, font_sm, "Brush Size", 10, 376)
        for i, (sz, lbl) in enumerate(zip(BRUSH_SIZES, BRUSH_LABELS)):
            r   = brush_rect(i)
            act = (i == brush_idx)
            hov = (hov_brush == i)
            rrect(screen, ACTIVE_BG if act else (HOVER if hov else PANEL_DRK),
                  r, 6, 1, ACCENT if act else BORDER)
            mid = r.y + r.h // 2
            pygame.draw.line(screen, draw_color, (r.x+10, mid), (r.x+45, mid), sz)
            screen.blit(font_med.render(lbl,        True, ACCENT if act else TEXT_COL), (r.x+55, r.y+10))
            screen.blit(font_sm .render(f"[{i+1}]", True, TEXT_DIM),                   (r.x+55, r.y+24))

        for aname, r in ACTION_RECTS.items():
            hov = (hov_action == aname)
            col = (200,70,70) if aname == "clear" else (50,160,80)
            bg  = lerp_color(PANEL_DRK, col, 0.35 if hov else 0.15)
            rrect(screen, bg, r, 7, 1, lerp_color(BORDER, col, 0.6))
            lbl = "Clear" if aname == "clear" else "Save (^S)"
            t   = font_med.render(lbl, True, lerp_color(TEXT_DIM, TEXT_COL, 0.7 if hov else 0.3))
            screen.blit(t, (r.x+(r.w-t.get_width())//2, r.y+(r.h-t.get_height())//2))

        if status_timer > 0:
            c = lerp_color(PANEL_BG, ACCENT2, min(status_timer*4, 255)/255)
            screen.blit(font_sm.render(status_msg, True, c), (10, HEIGHT-52))

        mx, my = pygame.mouse.get_pos()
        if in_canvas(mx, my):
            x, y = cv(mx, my)
            screen.blit(font_sm.render(f"x:{x}  y:{y}", True, TEXT_DIM), (10, HEIGHT-32))

    running = True
    while running:
        clock.tick(FPS)
        mx, my = pygame.mouse.get_pos()
        cx, cy = cv(mx, my)

        hov_tool   = next((t for i,(t,*_) in enumerate(TOOL_DEFS) if tool_rect(i) .collidepoint(mx,my)), None)
        hov_color  = next((i for i in range(len(COLORS))      if color_rect(i).collidepoint(mx,my)), None)
        hov_brush  = next((i for i in range(len(BRUSH_SIZES)) if brush_rect(i).collidepoint(mx,my)), None)
        hov_action = next((a for a,r in ACTION_RECTS.items()  if r             .collidepoint(mx,my)), None)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                mods = pygame.key.get_mods()
                if mods & pygame.KMOD_CTRL and event.key == pygame.K_s:
                    save_canvas()
                elif event.key == pygame.K_p: tool_name = "pencil"
                elif event.key == pygame.K_l: tool_name = "line"
                elif event.key == pygame.K_r: tool_name = "rect"
                elif event.key == pygame.K_c: tool_name = "circle"
                elif event.key == pygame.K_f: tool_name = "fill"
                elif event.key == pygame.K_t: tool_name = "text"
                elif event.key == pygame.K_1: brush_idx = 0; brush_size = BRUSH_SIZES[0]
                elif event.key == pygame.K_2: brush_idx = 1; brush_size = BRUSH_SIZES[1]
                elif event.key == pygame.K_3: brush_idx = 2; brush_size = BRUSH_SIZES[2]

                if text_active:
                    if   event.key == pygame.K_RETURN:    text_commit()
                    elif event.key == pygame.K_ESCAPE:    text_active = False; text_buffer = ""
                    elif event.key == pygame.K_BACKSPACE: text_buffer = text_buffer[:-1]
                    elif event.unicode and event.unicode.isprintable():
                        text_buffer += event.unicode

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                LMBpressed = True

                for i,(tname,*_) in enumerate(TOOL_DEFS):
                    if tool_rect(i).collidepoint(mx, my):  tool_name = tname
                for i in range(len(COLORS)):
                    if color_rect(i).collidepoint(mx, my): color_idx = i; draw_color = COLORS[i]
                for i in range(len(BRUSH_SIZES)):
                    if brush_rect(i).collidepoint(mx, my): brush_idx = i; brush_size = BRUSH_SIZES[i]
                if hov_action == "clear":
                    canvas.fill((255,255,255)); base_layer.fill((255,255,255))
                    set_status("Canvas cleared")
                elif hov_action == "save":
                    save_canvas()

                if in_canvas(mx, my):
                    startX, startY = cx, cy   
                    prevX,  prevY  = cx, cy   

                    if tool_name == "pencil":
                        pygame.draw.circle(canvas, draw_color, (cx, cy), brush_size // 2)

                    elif tool_name == "fill":
                        flood_fill(canvas, cx, cy, draw_color)
                        base_layer.blit(canvas, (0, 0))

                    elif tool_name == "text":
                        if text_active and text_buffer:
                            text_commit()
                        text_active = True
                        text_pos    = (cx, cy)
                        text_buffer = ""

            elif event.type == pygame.MOUSEMOTION:
                if LMBpressed and in_canvas(mx, my):

                    if tool_name == "pencil":
                        pygame.draw.line(canvas, draw_color, (prevX,prevY), (cx,cy), brush_size)
                        pygame.draw.circle(canvas, draw_color, (cx,cy), brush_size // 2)

                    elif tool_name in ("line", "rect", "circle"):
                        canvas.blit(base_layer, (0, 0))
                        if tool_name == "line":
                            pygame.draw.line(canvas, draw_color, (startX,startY), (cx,cy), brush_size)
                        elif tool_name == "rect":
                            pygame.draw.rect(canvas, draw_color, calc_rect(startX,startY,cx,cy), brush_size)
                        elif tool_name == "circle":
                            r = max(int((abs(cx-startX)+abs(cy-startY))//2), 1)
                            pygame.draw.circle(canvas, draw_color, (startX,startY), r, brush_size)

                prevX, prevY = cx, cy   

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                LMBpressed = False
                if in_canvas(mx, my) and tool_name in ("line", "rect", "circle"):
                    canvas.blit(base_layer, (0, 0))
                    if tool_name == "line":
                        pygame.draw.line(canvas, draw_color, (startX,startY), (cx,cy), brush_size)
                    elif tool_name == "rect":
                        pygame.draw.rect(canvas, draw_color, calc_rect(startX,startY,cx,cy), brush_size)
                    elif tool_name == "circle":
                        r = max(int((abs(cx-startX)+abs(cy-startY))//2), 1)
                        pygame.draw.circle(canvas, draw_color, (startX,startY), r, brush_size)
                    base_layer.blit(canvas, (0, 0))  
                elif tool_name == "pencil" and LMBpressed is False:
                    base_layer.blit(canvas, (0, 0))   

        if status_timer > 0:
            status_timer -= 1

        screen.fill(BG)
        pygame.draw.rect(screen, (40,40,50), (CANVAS_X-4,-4,CANVAS_W+8,HEIGHT+8), border_radius=4)
        screen.blit(canvas, (CANVAS_X, 0))

        if text_active:
            text_blink = (text_blink + 1) % 60
            f    = text_font()
            surf = f.render(text_buffer, True, draw_color)
            px, py = text_pos[0] + CANVAS_X, text_pos[1]
            screen.blit(surf, (px, py))
            if text_blink < 30:
                bx = px + surf.get_width() + 2
                pygame.draw.line(screen, draw_color, (bx, py), (bx, py + surf.get_height()), 2)

        draw_toolbar()
        pygame.draw.rect(screen, BORDER, (CANVAS_X, 0, CANVAS_W, HEIGHT), 1)
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()