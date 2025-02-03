import pygame
import random
import time
from pygame import mixer

# Initialize Pygame
pygame.init()
# Initialize Pygame mixer
mixer.init()

# Load and play background music
#mixer.music.load("2-18. Dreiton.mp3")  # Replace with your file name
#mixer.music.set_volume(0.5)  # Adjust volume (0.0 to 1.0)
#mixer.music.play(-1)  # Play the music on a loop

# Screen dimensions
GRID_SIZE = 7
TILE_SIZE = 60  # Increased tile size
PADDING = 5  # Space between tiles
SCREEN_WIDTH = GRID_SIZE * (TILE_SIZE + PADDING) - PADDING
SCREEN_HEIGHT = GRID_SIZE * (TILE_SIZE + PADDING) + 100  # Increased to accommodate the score and time display

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (135, 206, 250)
LIGHT_GRAY = (200, 200, 200)
MUTED_BLUE = (173, 216, 230)
BORDER_COLOR = (100, 100, 100)
SELECTED_COLOR = (100, 149, 237)  # Darker blue for selected tile

# Define piece types
#PIECES = ['mammoth', 'moai', 'fossil', 'pharaoh', 'mask']
#PIECES = ['helmet', 'eye-mask', 'hammer', 'nuclear', 'regeneration']
#PIECES = ['bonfire', 'candy-cane', 'cookie', 'deer', 'snow-globe']
#PIECES = ['starfish', 'pamela-hat', 'help', 'coconut-drink', 'watermelon']
#PIECES = ['parrot', 'pirates', 'compass', 'ship-wheel', 'hook']
#PIECES = ['cone', 'cross', 'cube', 'cylinder', 'geometry']
PIECES = ['voodoo-doll', 'cauldron', 'pumpkin', 'frankenstein', 'decapitate']

# Load images
images = {piece: pygame.transform.scale(pygame.image.load(f"{piece}.png"), (TILE_SIZE, TILE_SIZE)) for piece in PIECES}

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Match-3 Game")

# Font for score and time
default_font = pygame.font.Font(pygame.font.get_default_font(), 24)


# Create grid

def create_grid():
    while True:
        grid = [[random.choice(PIECES) for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        if not check_match(grid):
            return grid


def draw_grid(grid, selected_tile):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x = col * (TILE_SIZE + PADDING)
            y = row * (TILE_SIZE + PADDING) + 100  # Adjusted for the top display
            if selected_tile == (row, col):
                pygame.draw.rect(screen, SELECTED_COLOR, (x, y, TILE_SIZE, TILE_SIZE))  # Highlight selected tile
            pygame.draw.rect(screen, BORDER_COLOR, (x, y, TILE_SIZE, TILE_SIZE), 1)  # Border
            if grid[row][col] is not None:  # Only draw non-None tiles
                screen.blit(images[grid[row][col]], (x, y))


def draw_score_and_time(score, remaining_time):
    pygame.draw.rect(screen, LIGHT_GRAY, (0, 0, SCREEN_WIDTH, 100))
    pygame.draw.line(screen, BLACK, (0, 100), (SCREEN_WIDTH, 100), 2)
    score_text = default_font.render(f"Score: {score}", True, BLACK)
    #time_elapsed = int(time.time() - remaining_time)
    time_text = default_font.render(f"Time: {remaining_time}s", True, BLACK)
    screen.blit(score_text, (20, 30))
    screen.blit(time_text, (SCREEN_WIDTH - 120, 30))

def check_match(grid):
    matches = []
    # Check rows
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE - 2):
            if grid[row][col] == grid[row][col + 1] == grid[row][col + 2]:
                matches.append((row, col))
                matches.append((row, col + 1))
                matches.append((row, col + 2))

    # Check columns
    for col in range(GRID_SIZE):
        for row in range(GRID_SIZE - 2):
            if grid[row][col] == grid[row + 1][col] == grid[row + 2][col]:
                matches.append((row, col))
                matches.append((row + 1, col))
                matches.append((row + 2, col))
    return list(set(matches))


def remove_matches(grid, matches):
    for row, col in matches:
        grid[row][col] = None


def drop_pieces(grid):
    for col in range(GRID_SIZE):
        for row in range(GRID_SIZE - 1, -1, -1):  # Start from the bottom row
            if grid[row][col] is None:  # If there's an empty cell
                # Look upwards for a non-None piece
                for above_row in range(row - 1, -1, -1):
                    if grid[above_row][col] is not None:
                        # Move the piece down
                        grid[row][col] = grid[above_row][col]
                        grid[above_row][col] = None
                        break


def animate_drop(grid, score, remaining_time):
    for _ in range(10):  # Increase for smoother animation
        screen.fill(MUTED_BLUE)
        draw_grid(grid, None)
        draw_score_and_time(score, remaining_time)
        pygame.display.flip()
        pygame.time.delay(70)



def refill_grid(grid):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if grid[row][col] is None:
                grid[row][col] = random.choice(PIECES)


def swap(grid, pos1, pos2):
    grid[pos1[0]][pos1[1]], grid[pos2[0]][pos2[1]] = grid[pos2[0]][pos2[1]], grid[pos1[0]][pos1[1]]


# def animate_removal(matches):
#     for _ in range(5):  # Simple animation effect
#         for row, col in matches:
#             x = col * (TILE_SIZE + PADDING)
#             y = row * (TILE_SIZE + PADDING) + 100
#             pygame.draw.rect(screen, BLUE, (x, y, TILE_SIZE, TILE_SIZE))
#         pygame.display.flip()
#         pygame.time.delay(70)

def animate_removal(grid, matches,score, remaining_time):
    for alpha in range(255, 0, -25):  # Gradually reduce opacity
        screen.fill(MUTED_BLUE)  # Clear screen
        draw_grid(grid, None)  # Draw the existing grid
        draw_score_and_time(score, remaining_time)
        for row, col in matches:
            x = col * (TILE_SIZE + PADDING)
            y = row * (TILE_SIZE + PADDING) + 100
            temp_surface = pygame.Surface((TILE_SIZE, TILE_SIZE))
            temp_surface.set_alpha(alpha)  # Set opacity
            temp_surface.fill(WHITE)  # Fill with a fade color (can adjust as needed)
            screen.blit(temp_surface, (x, y))  # Overlay fading tile

        pygame.display.flip()
        pygame.time.delay(30)  # Adjust speed of fade-out

    # Remove the tiles after the animation
    for row, col in matches:
        grid[row][col] = None

#
# def animate_swap(grid, pos1, pos2):
#     for i in range(5):
#         offset = 5 if i % 2 == 0 else -5
#         draw_grid(grid, None)
#         x1, y1 = pos1[1] * (TILE_SIZE + PADDING), pos1[0] * (TILE_SIZE + PADDING) + 100
#         x2, y2 = pos2[1] * (TILE_SIZE + PADDING), pos2[0] * (TILE_SIZE + PADDING) + 100
#         screen.blit(images[grid[pos1[0]][pos1[1]]], (x1 + offset, y1))
#         screen.blit(images[grid[pos2[0]][pos2[1]]], (x2 - offset, y2))
#         pygame.display.flip()
#         pygame.time.delay(50)
def animate_swap(grid, pos1, pos2,score, remaining_time):
    x1, y1 = pos1[1] * (TILE_SIZE + PADDING), pos1[0] * (TILE_SIZE + PADDING) + 100
    x2, y2 = pos2[1] * (TILE_SIZE + PADDING), pos2[0] * (TILE_SIZE + PADDING) + 100
    for i in range(10):
        offset = i * (TILE_SIZE // 10)
        screen.fill(MUTED_BLUE)
        draw_grid(grid, None)
        draw_score_and_time(score, remaining_time)

        if x1 < x2:
            screen.blit(images[grid[pos1[0]][pos1[1]]], (x1 + offset, y1))
            screen.blit(images[grid[pos2[0]][pos2[1]]], (x2 - offset, y2))
        elif y1 < y2:
            screen.blit(images[grid[pos1[0]][pos1[1]]], (x1, y1 + offset))
            screen.blit(images[grid[pos2[0]][pos2[1]]], (x2, y2 - offset))
        elif x1 > x2:
            screen.blit(images[grid[pos1[0]][pos1[1]]], (x1 - offset, y1))
            screen.blit(images[grid[pos2[0]][pos2[1]]], (x2 + offset, y2))
        elif y1 > y2:
            screen.blit(images[grid[pos1[0]][pos1[1]]], (x1, y1 - offset))
            screen.blit(images[grid[pos2[0]][pos2[1]]], (x2, y2 + offset))
        pygame.display.flip()
        pygame.time.delay(25)


def animate_shake(grid, pos1, pos2):
    for i in range(4):
        offset = 5 if i % 2 == 0 else -5
        draw_grid(grid, None)
        x1, y1 = pos1[1] * (TILE_SIZE + PADDING), pos1[0] * (TILE_SIZE + PADDING) + 100
        x2, y2 = pos2[1] * (TILE_SIZE + PADDING), pos2[0] * (TILE_SIZE + PADDING) + 100
        screen.blit(images[grid[pos1[0]][pos1[1]]], (x1 + offset, y1))
        screen.blit(images[grid[pos2[0]][pos2[1]]], (x2 - offset, y2))
        pygame.display.flip()
        pygame.time.delay(25)


def valid_swap(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1]) == 1




def game_over_screen(score, high_score):
    screen.fill(BLACK)
    game_over_text = default_font.render("GAME OVER", True, WHITE)
    score_text = default_font.render(f"Your Score: {score}", True, WHITE)
    high_score_text = default_font.render(f"High Score: {high_score}", True, WHITE)
    play_again_text = default_font.render("Click to PLAY AGAIN", True, WHITE)

    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 60))
    screen.blit(score_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 20))
    screen.blit(high_score_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 20))
    screen.blit(play_again_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 60))

    pygame.display.flip()


def main():
    clock = pygame.time.Clock()
    grid = create_grid()
    selected_tile = None
    score = 0
    high_score = 0
    total_time = 10  # Game duration in seconds
    start_time = time.time()

    running = True
    game_over = False

    while running:
        if not game_over:
            remaining_time = max(0, total_time - int(time.time() - start_time))
            if remaining_time == 0:
                game_over = True
                high_score = max(high_score, score)

            screen.fill(MUTED_BLUE)
            draw_grid(grid, selected_tile)
            draw_score_and_time(score, remaining_time)
            pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if not game_over and event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                row, col = (y - 100) // (TILE_SIZE + PADDING), x // (TILE_SIZE + PADDING)
                if row >= 0:
                    if selected_tile:
                        if valid_swap(selected_tile, (row, col)):
                            animate_swap(grid, selected_tile, (row, col),score, remaining_time)
                            swap(grid, selected_tile, (row, col))
                            if not check_match(grid):
                                animate_shake(grid, selected_tile, (row, col))
                                swap(grid, selected_tile, (row, col))  # Swap back if no match
                            else:
                                while True:
                                    matches = check_match(grid)
                                    if not matches:
                                        break
                                    animate_removal(grid,matches,score, remaining_time)
                                    score += len(matches) * 10
                                    total_time += 2  # Add 5 seconds for each match
                                    remove_matches(grid, matches)
                                    drop_pieces(grid)
                                    animate_drop(grid, score, remaining_time)
                                    refill_grid(grid)
                        selected_tile = None
                    else:
                        selected_tile = (row, col)

            if game_over and event.type == pygame.MOUSEBUTTONDOWN:
                # Restart the game
                grid = create_grid()
                total_time = 10
                selected_tile = None
                score = 0
                start_time = time.time()
                game_over = False

        if game_over:
            game_over_screen(score, high_score)

        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()
