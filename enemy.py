import pygame


class Enemy:

    def __init__(self, x, y):

        self.rect = pygame.Rect(x, y, 50, 70)

        self.speed = 2

        self.direction = 1

    def update(self):

        self.rect.x += self.speed * self.direction

        if self.rect.left < 0:
            self.direction = 1

        if self.rect.right > 1000:
            self.direction = -1

    def draw(self, screen):

        pygame.draw.rect(screen, (220, 50, 50), self.rect)