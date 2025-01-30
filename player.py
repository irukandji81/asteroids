# player.py
import pygame
from circleshape import CircleShape
from constants import PLAYER_RADIUS, PLAYER_TURN_SPEED, PLAYER_ACCELERATION, PLAYER_SHOOT_SPEED, PLAYER_SHOOT_COOLDOWN
from shot import Shot
from powerup import PowerUp, BombPowerUp
from asteroid import Asteroid

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shoot_timer = 0
        self.acceleration = pygame.Vector2(0, 0)
        self.has_shield = False
        self.has_bomb = False

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        # Draw the triangle with a black border
        pygame.draw.polygon(screen, "black", self.triangle())
        # Draw the filled triangle
        pygame.draw.polygon(screen, "white", self.triangle())

        # Draw the shield if the player has it
        if self.has_shield:
            pygame.draw.circle(screen, (0, 255, 255), (int(self.position.x), int(self.position.y)), self.radius + 5, 2)

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

        if keys[pygame.K_e] and self.has_bomb:
            self.activate_bomb()

        self.velocity += self.acceleration * dt
        self.position += self.velocity * dt

        self.wrap_around_screen()

        if keys[pygame.K_SPACE]:
            self.shoot()

    def collides_with(self, other):
        distance = self.position.distance_to(other.position)
        return distance < (self.radius + other.radius)

    def apply_powerup(self, powerup):
        if isinstance(powerup, PowerUp):
            self.has_shield = True
        elif isinstance(powerup, BombPowerUp):
            self.has_bomb = True

    def activate_bomb(self):
        self.has_bomb = False
        for asteroid in list(self.groups()[0]):
            if isinstance(asteroid, Asteroid):
                asteroid.kill()

    def get_active_powerups(self):
        active_powerups = []
        if self.has_shield:
            active_powerups.append("Shield")
        if self.has_bomb:
            active_powerups.append("Bomb")
        return active_powerups