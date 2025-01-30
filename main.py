# main.py
import pygame
from constants import *
from player import Player

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

    # Instantiate a Player object
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    # Create the game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        # Fill the screen with black color
        screen.fill((0, 0, 0))

        # Update and draw the player
        player.update(dt)
        player.draw(screen)

        # Refresh the screen
        pygame.display.flip()

        # Cap the frame rate at 60 FPS and get delta time
        dt = clock.tick(60) / 1000

if __name__ == "__main__":
    main()
