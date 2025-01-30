import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

def main():
    # Initialize pygame
    pygame.init()
    print("Starting asteroids!")

    # Set up the game window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    # Create a pygame.time.Clock object and dt variable
    clock = pygame.time.Clock()
    dt = 0

    # Create groups
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    # Set the static containers fields
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    Shot.containers = (shots, updatable, drawable)

    # Instantiate a Player object and add to groups
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    updatable.add(player)
    drawable.add(player)

    # Create an AsteroidField object
    asteroid_field = AsteroidField()
    updatable.add(asteroid_field)

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
                print("Game over!")
                return

        # Check for collisions between shots and asteroids
        for shot in shots:
            for asteroid in asteroids:
                if shot.collides_with(asteroid):
                    shot.kill()
                    asteroid.split()

        # Fill the screen with black color
        screen.fill((0, 0, 0))

        # Draw all drawable objects
        for drawable_object in drawable:
            drawable_object.draw(screen)

        # Refresh the screen
        pygame.display.flip()

        # Cap the frame rate at 60 FPS and get delta time
        dt = clock.tick(60) / 1000

if __name__ == "__main__":
    main()
