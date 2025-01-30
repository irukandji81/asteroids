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

class BombPowerUp(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS / 2)
        self.color = (255, 0, 0)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.position.x), int(self.position.y)), self.radius)

    def update(self, dt):
        pass  # Power-ups remain stationary

class TripleShotPowerUp(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS / 2)
        self.color = (255, 215, 0)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.position.x), int(self.position.y)), self.radius)

    def update(self, dt):
        # Even if stationary, we'll implement update to use dt
        self.position += pygame.Vector2(0, 0)
