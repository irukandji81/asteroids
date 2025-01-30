# asteroid.py
import pygame
import random
from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.points = self.generate_points()
        self.rotation_speed = random.uniform(-0.5, 0.5)  # Adjust this range for desired rotation speed
        self.angle = 0

    def generate_points(self):
        points = []
        angle_step = 360 // 12  # Adjust this value for more or fewer points
        for angle in range(0, 360, angle_step):
            offset = random.uniform(0.8, 1.2)  # Adjust this range for lumpiness
            point_x = self.radius * offset * pygame.math.Vector2(1, 0).rotate(angle).x
            point_y = self.radius * offset * pygame.math.Vector2(1, 0).rotate(angle).y
            points.append((point_x, point_y))
        return points

    def draw(self, screen):
        rotated_points = [pygame.math.Vector2(p).rotate(self.angle) + self.position for p in self.points]
        pygame.draw.polygon(screen, "gray", rotated_points)  # Fill with a solid color

    def update(self, dt):
        self.position += self.velocity * dt
        self.wrap_around_screen()
        self.angle += self.rotation_speed

    def split(self):
        self.kill()

        if self.radius <= ASTEROID_MIN_RADIUS:
            return

        random_angle = random.uniform(20, 50)
        new_radius = self.radius - ASTEROID_MIN_RADIUS

        velocity1 = self.velocity.rotate(random_angle) * 1.2
        velocity2 = self.velocity.rotate(-random_angle) * 1.2

        asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid1.velocity = velocity1

        asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid2.velocity = velocity2
