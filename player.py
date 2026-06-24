import pygame


class Player:

    def __init__(self):
        self.rect = pygame.Rect(100, 450, 50, 80)

        self.speed = 6

        self.vel_y = 0
        self.gravity = 0.8

        self.jumping = False

        self.life = 100

        self.direction = 1

    def move(self, keys):

        if keys[pygame.K_a]:
            self.rect.x -= self.speed
            self.direction = -1

        if keys[pygame.K_d]:
            self.rect.x += self.speed
            self.direction = 1

    def jump(self):

        if not self.jumping:
            self.vel_y = -16
            self.jumping = True

    def update(self, floor_y):

        self.vel_y += self.gravity
        self.rect.y += self.vel_y

        if self.rect.bottom >= floor_y:
            self.rect.bottom = floor_y
            self.vel_y = 0
            self.jumping = False

    def draw(self, screen):

        pygame.draw.rect(screen, (50, 120, 255), self.rect)