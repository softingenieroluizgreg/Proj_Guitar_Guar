import pygame
import sys

from player import Player
from enemy import Enemy
from projectile import Projectile

pygame.init()

WIDTH = 1000
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Guitar Guardian")

clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
GREEN = (50, 180, 50)

font = pygame.font.SysFont("arial", 30)
title_font = pygame.font.SysFont("arial", 60, bold=True)

MENU = 0
PLAYING = 1
WIN = 2
GAME_OVER = 3

state = MENU

floor_y = 530

player = Player()

enemies = [
    Enemy(500, 460),
    Enemy(800, 460)
]

projectiles = []

notes_collected = 0
target_notes = 10

damage_cooldown = 0

running = True

while running:

    clock.tick(60)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if state == MENU:

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RETURN:
                    state = PLAYING

        elif state == PLAYING:

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE:
                    player.jump()

                if event.key == pygame.K_LCTRL:

                    projectile = Projectile(
                        player.rect.centerx,
                        player.rect.centery,
                        player.direction
                    )

                    projectiles.append(projectile)

    # MENU

    if state == MENU:

        screen.fill((20, 20, 60))

        title = title_font.render(
            "GUITAR GUARDIAN",
            True,
            WHITE
        )

        screen.blit(title, (220, 80))

        controls = [
            "CONTROLES",
            "",
            "A - ESQUERDA",
            "D - DIREITA",
            "SPACE - PULAR",
            "CTRL - TOCAR GUITARRA",
            "",
            "ENTER - INICIAR"
        ]

        y = 220

        for line in controls:

            text = font.render(line, True, WHITE)

            screen.blit(text, (340, y))

            y += 35

    elif state == PLAYING:

        keys = pygame.key.get_pressed()

        player.move(keys)
        player.update(floor_y)

        screen.fill((120, 200, 255))

        pygame.draw.rect(
            screen,
            GREEN,
            (0, floor_y, WIDTH, HEIGHT - floor_y)
        )

        # inimigos

        for enemy in enemies:
            enemy.update()

        # projéteis

        for projectile in projectiles[:]:

            projectile.update()

            if projectile.off_screen():
                projectiles.remove(projectile)
                continue

            for enemy in enemies[:]:

                if projectile.rect.colliderect(enemy.rect):

                    if projectile in projectiles:
                        projectiles.remove(projectile)

                    if enemy in enemies:
                        enemies.remove(enemy)

                    notes_collected += 1
                    break

        # dano

        if damage_cooldown > 0:
            damage_cooldown -= 1

        for enemy in enemies:

            if player.rect.colliderect(enemy.rect):

                if damage_cooldown == 0:

                    player.life -= 20
                    damage_cooldown = 60

        # vitória

        if notes_collected >= target_notes:
            state = WIN

        # derrota

        if player.life <= 0:
            state = GAME_OVER

        player.draw(screen)

        for enemy in enemies:
            enemy.draw(screen)

        for projectile in projectiles:
            projectile.draw(screen)

        life_text = font.render(
            f"Vida: {player.life}",
            True,
            BLACK
        )

        score_text = font.render(
            f"Notas da Harmonia: {notes_collected}/{target_notes}",
            True,
            BLACK
        )

        screen.blit(life_text, (20, 20))
        screen.blit(score_text, (20, 60))

    elif state == WIN:

        screen.fill((20, 120, 20))

        text = title_font.render(
            "VOCE VENCEU!",
            True,
            WHITE
        )

        screen.blit(text, (250, 250))

    elif state == GAME_OVER:

        screen.fill((120, 20, 20))

        text = title_font.render(
            "GAME OVER",
            True,
            WHITE
        )

        screen.blit(text, (280, 250))

    pygame.display.flip()

pygame.quit()
sys.exit()