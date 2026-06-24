import pygame
import sys

pygame.init()

# ==========================
# CONFIGURAÇÕES
# ==========================

LARGURA = 1000
ALTURA = 600

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Guitar Guardian")

clock = pygame.time.Clock()

BRANCO = (255, 255, 255)
PRETO = (20, 20, 20)
AZUL = (50, 120, 255)
VERDE = (50, 200, 50)

fonte = pygame.font.SysFont("arial", 32)
fonte_titulo = pygame.font.SysFont("arial", 60, bold=True)

# ==========================
# ESTADOS
# ==========================

MENU = 0
JOGANDO = 1

estado = MENU

# ==========================
# JOGADOR
# ==========================

player = pygame.Rect(100, 450, 50, 80)

velocidade = 6

vel_y = 0
gravidade = 0.8
pulando = False

chao = 530

# ==========================
# LOOP PRINCIPAL
# ==========================

while True:

    clock.tick(60)

    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if estado == MENU:

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    estado = JOGANDO

        elif estado == JOGANDO:

            if evento.type == pygame.KEYDOWN:

                if evento.key == pygame.K_SPACE and not pulando:
                    vel_y = -16
                    pulando = True

    # ==========================
    # MENU
    # ==========================

    if estado == MENU:

        tela.fill((15, 15, 40))

        titulo = fonte_titulo.render(
            "GUITAR GUARDIAN",
            True,
            BRANCO
        )

        tela.blit(titulo, (250, 80))

        controles = [
            "CONTROLES",
            "",
            "A - ESQUERDA",
            "D - DIREITA",
            "SPACE - PULAR",
            "CTRL - TOCAR GUITARRA",
            "",
            "ENTER - INICIAR"
        ]

        y = 200

        for texto in controles:
            linha = fonte.render(texto, True, BRANCO)
            tela.blit(linha, (350, y))
            y += 40

    # ==========================
    # JOGO
    # ==========================

    elif estado == JOGANDO:

        teclas = pygame.key.get_pressed()

        if teclas[pygame.K_a]:
            player.x -= velocidade

        if teclas[pygame.K_d]:
            player.x += velocidade

        # gravidade
        vel_y += gravidade
        player.y += vel_y

        # chão
        if player.bottom >= chao:
            player.bottom = chao
            vel_y = 0
            pulando = False

        tela.fill((120, 200, 255))

        pygame.draw.rect(
            tela,
            VERDE,
            (0, chao, LARGURA, ALTURA - chao)
        )

        pygame.draw.rect(
            tela,
            AZUL,
            player
        )

        info = fonte.render(
            "Greg Guitar Guardian",
            True,
            PRETO
        )

        tela.blit(info, (20, 20))

    pygame.display.flip()