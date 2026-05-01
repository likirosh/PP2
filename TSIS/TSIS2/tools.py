"""
tools.py — All drawing tool implementations for Studio Paint.
Each tool exposes:
    on_mouse_down(canvas, x, y, color, size)
    on_mouse_drag(canvas, x, y, color, size)
    on_mouse_up  (canvas, x, y, color, size)
    draw_preview (surface, x, y, color, size)   ← overlay (SRCALPHA)
"""

import pygame
from collections import deque

# ── Color Palette ────────────────────────────────────────────────────────────
COLORS = [
    (0,   0,   0),      # Black
    (255, 255, 255),    # White
    (220,  50,  50),    # Red
    (240, 130,  40),    # Orange
    (240, 210,  40),    # Yellow
    (60,  180,  75),    # Green
    (30,  120, 220),    # Blue
    (100,  50, 200),    # Purple
    (220,  90, 180),    # Pink
    (40,  200, 200),    # Cyan
    (160,  82,  45),    # Brown
    (128, 128, 128),    # Gray
]

# ── Brush Sizes ───────────────────────────────────────────────────────────────
BRUSH_SIZES  = [2, 5, 10]
BRUSH_LABELS = ["Small  (2px)", "Medium (5px)", "Large (10px)"]


# ── Base Tool ────────────────────────────────────────────────────────────────
class BaseTool:
    def on_mouse_down(self, canvas, x, y, color, size): pass
    def on_mouse_drag(self, canvas, x, y, color, size): pass
    def on_mouse_up  (self, canvas, x, y, color, size): pass
    def draw_preview (self, surface, x, y, color, size): pass


# ── 3.1  Pencil Tool ─────────────────────────────────────────────────────────
class PencilTool(BaseTool):
    def __init__(self):
        self._last = None
        self._drawing = False

    def on_mouse_down(self, canvas, x, y, color, size):
        self._drawing = True
        self._last = (x, y)
        pygame.draw.circle(canvas, color, (x, y), size // 2)

    def on_mouse_drag(self, canvas, x, y, color, size):
        if self._drawing and self._last:
            pygame.draw.line(canvas, color, self._last, (x, y), size)
            # Fill gaps at corners with circles
            pygame.draw.circle(canvas, color, (x, y), size // 2)
            self._last = (x, y)

    def on_mouse_up(self, canvas, x, y, color, size):
        self._drawing = False
        self._last = None

    def draw_preview(self, surface, x, y, color, size):
        # Show a crosshair cursor ring
        r = max(size // 2, 1)
        pygame.draw.circle(surface, (*color, 120), (x, y), r + 2, 1)


# ── 3.1  Line Tool ────────────────────────────────────────────────────────────
class LineTool(BaseTool):
    def __init__(self):
        self._start  = None
        self._active = False

    def on_mouse_down(self, canvas, x, y, color, size):
        self._start  = (x, y)
        self._active = True
        self._cur    = (x, y)

    def on_mouse_drag(self, canvas, x, y, color, size):
        if self._active:
            self._cur = (x, y)

    def on_mouse_up(self, canvas, x, y, color, size):
        if self._active and self._start:
            pygame.draw.line(canvas, color, self._start, (x, y), size)
        self._active = False
        self._start  = None

    def draw_preview(self, surface, x, y, color, size):
        if self._active and self._start:
            pygame.draw.line(surface, (*color, 180), self._start, (x, y), size)
            # Start/end dots
            pygame.draw.circle(surface, (*color, 220), self._start, size // 2 + 3, 1)
            pygame.draw.circle(surface, (*color, 220), (x, y), size // 2 + 3, 1)


# ── Rectangle Tool ────────────────────────────────────────────────────────────
class RectTool(BaseTool):
    def __init__(self):
        self._start  = None
        self._active = False

    def on_mouse_down(self, canvas, x, y, color, size):
        self._start  = (x, y)
        self._active = True

    def on_mouse_drag(self, canvas, x, y, color, size):
        if self._active:
            self._cur = (x, y)

    def on_mouse_up(self, canvas, x, y, color, size):
        if self._active and self._start:
            r = _rect_from_points(self._start, (x, y))
            pygame.draw.rect(canvas, color, r, size)
        self._active = False

    def draw_preview(self, surface, x, y, color, size):
        if self._active and self._start:
            r = _rect_from_points(self._start, (x, y))
            pygame.draw.rect(surface, (*color, 160), r, size)
            pygame.draw.rect(surface, (*color, 80),  r.inflate(2, 2), 1)


# ── Circle Tool ───────────────────────────────────────────────────────────────
class CircleTool(BaseTool):
    def __init__(self):
        self._start  = None
        self._active = False

    def on_mouse_down(self, canvas, x, y, color, size):
        self._start  = (x, y)
        self._active = True

    def on_mouse_drag(self, canvas, x, y, color, size):
        if self._active:
            self._cur = (x, y)

    def on_mouse_up(self, canvas, x, y, color, size):
        if self._active and self._start:
            cx, cy = self._start
            rx = abs(x - cx)
            ry = abs(y - cy)
            r  = max(int((rx + ry) / 2), 1)
            pygame.draw.circle(canvas, color, (cx, cy), r, size)
        self._active = False

    def draw_preview(self, surface, x, y, color, size):
        if self._active and self._start:
            cx, cy = self._start
            rx = abs(x - cx)
            ry = abs(y - cy)
            r  = max(int((rx + ry) / 2), 1)
            pygame.draw.circle(surface, (*color, 150), (cx, cy), r, size)
            # Center dot
            pygame.draw.circle(surface, (*color, 200), (cx, cy), 3)


# ── 3.3  Fill Tool ────────────────────────────────────────────────────────────
class FillTool(BaseTool):
    def on_mouse_down(self, canvas, x, y, color, size):
        _flood_fill(canvas, x, y, color)

    def draw_preview(self, surface, x, y, color, size):
        # Bucket cursor indicator
        pygame.draw.circle(surface, (*color, 200), (x, y), 6)
        pygame.draw.circle(surface, (255, 255, 255, 120), (x, y), 6, 1)


def _flood_fill(canvas: pygame.Surface, sx: int, sy: int, fill_color):
    """BFS flood fill using get_at / set_at."""
    w, h = canvas.get_size()
    if not (0 <= sx < w and 0 <= sy < h):
        return

    target = canvas.get_at((sx, sy))[:3]      # ignore alpha
    fill   = fill_color[:3] if len(fill_color) >= 3 else fill_color

    if target == fill:
        return

    queue = deque()
    queue.append((sx, sy))
    visited = set()
    visited.add((sx, sy))

    while queue:
        x, y = queue.popleft()
        canvas.set_at((x, y), fill)
        for nx, ny in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
            if (0 <= nx < w and 0 <= ny < h and
                    (nx, ny) not in visited and
                    canvas.get_at((nx, ny))[:3] == target):
                visited.add((nx, ny))
                queue.append((nx, ny))


# ── 3.5  Text Tool ────────────────────────────────────────────────────────────
class TextTool(BaseTool):
    def __init__(self):
        self._active   = False
        self._pos      = None
        self._buffer   = ""
        self._blink    = 0
        self._font     = None

    def _get_font(self, size):
        fs = {2: 14, 5: 20, 10: 32}.get(size, 20)
        if self._font is None or self._font_size != fs:
            self._font      = pygame.font.SysFont("consolas", fs)
            self._font_size = fs
        return self._font

    def on_mouse_down(self, canvas, x, y, color, size):
        # Commit any in-progress text first
        if self._active and self._buffer:
            self._commit(canvas, color, size)
        self._active = True
        self._pos    = (x, y)
        self._buffer = ""
        self._blink  = 0

    def handle_key(self, event, canvas, color, size):
        if not self._active:
            return
        if event.key == pygame.K_RETURN:
            self._commit(canvas, color, size)
        elif event.key == pygame.K_ESCAPE:
            self._active = False
            self._buffer = ""
        elif event.key == pygame.K_BACKSPACE:
            self._buffer = self._buffer[:-1]
        else:
            ch = event.unicode
            if ch and ch.isprintable():
                self._buffer += ch

    def _commit(self, canvas, color, size):
        if self._buffer and self._pos:
            font = self._get_font(size)
            surf = font.render(self._buffer, True, color)
            canvas.blit(surf, self._pos)
        self._active = False
        self._buffer = ""

    def draw_preview(self, surface, x, y, color, size):
        pass  # cursor drawn separately in main loop

    def draw_cursor(self, screen, canvas_x, color):
        if not self._active or not self._pos:
            return
        self._blink = (self._blink + 1) % 60
        # Re-render live text
        font  = self._font if self._font else pygame.font.SysFont("consolas", 20)
        surf  = font.render(self._buffer, True, color)
        px, py = self._pos[0] + canvas_x, self._pos[1]
        screen.blit(surf, (px, py))
        # Blinking cursor bar
        if self._blink < 30:
            cx = px + surf.get_width() + 2
            pygame.draw.line(screen, color, (cx, py), (cx, py + surf.get_height()), 2)


# ── Utility ───────────────────────────────────────────────────────────────────

def _rect_from_points(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return pygame.Rect(min(x1,x2), min(y1,y2), abs(x2-x1)+1, abs(y2-y1)+1)