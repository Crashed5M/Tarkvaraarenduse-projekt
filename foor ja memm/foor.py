import pygame # Impordib PyGame mooduli
pygame.init() # Käivitab mooduli

screen = pygame.display.set_mode((300, 300)) # Loon akna
pygame.display.set_caption("Valgusfoor-Karl-Eerik Pendonen") # Akna pealkiri

# Värvid, mida kasutan
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
GRAY = (60, 60, 60)   # uus taustavärv

work = True  # Näitab, kas programm töötab veel

while work:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            work = False

    # Taustavärv (hall)
    screen.fill(GRAY)

    # Valgusfoori korpus
    pygame.draw.rect(screen, BLACK, (120, 30, 60, 160))

    # Valgusfoori tuled
    pygame.draw.circle(screen, RED, (150, 60), 19)
    pygame.draw.circle(screen, YELLOW, (150, 105), 19)
    pygame.draw.circle(screen, GREEN, (150, 150), 19)

    # Valgusfoori post
    pygame.draw.rect(screen, BLACK, (145, 190, 10, 60))

    # Must trapets (postialus)
    polygon = [(90, 287.5), (210, 287.5), (165, 242.5), (135, 242.5)]
    pygame.draw.polygon(screen, BLACK, polygon)

    pygame.display.flip()

pygame.quit()
