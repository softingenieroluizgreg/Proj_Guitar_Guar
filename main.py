import pygame
import sys

from assets import Assets
from player import Player
from enemy import Enemy
from projectile import Projectile

pygame.init()
pygame.mixer.init()

# ==================================================
# CONFIGURAÇÕES
# ==================================================

WIDTH = 1000
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Guitar Guardian")

clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (50, 180, 50)

font = pygame.font.SysFont("arial", 28)
title_font = pygame.font.SysFont("arial", 60, bold=True)

# ==================================================
# ASSETS
# ==================================================

background = Assets.image("background_city.png")

shoot_sound = Assets.sound("guitar_shot.wav")
hit_sound = Assets.sound("hit.wav")
enemy_sound = Assets.sound("enemy_defeated.wav")

pygame.mixer.music.load(
    Assets.music("stage_theme.mp3")
)

pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# ==================================================
# ESTADOS
# ==================================================

MENU = 0
PLAYING = 1
WIN = 2
GAME_OVER = 3

state = MENU

# ==================================================
# JOGADOR
# ==================================================

floor_y = 530

player = Player()

# ==================================================
# INIMIGOS
# ==================================================

enemies = [
    Enemy(500, 460),
    Enemy(750, 460),
    Enemy(900, 460)
]

# ==================================================
# PROJÉTEIS
# ==================================================

projectiles = []

# ==================================================
# JOGO
# ==================================================

score = 0
target_score = 10

damage_cooldown = 0

# ==================================================
# LOOP PRINCIPAL
# ==================================================

running = True

while running:

    clock.tick(60)

    # ==============================================
    # EVENTOS
    # ==============================================

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

                    shoot_sound.play()

    # ==============================================
    # MENU
    # ==============================================

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
            "A - MOVER PARA ESQUERDA",
            "D - MOVER PARA DIREITA",
            "SPACE - PULAR",
            "CTRL - TOCAR GUITARRA",
            "",
            "ENTER - INICIAR"
        ]

        y = 220

        for line in controls:
            text = font.render(line, True, WHITE)

            screen.blit(text, (280, y))

            y += 35

    # ==============================================
    # JOGO
    # ==============================================

    elif state == PLAYING:


        keys = pygame.key.get_pressed()

        player.move(keys)
        player.update(floor_y)

        screen.blit(background, (0, 0))

        pygame.draw.rect(
            screen,
            GREEN,
            (0, floor_y, WIDTH, HEIGHT - floor_y)
        )
        player.draw(screen)
        

        # ------------------------------------------
        # Atualiza inimigos
        # ------------------------------------------

        for enemy in enemies:
            enemy.update()

        # ------------------------------------------
        # Atualiza projéteis
        # ------------------------------------------

        for projectile in projectiles[:]:

            projectile.update()

            if projectile.off_screen():
                projectiles.remove(projectile)
                continue

            for enemy in enemies[:]:

                if projectile.rect.colliderect(enemy.rect):

                    enemy_sound.play()

                    if projectile in projectiles:
                        projectiles.remove(projectile)

                    if enemy in enemies:
                        enemies.remove(enemy)

                    score += 1
                    break

        # ------------------------------------------
        # Dano ao jogador
        # ------------------------------------------

        if damage_cooldown > 0:
            damage_cooldown -= 1

        for enemy in enemies:

            if player.rect.colliderect(enemy.rect):

                if damage_cooldown == 0:
                    player.life -= 20

                    hit_sound.play()

                    damage_cooldown = 60

        # ------------------------------------------
        # Vitória
        # ------------------------------------------

        if score >= target_score:
            state = WIN

        # ------------------------------------------
        # Derrota
        # ------------------------------------------

        if player.life <= 0:
            state = GAME_OVER

        # ------------------------------------------
        # Desenha jogador

        # ------------------------------------------



        player.draw(screen)

        # ------------------------------------------
        # Desenha inimigos
        # ------------------------------------------

        for enemy in enemies:
            enemy.draw(screen)

        # ------------------------------------------
        # Desenha projéteis
        # ------------------------------------------

        for projectile in projectiles:
            projectile.draw(screen)

        # ------------------------------------------
        # HUD
        # ------------------------------------------

        life_text = font.render(
            f"Vida: {player.life}",
            True,
            BLACK
        )

        score_text = font.render(
            f"Harmonia: {score}/{target_score}",
            True,
            BLACK
        )

        screen.blit(life_text, (20, 20))
        screen.blit(score_text, (20, 55))

        # Barra de vida

        pygame.draw.rect(
            screen,
            (180, 0, 0),
            (20, 90, 200, 20)
        )

        pygame.draw.rect(
            screen,
            (0, 200, 0),
            (20, 90, player.life * 2, 20)
        )

    # ==============================================
    # VITÓRIA
    # ==============================================

    elif state == WIN:

        screen.fill((20, 120, 20))

        text = title_font.render(
            "VOCE VENCEU!",
            True,
            WHITE
        )

        screen.blit(text, (230, 250))

    # ==============================================
    # GAME OVER
    # ==============================================

    elif state == GAME_OVER:

        screen.fill((120, 20, 20))

        text = title_font.render(
            "GAME OVER",
            True,
            WHITE
        )

        screen.blit(text, (260, 250))

    pygame.display.flip()

pygame.quit()
sys.exit()
