import pygame


class Projectile:

    def __init__(self, x, y, direction):

        self.rect = pygame.Rect(x, y, 20, 10)

        self.speed = 10 * direction

    def update(self):

        self.rect.x += self.speed

    def draw(self, screen):

        pygame.draw.rect(screen, (255, 255, 0), self.rect)

    def off_screen(self):

        return self.rect.x < 0 or self.rect.x > 1000