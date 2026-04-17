import pygame
import sys
import datetime
import os

from clock import ClockHand, minutes_angle, seconds_angle

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
CLOCK_IMG  = os.path.join(BASE_DIR, "mainclock.png")
LEFT_IMG   = os.path.join(BASE_DIR, "leftarm.png")   
RIGHT_IMG  = os.path.join(BASE_DIR, "rightarm.png")  

CLOCK_SCALE  = 0.55          
FPS          = 10            

LEFT_CROP    = (1, 255, 62, 515)
LEFT_PIVOT   = (30, 259)     

RIGHT_CROP   = (528, 384, 720, 538)
RIGHT_PIVOT  = (96, 142)


def main():
    pygame.init()

    clock_raw  = pygame.image.load(CLOCK_IMG).convert_alpha()
    cw = int(clock_raw.get_width()  * CLOCK_SCALE)
    ch = int(clock_raw.get_height() * CLOCK_SCALE)
    clock_face = pygame.transform.smoothscale(clock_raw, (cw, ch))

    screen = pygame.display.set_mode((cw, ch))
    pygame.display.set_caption("Mickey's Clock")

    arm_scale = CLOCK_SCALE * 1.1

    left_hand  = ClockHand(LEFT_IMG,  LEFT_CROP,  LEFT_PIVOT,  scale=arm_scale)
    right_hand = ClockHand(RIGHT_IMG, RIGHT_CROP, RIGHT_PIVOT, scale=arm_scale)

    cx = int(700 * CLOCK_SCALE)
    cy = int(490 * CLOCK_SCALE)
    centre = (cx, cy)

    tick = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        now     = datetime.datetime.now()
        minute  = now.minute
        second  = now.second

        min_ang = minutes_angle(minute, second)
        sec_ang = seconds_angle(second)

        screen.blit(clock_face, (0, 0))   

        right_hand.draw(screen, min_ang, centre)
        left_hand.draw(screen,  sec_ang, centre)

        pygame.display.flip()
        tick.tick(FPS)


if __name__ == "__main__":
    main()