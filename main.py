# this allows us to use code from
# the open-source pygame library
# throughout this file
import pygame

# Import everything from constants.py
from constants import *

def main():
    # Initialize pygame
    pygame.init()
    print("Starting asteroids!")

    # Set up the game window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    # Create the game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        # Fill the screen with black color
        screen.fill((0, 0, 0))

        # Refresh the screen
        pygame.display.flip()

if __name__ == "__main__":
    main()
