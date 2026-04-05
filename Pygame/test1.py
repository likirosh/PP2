import pygame

pygame.init()

screen = pygame.display.set_mode((800, 480))

COLOR_RED  = (255, 0, 0)   # RGB: each component 0–255 (8 bits)
COLOR_BLUE = (0, 0, 255)

running = True
is_red = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                is_red = not is_red   # toggle True ↔ False

    if is_red:
        screen.fill(COLOR_RED)
    else:
        screen.fill(COLOR_BLUE)

    pygame.display.flip()  # push the frame to the screen

pygame.quit()