import pygame
import sys

pygame.init()

# Värvid
taust = (200, 200, 200)      # helehall taust
ruut = (0, 0, 0)             # must ruudustiku värv

# Ekraan
width = 640
height = 480
square = 10

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Ülesanne 3")

running = True

while running:
    screen.fill(taust)  # uus taustavärv

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Ruudustik
    for y in range(0, height, square):
        for x in range(0, width, square):
            rect = pygame.Rect(x, y, square, square)
            pygame.draw.rect(screen, ruut, rect, 1)  # uus ruuduvärv

    pygame.display.flip()

pygame.quit()
sys.exit()
