import pygame
from assets import Assets


class Player:

    def __init__(self):

        self.image = Assets.image("hero_idle.png")
        self.image = pygame.transform.scale(self.image, (96, 96))

        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 450

        self.speed = 6

        self.vel_y = 0
        self.gravity = 0.8

        self.jumping = False

        self.life = 100

        # 1 = direita / -1 = esquerda
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

        if self.direction == -1:
            sprite = pygame.transform.flip(
                self.image,
                True,
                False
            )
        else:
            sprite = self.image

        screen.blit(sprite, self.rect)