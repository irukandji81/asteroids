# shot.py
import pygame
from circleshape import CircleShape
from constants import SHOT_RADIUS, SCREEN_WIDTH, SCREEN_HEIGHT

class Shot(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, SHOT_RADIUS)

    def draw(self, screen):
        pygame.draw.circle(screen, "white", (int(self.position.x), int(self.position.y)), self.radius, 2)

    def update(self, dt):
        self.position += self.velocity * dt

        # Remove the shot if it goes off-screen
        if (self.position.x < -self.radius or self.position.x > SCREEN_WIDTH + self.radius or
                self.position.y < -self.radius or self.position.y > SCREEN_HEIGHT + self.radius):
            self.kill()
