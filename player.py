# player.py
import pygame
from circleshape import CircleShape
from constants import PLAYER_RADIUS, PLAYER_TURN_SPEED, PLAYER_ACCELERATION, PLAYER_SHOOT_SPEED, PLAYER_SHOOT_COOLDOWN
from shot import Shot  # Make sure this import statement is included

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shoot_timer = 0
        self.acceleration = pygame.Vector2(0, 0)

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), 2)

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def accelerate(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.acceleration = forward * PLAYER_ACCELERATION * dt

    def brake(self, dt):
        self.velocity *= 0.9  # Apply a braking factor to reduce velocity

    def shoot(self):
        if self.shoot_timer > 0:
            return
        self.shoot_timer = PLAYER_SHOOT_COOLDOWN
        shot = Shot(self.position.x, self.position.y)
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        shot.velocity = forward * PLAYER_SHOOT_SPEED

    def update(self, dt):
        self.shoot_timer = max(0, self.shoot_timer - dt)

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.accelerate(dt)
        else:
            self.acceleration = pygame.Vector2(0, 0)  # Stop accelerating but keep current velocity

        if keys[pygame.K_LSHIFT]:
            self.brake(dt)

        self.velocity += self.acceleration * dt
        self.position += self.velocity * dt

        self.wrap_around_screen()

        if keys[pygame.K_SPACE]:
            self.shoot()
