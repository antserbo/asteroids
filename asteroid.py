import pygame
import random

from circleshape import CircleShape
from constants import *


class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(screen, "pink", self.position, self.radius, 2)

    def update(self, dt):
        self.position += self.velocity * dt * 0.5

    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        else:
            random_angle = random.uniform(20, 50)
            first_vector = self.velocity.rotate(random_angle)
            second_vector = self.velocity.rotate(-random_angle)

            new_radius = self.radius - ASTEROID_MIN_RADIUS
            first_asteroid = Asteroid(self.position, self.position, new_radius)
            second_asteroid = Asteroid(self.position, self.position, new_radius)

            first_asteroid.velocity = first_vector * 1.2
            second_asteroid.velocity = second_vector * 1.2
