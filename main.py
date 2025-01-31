import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from explosion import Explosion
from powerup import PowerUp, BombPowerUp, TripleShotPowerUp
import random

def initialize_menu_asteroids(num_asteroids):
    menu_asteroids = pygame.sprite.Group()
    for _ in range(num_asteroids):
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(0, SCREEN_HEIGHT)
        asteroid = Asteroid(x, y, random.randint(20, 50))  # Random radius between 20 and 50
        asteroid.velocity = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)) * 0.5
        menu_asteroids.add(asteroid)
    return menu_asteroids

def start_menu(screen, background, menu_asteroids):
    font = pygame.font.Font(None, 74)
    title_text = font.render("Irukanjoids Game", True, (255, 255, 255))
    start_text = font.render("Press ENTER to Start", True, (255, 255, 255))
    quit_text = font.render("Press ESC to Quit", True, (255, 255, 255))

    clock = pygame.time.Clock()

    while True:
        screen.blit(background, (0, 0))
        
        # Update and draw menu asteroids
        for asteroid in menu_asteroids:
            asteroid.update(0.1)
            asteroid.draw(screen)
            
        screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, SCREEN_HEIGHT//4))
        screen.blit(start_text, (SCREEN_WIDTH//2 - start_text.get_width()//2, SCREEN_HEIGHT//2))
        screen.blit(quit_text, (SCREEN_WIDTH//2 - quit_text.get_width()//2, SCREEN_HEIGHT//1.5))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return True
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return False
        
        clock.tick(60)  # Limit to 60 FPS

def game_over_menu(screen, background, menu_asteroids, score):
    font = pygame.font.Font(None, 74)
    game_over_text = font.render("GAME OVER!", True, (255, 255, 255))
    final_score_text = font.render(f"Score: {score}",True, (255,255,255))
    retry_text = font.render("Press ENTER to Retry", True, (255, 255, 255))
    quit_text = font.render("Press ESC to Quit", True, (255, 255, 255))

    clock = pygame.time.Clock()

    while True:
        screen.blit(background, (0, 0))
        
        # Update and draw menu asteroids
        for asteroid in menu_asteroids:
            asteroid.update(0.1)
            asteroid.draw(screen)
            
        screen.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, SCREEN_HEIGHT//4))
        screen.blit(final_score_text, (SCREEN_WIDTH//2 - final_score_text.get_width()//2, SCREEN_HEIGHT//3))
        screen.blit(retry_text, (SCREEN_WIDTH//2 - retry_text.get_width()//2, SCREEN_HEIGHT//2))
        screen.blit(quit_text, (SCREEN_WIDTH//2 - quit_text.get_width()//2, SCREEN_HEIGHT//1.5))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return True
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return False

        clock.tick(60)  # Limit to 60 FPS

def main():
    # Initialize pygame
    pygame.init()
    print("Starting Irukanjoids!")

    # Set up the game window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    # Load the background image
    background = pygame.image.load('starry_dark_background.png')
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # Initialize asteroids for the menu
    menu_asteroids = initialize_menu_asteroids(10)  # 10 asteroids for the start menu

    if not start_menu(screen, background, menu_asteroids):
        return

    while True:
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
        BombPowerUp.containers = (powerups, updatable, drawable)
        TripleShotPowerUp.containers = (powerups, updatable, drawable)

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
            player.activate_shield()  # Activate shield on respawn

            # Clear asteroids in the central part of the screen
            safe_zone_radius = 150  # Increased the safe zone radius
            for asteroid in asteroids:
                if player.position.distance_to(asteroid.position) < safe_zone_radius:
                    asteroid.kill()

        def bomb_active():
            return any(isinstance(powerup, BombPowerUp) for powerup in powerups)

        def shield_active_count():
            return sum(1 for powerup in powerups if isinstance(powerup, PowerUp))
        
        def triple_shot_powerup_active_count(powerups):
            return sum(1 for powerup in powerups if isinstance(powerup, TripleShotPowerUp))

        # Create the game loop
        game_over = False
        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
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
                            game_over = True

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
                        powerup_chance = random.random()
                        if powerup_chance < 0.1 and shield_active_count() < 3:  # 10% chance to spawn a shield power-up
                            powerup = PowerUp(asteroid.position.x, asteroid.position.y)
                            updatable.add(powerup)
                            drawable.add(powerup)
                        elif powerup_chance < 0.1 and not player.has_bomb and not bomb_active():  # Additional 5% chance to spawn a bomb power-up
                            bomb_powerup = BombPowerUp(asteroid.position.x, asteroid.position.y)
                            updatable.add(bomb_powerup)
                            drawable.add(bomb_powerup)
                        elif powerup_chance < 0.1 and triple_shot_powerup_active_count(powerups) < 3:  # Additional 5% chance to spawn a triple-shot power-up
                            triple_shot_powerup = TripleShotPowerUp(asteroid.position.x, asteroid.position.y)
                            updatable.add(triple_shot_powerup)
                            drawable.add(triple_shot_powerup)

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

            # Render active power-ups and triple-shot timer
            active_powerups_text = "Power-ups: " + ", ".join(player.get_active_powerups())
            powerups_text = font.render(active_powerups_text, True, (255, 255, 255))
            screen.blit(powerups_text, (10, 50))

            # Refresh the screen
            pygame.display.flip()

            # Cap the frame rate at 60 FPS and get delta time
            dt = clock.tick(60) / 1000

        if not game_over_menu(screen, background, menu_asteroids, score):
            return

if __name__ == "__main__":
    main()
    