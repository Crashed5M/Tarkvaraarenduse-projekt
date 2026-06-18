import pygame

# -----------------------------------
# Seaded
# -----------------------------------
pygame.init()

LAIUS, KORGUS = 300, 300
EKRAAN = pygame.display.set_mode((LAIUS, KORGUS))
pygame.display.set_caption("Lumememm – Karl‑Eerik Pendonen")

# Värvid
VALGE = (255, 255, 255)
MUST = (0, 0, 0)
PRUUN = (70, 40, 20)
ORANZ = (255, 165, 0)
TAUST = (135, 206, 235)
HALL = (191, 205, 219)
KOLLANE = (255, 255, 0)

töötab = True


# -----------------------------------
# Funktsioonid
# -----------------------------------
def joonista_pilv(surface, x, y):
    pygame.draw.circle(surface, HALL, (x, y), 13)
    pygame.draw.circle(surface, HALL, (x + 20, y + 5), 15)
    pygame.draw.circle(surface, HALL, (x - 20, y + 5), 15)
    pygame.draw.circle(surface, HALL, (x, y + 12), 13)


def joonista_lumememm(surface):
    # Keha
    pygame.draw.circle(surface, VALGE, (150, 100), 30)
    pygame.draw.circle(surface, VALGE, (150, 160), 40)
    pygame.draw.circle(surface, VALGE, (150, 240), 50)

    # Silmad
    pygame.draw.circle(surface, MUST, (140, 95), 4)
    pygame.draw.circle(surface, MUST, (160, 95), 4)

    # Nina
    pygame.draw.polygon(surface, ORANZ, [(150, 115), (145, 100), (155, 100)])

    # Nööbid
    for offset in (145, 160, 175):
        pygame.draw.circle(surface, MUST, (150, offset), 3)

    # Käed
    pygame.draw.line(surface, PRUUN, (185, 150), (220, 145), 4)
    pygame.draw.line(surface, PRUUN, (115, 150), (80, 145), 4)

    # Hari
    pygame.draw.line(surface, PRUUN, (218, 200), (218, 125), 6)
    pygame.draw.line(surface, PRUUN, (218, 126), (218, 95), 4)
    pygame.draw.line(surface, PRUUN, (218, 126), (230, 95), 4)
    pygame.draw.line(surface, PRUUN, (218, 126), (206, 95), 4)

    # Müts
    pygame.draw.rect(surface, PRUUN, (120, 70, 60, 9))
    pygame.draw.rect(surface, PRUUN, (130, 35, 40, 40))


def joonista_päike(surface):
    pygame.draw.circle(surface, KOLLANE, (65, 50), 25)

    # Kiired
    pygame.draw.line(surface, KOLLANE, (65, 95), (65, 5), 2)
    pygame.draw.line(surface, KOLLANE, (110, 50), (20, 50), 2)

    step = 32
    pygame.draw.line(surface, KOLLANE, (65 - step, 50 - step), (65 + step, 50 + step), 2)
    pygame.draw.line(surface, KOLLANE, (65 + step, 50 - step), (65 - step, 50 + step), 2)


# -----------------------------------
# Põhitsükkel
# -----------------------------------
while töötab:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            töötab = False

    EKRAAN.fill(TAUST)

    # Joonistamine
    joonista_lumememm(EKRAAN)
    joonista_päike(EKRAAN)

    joonista_pilv(EKRAAN, 250, 47)
    joonista_pilv(EKRAAN, 280, 12)
    joonista_pilv(EKRAAN, 200, 14)

    pygame.display.flip()

pygame.quit()
