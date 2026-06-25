import pygame
from assets import Assets

class Enemy:

    def __init__(self, x, y):
        self.image = Assets.image("noise_monster.png")

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

        screen.blit(self.image, self.rect)