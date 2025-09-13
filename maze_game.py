import pygame
import random

# Constants
CELL_SIZE = 40
MAZE_WIDTH = 15  # number of cells horizontally
MAZE_HEIGHT = 15  # number of cells vertically
SCREEN_WIDTH = CELL_SIZE * MAZE_WIDTH
SCREEN_HEIGHT = CELL_SIZE * MAZE_HEIGHT
FPS = 30
NUM_COINS = 20  # number of coins to place

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
CAT_COLOR = (255, 100, 100)
COIN_COLOR = (255, 215, 0)  # gold

# Directions for maze carving
DIRS = [(0, -1), (1, 0), (0, 1), (-1, 0)]  # N, E, S, W

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Random Maze with Cat and Coins")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# Maze generation using DFS
def generate_maze(w, h):
    maze = [[1] * w for _ in range(h)]  # 1 = wall, 0 = path

    def carve_passages(cx, cy):
        maze[cy][cx] = 0
        directions = DIRS[:]
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = cx + dx*2, cy + dy*2
            if 0 <= nx < w and 0 <= ny < h and maze[ny][nx] == 1:
                maze[cy + dy][cx + dx] = 0
                carve_passages(nx, ny)

    # Start carving from (1,1)
    carve_passages(1, 1)
    return maze

# Load a simple cat image or draw a simple rectangle as placeholder
def draw_cat(surface, x, y):
    # Draw a simple cat face (circle + eyes)
    center_x = x * CELL_SIZE + CELL_SIZE // 2
    center_y = y * CELL_SIZE + CELL_SIZE // 2
    pygame.draw.circle(surface, CAT_COLOR, (center_x, center_y), CELL_SIZE // 2 - 4)
    eye_radius = 4
    pygame.draw.circle(surface, BLACK, (center_x - 10, center_y - 8), eye_radius)
    pygame.draw.circle(surface, BLACK, (center_x + 10, center_y - 8), eye_radius)
    pygame.draw.polygon(surface, BLACK, [(center_x - 12, center_y - 25), (center_x - 5, center_y - 35), (center_x, center_y - 25)])  # left ear
    pygame.draw.polygon(surface, BLACK, [(center_x + 12, center_y - 25), (center_x + 5, center_y - 35), (center_x, center_y - 25)])  # right ear

def draw_coin(surface, x, y):
    center_x = x * CELL_SIZE + CELL_SIZE // 2
    center_y = y * CELL_SIZE + CELL_SIZE // 2
    pygame.draw.circle(surface, COIN_COLOR, (center_x, center_y), CELL_SIZE // 4)
    # simple shine
    pygame.draw.circle(surface, WHITE, (center_x - 5, center_y - 5), 5)

def place_coins(maze, num_coins, cat_pos):
    coins = set()
    free_cells = [(x, y) for y in range(MAZE_HEIGHT) for x in range(MAZE_WIDTH)
                  if maze[y][x] == 0 and (x, y) != cat_pos]
    random.shuffle(free_cells)
    for pos in free_cells[:num_coins]:
        coins.add(pos)
    return coins

def main():
    maze = generate_maze(MAZE_WIDTH, MAZE_HEIGHT)
    cat_x, cat_y = 1, 1  # starting position inside maze (path)
    coins = place_coins(maze, NUM_COINS, (cat_x, cat_y))
    score = 0

    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        moved = False
        if keys[pygame.K_LEFT]:
            if cat_x > 0 and maze[cat_y][cat_x - 1] == 0:
                cat_x -= 1
                moved = True
        if keys[pygame.K_RIGHT]:
            if cat_x < MAZE_WIDTH - 1 and maze[cat_y][cat_x + 1] == 0:
                cat_x += 1
                moved = True
        if keys[pygame.K_UP]:
            if cat_y > 0 and maze[cat_y - 1][cat_x] == 0:
                cat_y -= 1
                moved = True
        if keys[pygame.K_DOWN]:
            if cat_y < MAZE_HEIGHT - 1 and maze[cat_y + 1][cat_x] == 0:
                cat_y += 1
                moved = True

        # If moved, check coin collection
        if moved and (cat_x, cat_y) in coins:
            coins.remove((cat_x, cat_y))
            score += 1

        # Draw maze
        screen.fill(BLACK)
        for y in range(MAZE_HEIGHT):
            for x in range(MAZE_WIDTH):
                color = WHITE if maze[y][x] == 1 else GRAY
                pygame.draw.rect(screen, color, (x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE))
        
        # Draw coins
        for cx, cy in coins:
            draw_coin(screen, cx, cy)

        # Draw cat
        draw_cat(screen, cat_x, cat_y)

        # Draw score
        score_text = font.render(f"Coins: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
