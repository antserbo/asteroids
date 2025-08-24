from circleshape import CircleShape
from constants import *
import pygame
from shot import Shot


class Player(CircleShape):
    def __init__(self, x, y, radius=PLAYER_RADIUS):
        super().__init__(x, y, radius)
        self.rotation = 180.0
        self.shoot_timer = 0
        self.velocity = pygame.Vector2(0.0, 0.0)

    def triangle(self):
        forward = pygame.Vector2(0.0, 1.0).rotate(self.rotation)
        right = pygame.Vector2(0.0, 1.0).rotate(self.rotation + 90.0) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def forward(self) -> pygame.Vector2:
        return pygame.Vector2(0.0, 1.0).rotate(self.rotation)

    def apply_drag(self, dt: float):
        factor = PLAYER_DRAG ** dt
        self.velocity *= factor

    def accelerate(self, dt: float, sign: float = 1.0):
        self.velocity += self.forward() * (PLAYER_THRUST * sign * dt)
        speed = self.velocity.length()
        if speed > PLAYER_MAX_SPEED:
            self.velocity.scale_to_length(PLAYER_MAX_SPEED)

    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), 2)

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def shoot(self):
        if self.shoot_timer > 0:
            return
        self.shoot_timer = PLAYER_SHOOT_COOLDOWN
        shot = Shot(self.position.x, self.position.y)
        shot.velocity = pygame.Vector2(0.0, 1.0).rotate(self.rotation) * PLAYER_SHOT_SPEED

    def update(self, dt):
        self.shoot_timer -= dt
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.accelerate(dt, +1.0)
        if keys[pygame.K_s]:
            self.accelerate(dt, -0.6)

        self.apply_drag(dt)
        self.position += self.velocity * dt

        self.position.x %= SCREEN_WIDTH
        self.position.y %= SCREEN_HEIGHT

        if keys[pygame.K_SPACE]:
            self.shoot()
