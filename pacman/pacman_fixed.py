import pygame
import sys
import random

pygame.init()

# Ekraani seaded
WIDTH, HEIGHT = 840, 930
TILE = 30

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man - Kombineeritud")
clock = pygame.time.Clock()
FPS = 60

# Värvid
BLACK = (10, 10, 20)
BLUE = (0, 0, 180)
YELLOW = (255, 220, 0)
WHITE = (240, 240, 240)
RED = (255, 60, 60)
PINK = (255, 150, 200)
CYAN = (0, 255, 255)
ORANGE = (255, 180, 0)
SCARED_BLUE = (80, 80, 255)

# Maze
maze_layout = [
    "############################",
    "#............##............#",
    "#.####.#####.##.#####.####.#",
    "#o####.#####.##.#####.####o#",
    "#.####.#####.##.#####.####.#",
    "#..........................#",
    "#.####.##.########.##.####.#",
    "#.####.##.########.##.####.#",
    "#......##....##....##......#",
    "######.#####.##.#####.######",
    "######.#####.##.#####.######",
    "#............##............#",
    "#.####.#####.##.#####.####.#",
    "#.####.#####.##.#####.####.#",
    "#o..##................##..o#",
    "###.##.##.########.##.##.###",
    "###.##.##.########.##.##.###",
    "#......##....##....##......#",
    "#.####.#####.##.#####.####.#",
    "#.####.#####.##.#####.####.#",
    "#..........................#",
    "############################"
]

ROWS = len(maze_layout)
COLS = len(maze_layout[0])

# 0 = tühi, 1 = punkt, 2 = power pellet, 3 = sein
level = [[1 if c == '.' else 2 if c == 'o' else 3 if c == '#' else 0 for c in row] for row in maze_layout]

# Mängija
player_x = 14 * TILE + TILE // 2
player_y = 20 * TILE + TILE // 2
player_speed = 2

direction = (0, 0)
next_direction = (0, 0)

score = 0
lives = 3

# Ghostid
ghosts = [
    {"x": 14 * TILE + TILE // 2, "y": 9 * TILE + TILE // 2, "color": RED, "dir": (2, 0), "scared": False},
    {"x": 13 * TILE + TILE // 2, "y": 9 * TILE + TILE // 2, "color": PINK, "dir": (-2, 0), "scared": False},
    {"x": 15 * TILE + TILE // 2, "y": 9 * TILE + TILE // 2, "color": CYAN, "dir": (0, 2), "scared": False},
    {"x": 14 * TILE + TILE // 2, "y": 10 * TILE + TILE // 2, "color": ORANGE, "dir": (0, -2), "scared": False}
]

scared_timer = 0

# Font
font_small = pygame.font.Font(None, 36)
font_big = pygame.font.Font(None, 60)


# ------------------------------
# Abifunktsioonid
# ------------------------------
def can_move_tile(tx, ty):
    if 0 <= ty < ROWS and 0 <= tx < COLS:
        return level[ty][tx] != 3
    return False


def aligned(value):
    # Kas tegelane on ruudu keskpunktis (TILE // 2)?
    return value % TILE == TILE // 2


# ------------------------------
# Mängija liikumine
# ------------------------------
def update_player():
    global player_x, player_y, direction

    px, py = player_x, player_y
    tx, ty = px // TILE, py // TILE

    if aligned(px) and aligned(py):
        # proovi pöörata järgmisse suunda
        if next_direction != direction:
            nx = tx + next_direction[0] // player_speed
            ny = ty + next_direction[1] // player_speed
            if can_move_tile(nx, ny):
                direction = next_direction

        # kontrolli, kas praegune suund on lubatud
        nx = tx + direction[0] // player_speed
        ny = ty + direction[1] // player_speed
        if not can_move_tile(nx, ny):
            direction = (0, 0)

    player_x += direction[0]
    player_y += direction[1]


# ------------------------------
# Ghostid
# ------------------------------
def update_ghosts():
        global scared_timer

        for ghost in ghosts:
            ghost["scared"] = scared_timer > 0

            gx, gy = ghost["x"], ghost["y"]

            # Kui kummitus on ruudu keskel, vali uus suund
            if aligned(gx) and aligned(gy):
                tx = gx // TILE
                ty = gy // TILE

                dirs = [(2, 0), (-2, 0), (0, 2), (0, -2)]
                valid_dirs = []

                for d in dirs:
                    nx = tx + d[0] // 2
                    ny = ty + d[1] // 2
                    if can_move_tile(nx, ny):
                        valid_dirs.append(d)

                # väldi tagasi pööramist
                if ghost["dir"] != (0, 0):
                    opposite = (-ghost["dir"][0], -ghost["dir"][1])
                    if opposite in valid_dirs and len(valid_dirs) > 1:
                        valid_dirs.remove(opposite)

                # KÕIK ghostid jälitavad mängijat
                best_dir = None
                best_dist = None
                for d in valid_dirs:
                    nx = gx + d[0]
                    ny = gy + d[1]
                    dist = (nx - player_x) ** 2 + (ny - player_y) ** 2

                    # kui hirmul, jookse eemale
                    if ghost["scared"]:
                        dist = -dist

                    if best_dist is None or dist < best_dist:
                        best_dist = dist
                        best_dir = d

                ghost["dir"] = best_dir if best_dir else (0, 0)

            # liigu valitud suunas
            ghost["x"] += ghost["dir"][0]
            ghost["y"] += ghost["dir"][1]
# ------------------------------
# Punktid
# ------------------------------
def eat_dots():
    global score, scared_timer

    tx = int(player_x // TILE)
    ty = int(player_y // TILE)

    if 0 <= ty < ROWS and 0 <= tx < COLS:
        if level[ty][tx] == 1:
            score += 10
            level[ty][tx] = 0
        elif level[ty][tx] == 2:
            score += 50
            level[ty][tx] = 0
            scared_timer = 600  # veidi pikem aeg


# ------------------------------
# Kokkupõrked
# ------------------------------
def check_collision():
    global lives, player_x, player_y, score

    for ghost in ghosts:
        dist = ((player_x - ghost["x"]) ** 2 + (player_y - ghost["y"]) ** 2) ** 0.5
        if dist < 20:
            if ghost["scared"]:
                score += 200
                ghost["x"], ghost["y"] = 14 * TILE + TILE // 2, 9 * TILE + TILE // 2
                ghost["dir"] = (0, 0)
            else:
                lives -= 1
                player_x, player_y = 14 * TILE + TILE // 2, 20 * TILE + TILE // 2
                direction = (0, 0)
                if lives <= 0:
                    return True
    return False


# ------------------------------
# Joonistamine
# ------------------------------
def draw_maze():
    for y, row in enumerate(level):
        for x, cell in enumerate(row):
            px, py = x * TILE, y * TILE
            if cell == 3:
                pygame.draw.rect(screen, BLUE, (px, py, TILE, TILE), border_radius=6)
            elif cell == 1:
                pygame.draw.circle(screen, WHITE, (px + TILE // 2, py + TILE // 2), 4)
            elif cell == 2:
                pygame.draw.circle(screen, WHITE, (px + TILE // 2, py + TILE // 2), 8)


def draw_player():
    pygame.draw.circle(screen, YELLOW, (int(player_x), int(player_y)), 13)


def draw_ghosts():
    for ghost in ghosts:
        color = SCARED_BLUE if ghost["scared"] else ghost["color"]
        pygame.draw.circle(screen, color, (int(ghost["x"]), int(ghost["y"])), 13)


# ------------------------------
# Mängu tsükkel
# ------------------------------
running = True
while running:
    clock.tick(FPS)
    screen.fill(BLACK)

    # Sündmused
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                next_direction = (player_speed, 0)
            elif event.key == pygame.K_LEFT:
                next_direction = (-player_speed, 0)
            elif event.key == pygame.K_UP:
                next_direction = (0, -player_speed)
            elif event.key == pygame.K_DOWN:
                next_direction = (0, player_speed)

    update_player()
    eat_dots()

    if scared_timer > 0:
        scared_timer -= 1

    update_ghosts()
    game_over = check_collision()

    draw_maze()
    draw_player()
    draw_ghosts()

    score_text = font_small.render(f"Score: {score}   Lives: {lives}", True, WHITE)
    screen.blit(score_text, (10, 5))

    if game_over:
        gameover_text = font_big.render("GAME OVER", True, RED)
        screen.blit(gameover_text, (WIDTH // 2 - 150, HEIGHT // 2))
        pygame.display.flip()
        pygame.time.wait(3000)
        running = False

    pygame.display.flip()

pygame.quit()
sys.exit()
