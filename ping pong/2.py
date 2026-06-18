import pygame
import sys
import random

pygame.init()
pygame.mixer.init()

# =========================
# EKRAAN
# =========================
SCREEN_W, SCREEN_H = 960, 540
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("NEON CYBER PONG")
clock = pygame.time.Clock()

# =========================
# VÄRVID (NEON)
# =========================
WHITE = (255, 255, 255)
NEON_BLUE = (0, 255, 255)
NEON_PINK = (255, 0, 150)
NEON_PURPLE = (180, 0, 255)
BACKGROUND = (10, 10, 20)

# =========================
# FONTS
# =========================
title_font = pygame.font.SysFont("consolas", 72, bold=True)
menu_font = pygame.font.SysFont("consolas", 30, bold=True)
score_font = pygame.font.SysFont("consolas", 40, bold=True)

# =========================
# HELID (SAMAD MIS ENNE)
# =========================
bounce_sound = pygame.mixer.Sound("bounce.wav")
appear_sound = pygame.mixer.Sound("appear.wav")

pygame.mixer.music.load("background.mp3")
pygame.mixer.music.set_volume(0.6)

# =========================
# OBJEKTID
# =========================
player = pygame.Rect(SCREEN_W // 2 - 100, SCREEN_H - 60, 200, 22)
ball = pygame.Rect(SCREEN_W // 2, SCREEN_H // 2, 20, 20)

ball_speed_x = 6
ball_speed_y = -6
score = 0

# =========================
# PALLI SABA
# =========================
trail = []

def add_trail():
    trail.append([ball.centerx, ball.centery, 20])
    if len(trail) > 15:
        trail.pop(0)

# =========================
# PARTICLES INTRO
# =========================
particles = []

def create_particles():
    for _ in range(25):
        particles.append([
            random.randint(0, SCREEN_W),
            random.randint(-SCREEN_H, 0),
            random.randint(2, 6)
        ])

def reset_ball():
    global ball_speed_x, ball_speed_y
    ball.center = (SCREEN_W // 2, SCREEN_H // 2)
    ball_speed_x = random.choice([-6, 6])
    ball_speed_y = -6

create_particles()

# =========================
# INTRO
# =========================
intro = True
intro_anim = -400
appear_sound.play()

while intro:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            intro = False
            pygame.mixer.music.play(-1)

    # Taust (neon grid)
    screen.fill(BACKGROUND)
    for i in range(0, SCREEN_W, 40):
        pygame.draw.line(screen, (20, 20, 40), (i, 0), (i, SCREEN_H))
    for j in range(0, SCREEN_H, 40):
        pygame.draw.line(screen, (20, 20, 40), (0, j), (SCREEN_W, j))

    # Particles
    for p in particles:
        pygame.draw.rect(screen, NEON_BLUE, (p[0], p[1], 4, 20))
        p[1] += p[2]
        if p[1] > SCREEN_H:
            p[1] = random.randint(-200, -20)
            p[0] = random.randint(0, SCREEN_W)

    # Title animation
    if intro_anim < 130:
        intro_anim += 12

    title = title_font.render("NEON CYBER PONG", True, NEON_PINK)
    shadow = title_font.render("NEON CYBER PONG", True, NEON_PURPLE)

    screen.blit(shadow, shadow.get_rect(center=(SCREEN_W // 2 + 5, intro_anim + 5)))
    screen.blit(title, title.get_rect(center=(SCREEN_W // 2, intro_anim)))

    screen.blit(menu_font.render("PRESS ANY KEY TO START", True, WHITE),
                (SCREEN_W // 2 - 180, 300))
    screen.blit(menu_font.render("MOVE WITH A / D", True, NEON_BLUE),
                (SCREEN_W // 2 - 110, 350))

    pygame.display.flip()

# =========================
# GAME LOOP
# =========================
running = True

while running:
    clock.tick(60)

    # EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # INPUT
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player.x -= 9
    if keys[pygame.K_d]:
        player.x += 9

    # clamp
    player.left = max(player.left, 0)
    player.right = min(player.right, SCREEN_W)

    # BALL MOVEMENT
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    add_trail()

    if ball.left <= 0 or ball.right >= SCREEN_W:
        ball_speed_x *= -1
        bounce_sound.play()

    if ball.top <= 0:
        ball_speed_y *= -1
        bounce_sound.play()

    # paddle collision
    if ball.colliderect(player) and ball_speed_y > 0:
        ball.bottom = player.top
        ball_speed_y *= -1

        offset = (ball.centerx - player.centerx) / 18
        ball_speed_x = int(offset) or random.choice([-4, 4])

        bounce_sound.play()
        score += 1

    # GAME OVER
    if ball.top > SCREEN_H:
        waiting = True
        while waiting:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    score = 0
                    reset_ball()
                    waiting = False

            screen.fill(BACKGROUND)
            game_over = title_font.render("GAME OVER", True, NEON_PINK)
            restart = menu_font.render("PRESS R TO RESTART", True, WHITE)

            screen.blit(game_over, game_over.get_rect(center=(SCREEN_W // 2, 220)))
            screen.blit(restart, restart.get_rect(center=(SCREEN_W // 2, 320)))

            pygame.display.flip()

    # =========================
    # DRAW
    # =========================
    screen.fill(BACKGROUND)

    # neon grid
    for i in range(0, SCREEN_W, 40):
        pygame.draw.line(screen, (20, 20, 40), (i, 0), (i, SCREEN_H))
    for j in range(0, SCREEN_H, 40):
        pygame.draw.line(screen, (20, 20, 40), (0, j), (SCREEN_W, j))

    # palli saba
    for t in trail:
        pygame.draw.circle(screen, NEON_PINK, (t[0], t[1]), t[2], 2)

    # pall (glow)
    pygame.draw.circle(screen, NEON_PINK, ball.center, 18)
    pygame.draw.circle(screen, WHITE, ball.center, 8)

    # paddle (glow)
    pygame.draw.rect(screen, NEON_BLUE, player, border_radius=12)
    pygame.draw.rect(screen, WHITE, player.inflate(-10, -10), border_radius=12)

    # skoor
    score_text = score_font.render(f"SCORE: {score}", True, WHITE)
    screen.blit(score_text, (25, 20))

    pygame.display.flip()

pygame.quit()
