import pygame
import math


class ClockHand:
    """
    Represents one clock hand (an arm image that rotates around a pivot point).

    pivot_in_image: (x, y) pixel inside the CROPPED hand image that is the
                    rotation centre (where the arm meets Mickey's body).
    """

    def __init__(self, image_path, crop_rect, pivot_in_image, scale=1.0):
        """
        image_path    – path to the original PNG
        crop_rect     – (left, top, right, bottom) to crop the relevant arm
        pivot_in_image– (px, py) pivot point WITHIN the cropped image
        scale         – resize factor applied after cropping
        """
        raw = pygame.image.load(image_path).convert_alpha()

        x0, y0, x1, y1 = crop_rect
        cropped = raw.subsurface(pygame.Rect(x0, y0, x1 - x0, y1 - y0))

        w = int(cropped.get_width() * scale)
        h = int(cropped.get_height() * scale)
        self.image = pygame.transform.smoothscale(cropped, (w, h))

        self.pivot = (pivot_in_image[0] * scale,
                      pivot_in_image[1] * scale)

    def draw(self, surface, angle_deg, center):
        """
        Rotate the hand by angle_deg (clockwise from 12-o'clock = 0°)
        and blit it so that self.pivot lands exactly on `center`.

        pygame.transform.rotate rotates counter-clockwise, so we negate.
        """
        rotated = pygame.transform.rotate(self.image, -angle_deg)

        orig_w, orig_h = self.image.get_size()
        rot_w,  rot_h  = rotated.get_size()

        px, py = self.pivot
        dx = px - orig_w / 2
        dy = py - orig_h / 2

        rad = math.radians(angle_deg)
        rdx =  dx * math.cos(rad) + dy * math.sin(rad)
        rdy = -dx * math.sin(rad) + dy * math.cos(rad)

        pivot_rot_x = rot_w / 2 + rdx
        pivot_rot_y = rot_h / 2 + rdy

        blit_x = center[0] - pivot_rot_x
        blit_y = center[1] - pivot_rot_y

        surface.blit(rotated, (blit_x, blit_y))


def minutes_angle(minute: int, second: int) -> float:
    """Angle in degrees for the minute hand (0° = 12 o'clock, clockwise)."""
    return (minute + second / 60) * 6          


def seconds_angle(second: int) -> float:
    """Angle in degrees for the second hand."""
    return second * 6                     