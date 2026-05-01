import pygame
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
HUD_HEIGHT = 50

screen = pygame.display.set_mode((WIDTH, HEIGHT))
base_layer = pygame.Surface((WIDTH, HEIGHT - HUD_HEIGHT))

pygame.display.set_caption("Drawing Tool - Shapes")
clock = pygame.time.Clock()

font = pygame.font.SysFont("Segoe UI", 20)

LMBpressed = False
THICKNESS = 3

startX = startY = 0
currX = currY = 0

mode = "rect"

BG_COLOR = (25, 25, 25)
HUD_COLOR = (40, 40, 40)

base_layer.fill(BG_COLOR)


def calculate_rect(x1, y1, x2, y2):
    return pygame.Rect(min(x1, x2), min(y1, y2), abs(x1 - x2), abs(y1 - y2))


def draw_square(surface, x1, y1, x2, y2):
    size = min(abs(x2 - x1), abs(y2 - y1))
    rect = pygame.Rect(x1, y1, size if x2 > x1 else -size, size if y2 > y1 else -size)
    rect = calculate_rect(rect.x, rect.y, rect.x + rect.w, rect.y + rect.h)
    pygame.draw.rect(surface, "red", rect, THICKNESS)


def draw_right_triangle(surface, x1, y1, x2, y2):
    points = [(x1, y1), (x2, y1), (x1, y2)]
    pygame.draw.polygon(surface, "red", points, THICKNESS)


def draw_equilateral_triangle(surface, x1, y1, x2, y2):
    side = abs(x2 - x1)
    height = side * math.sqrt(3) / 2

    if y2 < y1:
        height = -height

    p1 = (x1, y1)
    p2 = (x1 + side, y1)
    p3 = (x1 + side / 2, y1 - height)

    pygame.draw.polygon(surface, "red", [p1, p2, p3], THICKNESS)


def draw_rhombus(surface, x1, y1, x2, y2):
    cx = (x1 + x2) // 2
    cy = (y1 + y2) // 2

    points = [
        (cx, y1),
        (x2, cy),
        (cx, y2),
        (x1, cy)
    ]

    pygame.draw.polygon(surface, "red", points, THICKNESS)


def draw_shape(surface):
    if mode == "rect":
        pygame.draw.rect(surface, "red",
                         calculate_rect(startX, startY, currX, currY), THICKNESS)

    elif mode == "square":
        draw_square(surface, startX, startY, currX, currY)

    elif mode == "rtriangle":
        draw_right_triangle(surface, startX, startY, currX, currY)

    elif mode == "etriangle":
        draw_equilateral_triangle(surface, startX, startY, currX, currY)

    elif mode == "rhombus":
        draw_rhombus(surface, startX, startY, currX, currY)


def draw_ui():
    pygame.draw.rect(screen, HUD_COLOR, (0, 0, WIDTH, HUD_HEIGHT))

    text = f"Mode: {mode.upper()} | 1-Rect 2-Square 3-RightTri 4-EquiTri 5-Rhombus | +/- Thickness | C-Clear"
    surf = font.render(text, True, (230, 230, 230))
    screen.blit(surf, (10, 15))


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if event.pos[1] > HUD_HEIGHT:
                LMBpressed = True
                startX, startY = event.pos[0], event.pos[1] - HUD_HEIGHT

        if event.type == pygame.MOUSEMOTION:
            if LMBpressed:
                currX, currY = event.pos[0], event.pos[1] - HUD_HEIGHT

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if LMBpressed:
                LMBpressed = False
                currX, currY = event.pos[0], event.pos[1] - HUD_HEIGHT
                draw_shape(base_layer)  # сохраняем

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                mode = "rect"
            if event.key == pygame.K_2:
                mode = "square"
            if event.key == pygame.K_3:
                mode = "rtriangle"
            if event.key == pygame.K_4:
                mode = "etriangle"
            if event.key == pygame.K_5:
                mode = "rhombus"

            if event.key == pygame.K_EQUALS:
                THICKNESS += 1
            if event.key == pygame.K_MINUS:
                THICKNESS = max(1, THICKNESS - 1)

            if event.key == pygame.K_c:
                base_layer.fill(BG_COLOR)

    # --- РЕНДЕР (самое важное место) ---

    # 1. базовый слой (всегда)
    screen.blit(base_layer, (0, HUD_HEIGHT))

    # 2. превью (если рисуем)
    if LMBpressed:
        temp_surface = base_layer.copy()
        draw_shape(temp_surface)
        screen.blit(temp_surface, (0, HUD_HEIGHT))

    # 3. UI
    draw_ui()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()