import pygame


class Ball:
    def __init__(self, screen_width, screen_height):
        self.radius = 25
        self.color = (220, 50, 50)  # Red
        self.speed = 20

        self.screen_width = screen_width
        self.screen_height = screen_height

        self.x = screen_width // 2
        self.y = screen_height // 2

    def move(self, direction):
        """Move the ball in the given direction. Ignores input that would go off-screen."""
        new_x, new_y = self.x, self.y

        if direction == "UP":
            new_y -= self.speed
        elif direction == "DOWN":
            new_y += self.speed
        elif direction == "LEFT":
            new_x -= self.speed
        elif direction == "RIGHT":
            new_x += self.speed

        if self._is_within_bounds(new_x, new_y):
            self.x = new_x
            self.y = new_y

    def _is_within_bounds(self, x, y):
        """Check if position keeps the ball fully within the screen."""
        return (
            self.radius <= x <= self.screen_width - self.radius
            and self.radius <= y <= self.screen_height - self.radius
        )

    def draw(self, surface):
        """Draw the ball on the given surface."""
        pygame.draw.circle(surface, (180, 30, 30), (self.x + 3, self.y + 3), self.radius)
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)
        pygame.draw.circle(surface, (255, 120, 120), (self.x - 8, self.y - 8), 7)