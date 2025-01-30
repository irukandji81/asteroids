# powerup.py
import pygame
from circleshape import CircleShape
from constants import PLAYER_RADIUS

class PowerUp(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS / 2)
        self.color = (0, 255, 255)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.position.x), int(self.position.y)), self.radius)
    
    def update(self, dt):
        pass  # Power-ups remain stationary
