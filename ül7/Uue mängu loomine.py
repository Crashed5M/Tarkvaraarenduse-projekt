import pygame
import sys
import random
import time

pygame.init()

# Ekraan
W, H = 640, 480
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Hiiremäng – Karl‑Eerik")
clock = pygame.time.Clock()

# Värvid
TAUST = (173, 216, 230)
RING_VÄRV = (0, 0, 139)
BOONUS = (220, 20, 60)
MUST = (0, 0, 0)

# Konstandid
ALGRAADIUS = 10
KASV = 5
MAX_RINGID = 10
BOONUS_TÕENÄOSUS = 0.2
RINGI_ELUAEG = 3  # sekundites

font = pygame.font.SysFont("Arial", 20)

# Ringi struktuur: x, y, raadius, boonusring?, loomise aeg
ringid = []
skoor = 0
mäng_läbi = False

# Raskusastme süsteem
algusaeg = time.time()
raskus = 1.0


def reset():
    global ringid, skoor, mäng_läbi, algusaeg, raskus
    ringid = []
    skoor = 0
    mäng_läbi = False
    algusaeg = time.time()
    raskus = 1.0


while True:

    # Arvutame raskuse (kasvab ajaga)
    raskus = 1.0 + (time.time() - algusaeg) * 0.1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Restart
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            reset()

        # Klõps
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not mäng_läbi:
            mx, my = event.pos

            # Kontrollime, kas klikk tabas mõnda ringi
            tabas = False
            for r in ringid[:]:
                dx = mx - r["x"]
                dy = my - r["y"]
                if dx*dx + dy*dy <= r["raadius"]**2:
                    tabas = True
                    skoor += 3 if r["on_boonus"] else 1
                    ringid.remove(r)
                    break

            # Möödalaskmine lõpetab mängu AINULT kui ringe juba oli
            if not tabas and len(ringid) > 0:
                mäng_läbi = True

            # Loome uue ringi
            uus_raadius = max(5, (ALGRAADIUS + len(ringid) * KASV) / raskus)
            boonuse_tõenäosus = max(0.05, BOONUS_TÕENÄOSUS / raskus)
            on_boonus = random.random() < boonuse_tõenäosus

            ringid.append({
                "x": mx,
                "y": my,
                "raadius": uus_raadius,
                "on_boonus": on_boonus,
                "aeg": time.time()
            })

            # Liiga palju ringe → eemaldame vanima
            while len(ringid) > MAX_RINGID:
                ringid.pop(0)

    # Taust
    screen.fill(TAUST)

    # Ringi eluaja kontroll (eluiga lüheneb raskusega)
    nüüd = time.time()
    for r in ringid[:]:
        if nüüd - r["aeg"] > RINGI_ELUAEG / raskus:
            ringid.remove(r)

    # Joonistame ringid
    for r in ringid:
        värv = BOONUS if r["on_boonus"] else RING_VÄRV

        # Boonusring pulseerib
        if r["on_boonus"]:
            pulse = int((time.time() * 5) % 2) * 2 + 1
            pygame.draw.circle(screen, värv, (r["x"], r["y"]), int(r["raadius"]), pulse)
        else:
            pygame.draw.circle(screen, värv, (r["x"], r["y"]), int(r["raadius"]), 2)

    # Tekstid
    skooritekst = font.render(f"Skoor: {skoor}", True, MUST)
    screen.blit(skooritekst, (10, 10))


    raskustekst = font.render(f"Raskus: {raskus:.2f}", True, MUST)
    screen.blit(raskustekst, (10, 35))

    if mäng_läbi:
        lõpp = font.render("Mäng läbi! Vajuta R, et uuesti alustada", True, (200, 0, 0))
        screen.blit(lõpp, (W//2 - lõpp.get_width()//2, H//2))

    pygame.display.flip()
    clock.tick(60)
