import pygame
import random
import time
from pygame import mixer

# Initialize Pygame
pygame.init()
mixer.init()

# Screen dimensions
GRID_SIZE = 8
TILE_SIZE = 60
PADDING = 5
SCREEN_WIDTH = GRID_SIZE * (TILE_SIZE + PADDING) - PADDING
SCREEN_HEIGHT = GRID_SIZE * (TILE_SIZE + PADDING) + 100

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (135, 206, 250)
LIGHT_GRAY = (200, 200, 200)
MUTED_BLUE = (173, 216, 230)
BORDER_COLOR = (100, 100, 100)
SELECTED_COLOR = (100, 149, 237)

# Pieces
PIECES = ['bonfire', 'candy-cane', 'cookie', 'deer', 'snow-globe']
images = {piece: pygame.transform.scale(pygame.image.load(f"{piece}.png"), (TILE_SIZE, TILE_SIZE)) for piece in PIECES}

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Match-3 Game")

default_font = pygame.font.Font(pygame.font.get_default_font(), 24)

def create_grid():
    while True:
        grid = [[random.choice(PIECES) for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        if not check_match(grid):
            return grid

def draw_grid(grid, selected_tile):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x = col * (TILE_SIZE + PADDING)
            y = row * (TILE_SIZE + PADDING) + 100
            if selected_tile == (row, col):
                pygame.draw.rect(screen, SELECTED_COLOR, (x, y, TILE_SIZE, TILE_SIZE))
            pygame.draw.rect(screen, BORDER_COLOR, (x, y, TILE_SIZE, TILE_SIZE), 1)
            if grid[row][col]:
                screen.blit(images[grid[row][col]], (x, y))

def draw_score_and_time(score, remaining_time):
    pygame.draw.rect(screen, LIGHT_GRAY, (0, 0, SCREEN_WIDTH, 100))
    pygame.draw.line(screen, BLACK, (0, 100), (SCREEN_WIDTH, 100), 2)
    score_text = default_font.render(f"Score: {score}", True, BLACK)
    time_text = default_font.render(f"Time: {remaining_time}s", True, BLACK)
    screen.blit(score_text, (20, 30))
    screen.blit(time_text, (SCREEN_WIDTH - 150, 30))

def check_match(grid):
    matches = []
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE - 2):
            if grid[row][col] == grid[row][col + 1] == grid[row][col + 2]:
                matches.extend([(row, col), (row, col + 1), (row, col + 2)])
    for col in range(GRID_SIZE):
        for row in range(GRID_SIZE - 2):
            if grid[row][col] == grid[row + 1][col] == grid[row + 2][col]:
                matches.extend([(row, col), (row + 1, col), (row + 2, col)])
    return list(set(matches))

def remove_matches(grid, matches):
    for row, col in matches:
        grid[row][col] = None

def drop_pieces(grid):
    for col in range(GRID_SIZE):
        for row in range(GRID_SIZE - 1, -1, -1):
            if grid[row][col] is None:
                for above_row in range(row - 1, -1, -1):
                    if grid[above_row][col] is not None:
                        grid[row][col] = grid[above_row][col]
                        grid[above_row][col] = None
                        break

def refill_grid(grid):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if grid[row][col] is None:
                grid[row][col] = random.choice(PIECES)

def animate_swap(grid, pos1, pos2):
    x1, y1 = pos1[1] * (TILE_SIZE + PADDING), pos1[0] * (TILE_SIZE + PADDING) + 100
    x2, y2 = pos2[1] * (TILE_SIZE + PADDING), pos2[0] * (TILE_SIZE + PADDING) + 100
    for i in range(10):
        offset = i * (TILE_SIZE // 10)
        screen.fill(MUTED_BLUE)
        draw_grid(grid, None)
        if x1 < x2:
            screen.blit(images[grid[pos1[0]][pos1[1]]], (x1 + offset, y1))
            screen.blit(images[grid[pos2[0]][pos2[1]]], (x2 - offset, y2))
        elif y1 < y2:
            screen.blit(images[grid[pos1[0]][pos1[1]]], (x1, y1 + offset))
            screen.blit(images[grid[pos2[0]][pos2[1]]], (x2, y2 - offset))
        pygame.display.flip()
        pygame.time.delay(30)

def animate_removal(matches):
    for _ in range(5):
        for row, col in matches:
            x = col * (TILE_SIZE + PADDING)
            y = row * (TILE_SIZE + PADDING) + 100
            pygame.draw.rect(screen, BLUE, (x, y, TILE_SIZE, TILE_SIZE))
        pygame.display.flip()
        pygame.time.delay(50)

def animate_drop(grid, score, start_time):
    for _ in range(10):
        screen.fill(MUTED_BLUE)
        draw_score_and_time(score, int(time.time() - start_time))
        draw_grid(grid, None)
        pygame.display.flip()
        pygame.time.delay(50)

def main():
    clock = pygame.time.Clock()
    grid = create_grid()
    selected_tile = None
    score = 0
    start_time = time.time()

    running = True
    while running:
        screen.fill(MUTED_BLUE)
        draw_score_and_time(score, int(60 - (time.time() - start_time)))
        draw_grid(grid, selected_tile)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                row, col = (y - 100) // (TILE_SIZE + PADDING), x // (TILE_SIZE + PADDING)
                if row >= 0:
                    if selected_tile:
                        animate_swap(grid, selected_tile, (row, col))
                        grid[selected_tile[0]][selected_tile[1]], grid[row][col] = grid[row][col], grid[selected_tile[0]][selected_tile[1]]
                        matches = check_match(grid)
                        if not matches:
                            animate_swap(grid, selected_tile, (row, col))
                            grid[selected_tile[0]][selected_tile[1]], grid[row][col] = grid[row][col], grid[selected_tile[0]][selected_tile[1]]
                        else:
                            while matches:
                                animate_removal(matches)
                                score += len(matches) * 10
                                remove_matches(grid, matches)
                                drop_pieces(grid)
                                animate_drop(grid, score, start_time)
                                refill_grid(grid)
                                matches = check_match(grid)
                        selected_tile = None
                    else:
                        selected_tile = (row, col)

        clock.tick(30)
    pygame.quit()

if __name__ == "__main__":
    main()
