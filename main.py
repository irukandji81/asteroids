import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from explosion import Explosion
from powerup import PowerUp
import random

def main():
    # Initialize pygame
    pygame.init()
    print("Starting asteroids!")

    # Set up the game window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    # Load the background image
    background = pygame.image.load('starry_dark_background.png')
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # Create a pygame.time.Clock object and dt variable
    clock = pygame.time.Clock()
    dt = 0

    # Create groups
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    powerups = pygame.sprite.Group()

    # Set the static containers fields
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    Shot.containers = (shots, updatable, drawable)
    Explosion.containers = (updatable, drawable)
    PowerUp.containers = (powerups, updatable, drawable)

    # Instantiate a Player object and add to groups
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    updatable.add(player)
    drawable.add(player)

    # Create an AsteroidField object
    asteroid_field = AsteroidField()
    updatable.add(asteroid_field)

    # Create a score variable
    score = 0

    # Create a lives variable
    lives = 3

    # Create a font for rendering the score and lives
    font = pygame.font.Font(None, 36)

    def respawn_player():
        player.position = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        player.velocity = pygame.Vector2(0, 0)
        player.rotation = 0
        player.acceleration = pygame.Vector2(0, 0)  # Reset acceleration
        player.has_shield = False  # Reset shield

        # Clear asteroids in the central part of the screen
        safe_zone_radius = 150  # Increased the safe zone radius
        for asteroid in asteroids:
            if player.position.distance_to(asteroid.position) < safe_zone_radius:
                asteroid.kill()

    # Create the game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        # Update all updatable objects
        updatable.update(dt)

        # Check for collisions between player and asteroids
        for asteroid in asteroids:
            if player.collides_with(asteroid):
                if player.has_shield:
                    player.has_shield = False  # Use up the shield
                    asteroid.kill()  # Destroy the asteroid
                else:
                    lives -= 1
                    if lives > 0:
                        print(f"Lives left: {lives}")
                        respawn_player()
                    else:
                        print("Game over!")
                        return

        # Check for collisions between shots and asteroids
        for shot in shots:
            for asteroid in asteroids:
                if shot.collides_with(asteroid):
                    shot.kill()
                    asteroid.split()
                    score += 10  # Increase score when an asteroid is destroyed
                    explosion = Explosion(asteroid.position.x, asteroid.position.y)
                    updatable.add(explosion)
                    drawable.add(explosion)
                    if random.random() < 0.1:  # 10% chance to spawn a power-up
                        powerup = PowerUp(asteroid.position.x, asteroid.position.y)
                        updatable.add(powerup)
                        drawable.add(powerup)

        # Check for collisions between player and power-ups
        for powerup in powerups:
            if player.collides_with(powerup):
                player.apply_powerup(powerup)
                powerup.kill()

        # Draw the background image
        screen.blit(background, (0, 0))

        # Draw all drawable objects
        for drawable_object in drawable:
            drawable_object.draw(screen)

        # Render the score
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        # Render the lives
        lives_text = font.render(f"Lives: {lives}", True, (255, 255, 255))
        screen.blit(lives_text, (SCREEN_WIDTH - 110, 10))

        # Render active power-ups
        powerups_text = font.render("Power-ups: " + ", ".join(player.get_active_powerups()), True, (255, 255, 255))
        screen.blit(powerups_text, (10, 50))

        # Refresh the screen
        pygame.display.flip()

        # Cap the frame rate at 60 FPS and get delta time
        dt = clock.tick(60) / 1000

if __name__ == "__main__":
    main()
