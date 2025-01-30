# explosion.py
import pygame

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.frames = []
        self.load_images()
        self.index = 0
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect(center=(x, y))
        self.animation_speed = 0.1
        self.timer = 0

    def load_images(self):
        for i in range(9):
            frame = pygame.Surface((50, 50), pygame.SRCALPHA)
            frame.fill((0, 0, 0, 0))
            pygame.draw.circle(frame, (255, 0, 0), (25, 25), 25 - i*2)
            self.frames.append(frame)

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.animation_speed:
            self.timer = 0
            self.index += 1
            if self.index >= len(self.frames):
                self.kill()
            else:
                self.image = self.frames[self.index]

    def draw(self, screen):
        screen.blit(self.image, self.rect)
