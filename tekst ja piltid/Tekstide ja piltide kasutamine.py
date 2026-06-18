import pygame
import math

pygame.init()

# Ekraan
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Ülesanne 2")

# Font
font = pygame.font.SysFont("Arial", 40)

# --- PILDID (parandatud failiteed!) ---

shop = pygame.image.load(r"C:\Users\karle\Desktop\tarkvaraarenuds\tarkvara\pildid\bg_shop.jpg")

man = pygame.image.load(r"C:\Users\karle\Desktop\tarkvaraarenuds\tarkvara\pildid\seller.png")
man = pygame.transform.scale(man, (233, 275))

textbox = pygame.image.load(r"C:\Users\karle\Desktop\tarkvaraarenuds\tarkvara\pildid\chat.png")
textbox = pygame.transform.scale(textbox, (285, 226))

sword = pygame.image.load(r"C:\Users\karle\Desktop\tarkvaraarenuds\tarkvara\pildid\Mõõk.png")
sword = pygame.transform.scale(sword, (157, 130))

cake = pygame.image.load(r"C:\Users\karle\Desktop\tarkvaraarenuds\tarkvara\pildid\ball.png")
cake = pygame.transform.scale(cake, (107, 127))

logo = pygame.image.load(r"C:\Users\karle\Desktop\tarkvaraarenuds\tarkvara\pildid\VIKK logo.png")
logo = pygame.transform.scale(logo, (640, 480))

# Tsükkel
work = True
clock = pygame.time.Clock()

while work:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            work = False

    # Taust
    screen.blit(shop, (0, 0))

    # Objektid
    screen.blit(man, (110, 185))
    screen.blit(textbox, (235, 50))
    screen.blit(sword, (510, 100))
    screen.blit(cake, (400, 170))
    screen.blit(logo, (10, 10))

    # Tekst
    text = font.render("Tere, olen Karl", True, (255, 255, 255))
    screen.blit(text, (270, 120))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
