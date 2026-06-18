# MÄNG - PING PONG

import pygame
import sys

pygame.init()

# EKRAANI SEADED
screenx, screeny = 640, 480
screen = pygame.display.set_mode((screenx, screeny))
pygame.display.set_caption("Ping Pong")
clock = pygame.time.Clock()
roosa = (255, 102, 204)

# TEKSTI FONT
font = pygame.font.SysFont("Arial", 30)

# PALL
ball = pygame.Rect(10, 10, 20, 20)
ballImage = pygame.image.load("ball.png")
ballImage = pygame.transform.scale(ballImage, (20, 20))
speedx, speedy = 4, 5

# ALUS
alus = pygame.Rect([100, screeny / 1.5], (120, 20))
alusImage = pygame.image.load("../../tööd/pad.png")
alusImage = pygame.transform.scale(alusImage, (120, 20))
alusSpeed = 3  # Aluse kiirus

# SKOOR
skoor = 0
gameover = False

# ALUSE SUUND (paremale = 1, vasakule = -1)
alusDirection = 1

# MÄNGUTSÜKKEL
while not gameover:

    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # -------------------------
    # PALLI LIIKUMINE
    # -------------------------
    ball.x += speedx
    ball.y += speedy

    # Põrge vasak/parem
    if ball.left <= 0 or ball.right >= screenx:
        speedx = -speedx

    # Põrge ülevalt
    if ball.top <= 0:
        speedy = -speedy

    # -------------------------
    # ALUSE LIIKUMINE (vasak-parem automaatne)
    # -------------------------
    alus.x += alusDirection * alusSpeed

    # Kui alus jõuab seina äärde → vaheta suunda
    if alus.left <= 0:
        alus.left = 0
        alusDirection = 1

    if alus.right >= screenx:
        alus.right = screenx
        alusDirection = -1

    # -------------------------
    # KOKKUPÕRGE ALUSEGA
    # -------------------------
    if ball.colliderect(alus):

        # Põrge ainult siis, kui pall liigub alla (speedy > 0)
        if speedy > 0:
            ball.bottom = alus.top
            speedy = -speedy
            skoor += 1  # +1 punkt
        else:
            # Kui pall tuleb alt üles (harva), lükka ta alla
            ball.top = alus.bottom
            speedy = -speedy

    # -------------------------
    # PALL PUUDUTAB ALUMIST ÄÄRT
    # -------------------------
    if ball.bottom >= screeny:
        skoor -= 1  # -1 punkt
        speedy = -speedy

    # -------------------------
    # EKRAANI JOONISTAMINE
    # -------------------------
    screen.fill(roosa)
    screen.blit(alusImage, alus)
    screen.blit(ballImage, ball)

    # SKOORI KUVAMINE
    tekst = font.render("Skoor: " + str(skoor), True, (255, 255, 255))
    screen.blit(tekst, (10, 10))

    pygame.display.flip()

pygame.quit()
sys.exit()
