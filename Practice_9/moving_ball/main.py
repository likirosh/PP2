import pygame
import sys
from ball import Ball

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
FPS = 60
BG_COLOR = (255, 255, 255)  # White
TITLE = "Moving Ball Game"

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()

    ball = Ball(SCREEN_WIDTH, SCREEN_HEIGHT)

    key_to_direction = {
        pygame.K_UP:    "UP",
        pygame.K_DOWN:  "DOWN",
        pygame.K_LEFT:  "LEFT",
        pygame.K_RIGHT: "RIGHT",
    }

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key in key_to_direction:
                    ball.move(key_to_direction[event.key])

        screen.fill(BG_COLOR)
        ball.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()