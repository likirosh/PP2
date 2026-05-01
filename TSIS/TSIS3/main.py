import pygame
import sys
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

from persistence import load_settings, save_settings, save_score
from racer       import run_game, load_assets, WIDTH, HEIGHT
from ui          import (main_menu, settings_screen,
                          leaderboard_screen, game_over_screen,
                          username_screen)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Racer  ·  TSIS3")
    clock    = pygame.time.Clock()

    load_assets()
    bg_img = pygame.image.load("assets/AnimatedStreet.png").convert()

    settings = load_settings()
    username = None  

    while True:
        action = main_menu(screen, clock, bg_img)

        if action == "quit":
            save_settings(settings)
            pygame.quit(); sys.exit()

        elif action == "leaderboard":
            leaderboard_screen(screen, clock, bg_img)

        elif action == "settings":
            settings = settings_screen(screen, clock, settings, bg_img)

        elif action == "play":
            if username is None:
                username = username_screen(screen, clock, bg_img)

            while True:  
                score, distance, coins = run_game(screen, clock, settings)
                save_score(username, score, distance)

                result = game_over_screen(
                    screen, clock, score, distance, coins, bg_img)

                if result == "retry":
                    continue
                else:
                    break  

if __name__ == "__main__":
    main()