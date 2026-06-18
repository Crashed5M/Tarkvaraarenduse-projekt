import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 840, 930
TILE = 30

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man - Kombineeritud")
clock = pygame.time.Clock()
FPS = 60

# Värvid
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
PINK = (255, 105, 180)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
SCARED_BLUE = (100, 100, 255)

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

# 0 = tühi, 1 = punkt, 2 = power pellet, 3 = sein
level = [[1 if c == '.' else 2 if c == 'o' else 3 if c == '#' else 0 for c in row] for row in maze_layout]

# Mängija
player_x = 14*TILE + 15
player_y = 20*TILE + 15
player_speed = 4
direction = (0, 0)
score = 0
lives = 3

# Ghostid
ghosts = [
    {"x": 14*TILE+15, "y": 9*TILE+15, "color": RED, "dir": (2, 0), "scared": False},
    {"x": 13*TILE+15, "y": 9*TILE+15, "color": PINK, "dir": (-2, 0), "scared": False},
    {"x": 15*TILE+15, "y": 9*TILE+15, "color": CYAN, "dir": (0, 2), "scared": False},
    {"x": 14*TILE+15, "y": 10*TILE+15, "color": ORANGE, "dir": (0, -2), "scared": False}
]

scared_timer = 0


# ------------------------------
# Joonistamine
# ------------------------------
def draw_maze():
    for y, row in enumerate(level):
        for x, cell in enumerate(row):
            px, py = x*TILE, y*TILE
            if cell == 3:
                pygame.draw.rect(screen, BLUE, (px, py, TILE, TILE))
            elif cell == 1:
                pygame.draw.circle(screen, WHITE, (px+15, py+15), 4)
            elif cell == 2:
                pygame.draw.circle(screen, WHITE, (px+15, py+15), 8)


def draw_player():
    pygame.draw.circle(screen, YELLOW, (int(player_x), int(player_y)), 13)


def draw_ghosts():
    for ghost in ghosts:
        color = SCARED_BLUE if ghost["scared"] else ghost["color"]
        pygame.draw.circle(screen, color, (int(ghost["x"]), int(ghost["y"])), 13)


# ------------------------------
# Liikumine
# ------------------------------
def can_move(x, y):
    tx = int(x // TILE)
    ty = int(y // TILE)
    return 0 <= ty < len(level) and 0 <= tx < len(level[0]) and level[ty][tx] != 3


def update_player():
    global player_x, player_y

    new_x = player_x + direction[0]
    new_y = player_y + direction[1]

    if (can_move(new_x-10, new_y-10) and can_move(new_x+10, new_y-10) and
        can_move(new_x-10, new_y+10) and can_move(new_x+10, new_y+10)):
        player_x, player_y = new_x, new_y


def update_ghosts():
    global scared_timer

    for ghost in ghosts:
        ghost["scared"] = scared_timer > 0

        if random.random() < 0.15:
            dirs = [(2,0), (-2,0), (0,2), (0,-2)]
            random.shuffle(dirs)
            for d in dirs:
                if can_move(ghost["x"] + d[0]*3, ghost["y"] + d[1]*3):
                    ghost["dir"] = d
                    break

        nx = ghost["x"] + ghost["dir"][0]
        ny = ghost["y"] + ghost["dir"][1]

        if can_move(nx, ny):
            ghost["x"], ghost["y"] = nx, ny
        else:
            ghost["dir"] = random.choice([(2,0), (-2,0), (0,2), (0,-2)])


# ------------------------------
# Punktide söömine
# ------------------------------
def eat_dots():
    global score, scared_timer

    tx, ty = int(player_x // TILE), int(player_y // TILE)

    if level[ty][tx] == 1:
        score += 10
        level[ty][tx] = 0

    elif level[ty][tx] == 2:
        score += 50
        level[ty][tx] = 0
        scared_timer = 300


# ------------------------------
# Kokkupõrked
# ------------------------------
def check_collision():
    global lives, player_x, player_y, score

    for ghost in ghosts:
        dist = ((player_x - ghost["x"])**2 + (player_y - ghost["y"])**2)**0.5
        if dist < 20:
            if ghost["scared"]:
                score += 200
                ghost["x"], ghost["y"] = 14*TILE+15, 9*TILE+15
            else:
                lives -= 1
                player_x, player_y = 14*TILE+15, 20*TILE+15
                if lives <= 0:
                    return True
    return False


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
                direction = (player_speed, 0)
            elif event.key == pygame.K_LEFT:
                direction = (-player_speed, 0)
            elif event.key == pygame.K_UP:
                direction = (0, -player_speed)
            elif event.key == pygame.K_DOWN:
                direction = (0, player_speed)

    update_player()
    eat_dots()

    if scared_timer > 0:
        scared_timer -= 1

    update_ghosts()
    game_over = check_collision()

    draw_maze()
    draw_player()
    draw_ghosts()

    score_text = pygame.font.Font(None, 36).render(f"Score: {score}   Lives: {lives}", True, WHITE)
    screen.blit(score_text, (10, 5))

    if game_over:
        gameover_text = pygame.font.Font(None, 60).render("GAME OVER", True, RED)
        screen.blit(gameover_text, (WIDTH//2 - 150, HEIGHT//2))
        pygame.display.flip()
        pygame.time.wait(3000)
        running = False

    pygame.display.flip()

pygame.quit()
sys.exit()
