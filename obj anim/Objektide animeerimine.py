import sys
import pygame

pygame.init()

# -----------------------------------
# Seaded
# -----------------------------------
LAIUS, KORGUS = 640, 480
EKRAAN = pygame.display.set_mode((LAIUS, KORGUS))
pygame.display.set_caption("Objektide animeerimine")
clock = pygame.time.Clock()

FONT = pygame.font.Font(None, 30)

# -----------------------------------
# Piltide laadimine (parandatud failiteed!)
# -----------------------------------
taust = pygame.image.load(r"/tarkvara/pildid/bg_rally.jpg")
taust = pygame.transform.scale(taust, (LAIUS, KORGUS))

punane_auto = pygame.transform.scale(
    pygame.image.load(r"/tarkvara/pildid/f1_red.png"), (45, 90)
)

sinine_auto = pygame.transform.scale(
    pygame.image.load(r"/tarkvara/pildid/f1_blue.png"), (45, 90)
)

# -----------------------------------
# Autode algpositsioonid ja kiirused
# -----------------------------------
punane = {"x": 320, "y": 380}

sinine1 = {"x": 390, "y": -50, "kiirus": 2}
sinine2 = {"x": 150, "y": 0, "kiirus": 3}

skoor = 0
gameover = False

# -----------------------------------
# Funktsioon siniste autode liigutamiseks
# -----------------------------------
def liigu_sinine(auto):
    global skoor
    auto["y"] += auto["kiirus"]

    if auto["y"] > KORGUS:
        auto["y"] = -90
        skoor += 1

# -----------------------------------
# Põhitsükkel
# -----------------------------------
while not gameover:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameover = True

    # Liiguta siniseid autosid
    liigu_sinine(sinine1)
    liigu_sinine(sinine2)

    # Joonista ekraan
    EKRAAN.blit(taust, (0, 0))
    EKRAAN.blit(sinine_auto, (sinine1["x"], sinine1["y"]))
    EKRAAN.blit(sinine_auto, (sinine2["x"], sinine2["y"]))
    EKRAAN.blit(punane_auto, (punane["x"], punane["y"]))

    # Skoor
    tekst = FONT.render(f"Skoor: {skoor}", True, (255, 255, 255))
    EKRAAN.blit(tekst, (10, 10))

    pygame.display.flip()

pygame.quit()
sys.exit()
