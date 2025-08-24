import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Asteroids")
    game_clock = pygame.time.Clock()
    dt = 0

    font = pygame.font.SysFont('Arial', 40)

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = updatable
    Shot.containers = (shots, updatable, drawable)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()

    game_running_state = True

    while game_running_state:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        updatable.update(dt)

        for asteroid in asteroids:
            if asteroid.collides_with(player):
                print("Game over!")
                game_running_state = False

        for shot in shots:
            for asteroid in asteroids:
                if asteroid.collides_with(shot):
                    shot.kill()
                    asteroid.split()

        screen.fill("black")

        for obj in drawable:
            obj.draw(screen)

        '''
        -----------
        FPS COUNTER.
        -----------
        '''
        fps_text = font.render(f"{game_clock.get_fps():.0f} FPS", True, "yellow")
        screen.blit(fps_text, (8, 8))

        pygame.display.flip()
        dt = game_clock.tick(GAME_FPS) / 1000


if __name__ == "__main__":
    main()
