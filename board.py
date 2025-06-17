import pygame
import random
import copy
from constants import *


class Board:
    def __init__(self, theme_pieces):
        self.grid_size = GRID_SIZE
        self.tile_size = TILE_SIZE
        self.padding = PADDING
        self.theme_pieces = theme_pieces  # Regular pieces
        self.all_possible_pieces = list(theme_pieces)  # Used for refilling
        self.images = self._load_all_tile_images()
        self.grid = self._create_initial_grid()

    def _load_all_tile_images(self):
        loaded_images = {}
        # Load regular theme images
        for piece in self.theme_pieces:
            try:
                image_path = f"{piece}.png"
                img = pygame.image.load(image_path).convert_alpha()
                loaded_images[piece] = pygame.transform.scale(img, (self.tile_size, self.tile_size))
            except pygame.error as e:
                print(f"Warning: Could not load regular tile image {image_path}. Error: {e}")
                fallback_surface = pygame.Surface((self.tile_size, self.tile_size))
                fallback_surface.fill(BLACK)
                loaded_images[piece] = fallback_surface

        # Load special tile images
        for special_type, path_base in SPECIAL_TILE_IMAGES.items():
            try:
                image_path = f"{path_base}.png"
                img = pygame.image.load(image_path).convert_alpha()
                loaded_images[special_type] = pygame.transform.scale(img, (self.tile_size, self.tile_size))
            except pygame.error as e:
                print(f"Warning: Could not load special tile image {image_path}. Error: {e}")
                fallback_surface = pygame.Surface((self.tile_size, self.tile_size))
                fallback_surface.fill(LIGHT_GRAY)  # Different fallback for special tiles
                loaded_images[special_type] = fallback_surface
        return loaded_images

    def _create_initial_grid(self):
        while True:
            grid = [[random.choice(self.theme_pieces) for _ in range(self.grid_size)] for _ in range(self.grid_size)]
            if not self.check_match(grid, initial_check=True)[0]:  # Check if any matches exist
                return grid

    def get_piece(self, row, col):
        if 0 <= row < self.grid_size and 0 <= col < self.grid_size:
            return self.grid[row][col]
        return None

    def set_piece(self, row, col, piece_type):
        if 0 <= row < self.grid_size and 0 <= col < self.grid_size:
            self.grid[row][col] = piece_type

    def draw(self, screen, selected_tile=None):
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                x = col * (self.tile_size + self.padding)
                y = row * (self.tile_size + self.padding) + GAME_BOARD_OFFSET_Y
                if selected_tile == (row, col):
                    pygame.draw.rect(screen, SELECTED_COLOR, (x, y, self.tile_size, self.tile_size))
                pygame.draw.rect(screen, BORDER_COLOR, (x, y, self.tile_size, self.tile_size), 1)

                piece = self.grid[row][col]
                if piece is not None and piece in self.images:  # Ensure piece exists in loaded images
                    screen.blit(self.images[piece], (x, y))
                elif piece is not None:
                    # Fallback for unknown piece types (shouldn't happen with proper loading)
                    fallback_surface = pygame.Surface((self.tile_size, self.tile_size))
                    fallback_surface.fill((255, 0, 255))  # Magenta for error
                    screen.blit(fallback_surface, (x, y))

    def check_match(self, current_grid=None, initial_check=False):
        grid_to_check = current_grid if current_grid is not None else self.grid

        matches = set()  # Store all (r, c) of matched tiles
        special_creation_info = []  # List of (pos, type) for special tiles to create

        # Store all detected patterns to prioritize special tile creation
        horiz_4s = []
        vert_4s = []
        horiz_5s = []
        vert_5s = []
        # l_t_shapes = [] # Not implemented in current check_match for creation

        # Check rows for 3-in-a-row and more
        for r in range(self.grid_size):
            for c in range(self.grid_size - 2):
                # Only regular tiles can start a new special tile creation.
                # Special tiles themselves do not form new specials by matching with regular ones.
                if grid_to_check[r][c] is None or grid_to_check[r][c] in ALL_SPECIAL_TILE_TYPES:
                    continue

                if (grid_to_check[r][c] == grid_to_check[r][c + 1] == grid_to_check[r][c + 2]):

                    match_coords = {(r, c), (r, c + 1), (r, c + 2)}

                    # Check for 4-in-a-row horizontal
                    if c + 3 < self.grid_size and grid_to_check[r][c] == grid_to_check[r][c + 3]:
                        match_coords.add((r, c + 3))
                        horiz_4s.append(list(match_coords))

                        # Check for 5-in-a-row horizontal
                        if c + 4 < self.grid_size and grid_to_check[r][c] == grid_to_check[r][c + 4]:
                            match_coords.add((r, c + 4))
                            horiz_5s.append(list(match_coords))

                    matches.update(match_coords)  # Add all found 3+ match coords

        # Check columns for 3-in-a-row and more
        for c in range(self.grid_size):
            for r in range(self.grid_size - 2):
                if grid_to_check[r][c] is None or grid_to_check[r][c] in ALL_SPECIAL_TILE_TYPES:
                    continue

                if (grid_to_check[r][c] == grid_to_check[r + 1][c] == grid_to_check[r + 2][c]):

                    match_coords = {(r, c), (r + 1, c), (r + 2, c)}

                    # Check for 4-in-a-row vertical
                    if r + 3 < self.grid_size and grid_to_check[r][c] == grid_to_check[r + 3][c]:
                        match_coords.add((r + 3, c))
                        vert_4s.append(list(match_coords))

                        # Check for 5-in-a-row vertical
                        if r + 4 < self.grid_size and grid_to_check[r][c] == grid_to_check[r + 4][c]:
                            match_coords.add((r + 4, c))
                            vert_5s.append(list(match_coords))

                    matches.update(match_coords)  # Add all found 3+ match coords

        # Prioritize special tile creation: 5-in-a-row (Color Bomb) > 4-in-a-row (Line Clear)
        # For simplicity, if multiple possible creations, pick the first one found.
        # This will create ONE special tile per match pattern detected.

        if not initial_check:  # Only create special tiles if it's not the initial grid check
            if horiz_5s:
                # The position to create the special tile. Here, picking the center of the 5.
                creation_pos = horiz_5s[0][2]
                special_creation_info = (creation_pos, SPECIAL_COLOR_BOMB_TILE)
            elif vert_5s:
                creation_pos = vert_5s[0][2]
                special_creation_info = (creation_pos, SPECIAL_COLOR_BOMB_TILE)
            elif horiz_4s:
                # Pick a logical spot, e.g., the 2nd tile in the 4-match (0-indexed)
                creation_pos = horiz_4s[0][1]
                special_creation_info = (creation_pos, SPECIAL_H_LINE_TILE)
            elif vert_4s:
                creation_pos = vert_4s[0][1]
                special_creation_info = (creation_pos, SPECIAL_V_LINE_TILE)
            # L/T shape detection and creation for SPECIAL_BOMB_TILE would go here.
            # Example (simplified): if (r,c) is part of a 3-horiz and a 3-vert, create bomb.
            # This requires more complex pattern matching.
            # For now, it will only create color bombs or line clears.
            else:
                special_creation_info = (None, None)  # No special tile to create
        else:
            special_creation_info = (None, None)  # No special tile creation on initial grid check

        return list(matches), special_creation_info

    def remove_tiles(self, tiles_to_remove_set):
        for r, c in tiles_to_remove_set:
            self.grid[r][c] = None

    def drop_pieces(self):
        for col in range(self.grid_size):
            for row in range(self.grid_size - 1, -1, -1):
                if self.grid[row][col] is None:
                    for above_row in range(row - 1, -1, -1):
                        if self.grid[above_row][col] is not None:
                            self.grid[row][col] = self.grid[above_row][col]
                            self.grid[above_row][col] = None
                            break

    def refill_grid(self):
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                if self.grid[row][col] is None:
                    self.grid[row][col] = random.choice(self.theme_pieces)  # Only regular pieces for refilling

    def swap_tiles(self, pos1, pos2):
        self.grid[pos1[0]][pos1[1]], self.grid[pos2[0]][pos2[1]] = \
            self.grid[pos2[0]][pos2[1]], self.grid[pos1[0]][pos1[1]]

    def valid_swap_positions(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1]) == 1

    def has_valid_moves(self):
        temp_grid = copy.deepcopy(self.grid)

        for r in range(self.grid_size):
            for c in range(self.grid_size):
                # Try swapping right
                if c + 1 < self.grid_size:
                    temp_grid[r][c], temp_grid[r][c + 1] = temp_grid[r][c + 1], temp_grid[r][c]
                    if self.check_match(temp_grid, initial_check=True)[0]:  # Check if any matches are formed
                        return True
                    temp_grid[r][c], temp_grid[r][c + 1] = temp_grid[r][c + 1], temp_grid[r][c]  # Swap back

                # Try swapping down
                if r + 1 < self.grid_size:
                    temp_grid[r][c], temp_grid[r + 1][c] = temp_grid[r + 1][c], temp_grid[r][c]
                    if self.check_match(temp_grid, initial_check=True)[0]:  # Check if any matches are formed
                        return True
                    temp_grid[r][c], temp_grid[r + 1][c] = temp_grid[r + 1][c], temp_grid[r][c]  # Swap back
        return False

    def reshuffle_board(self):
        print("No valid moves found, reshuffling board!")
        # Store all existing pieces (excluding Nones)
        existing_pieces = [self.grid[r][c] for r in range(self.grid_size) for c in range(self.grid_size) if
                           self.grid[r][c] is not None]

        # Add enough new random regular pieces to fill the grid if existing aren't enough
        num_missing = self.grid_size * self.grid_size - len(existing_pieces)
        existing_pieces.extend([random.choice(self.theme_pieces) for _ in range(num_missing)])

        random.shuffle(existing_pieces)

        # Ensure the reshuffled board has no initial matches
        while True:
            temp_grid_flat_idx = 0
            new_grid = [[None for _ in range(self.grid_size)] for _ in range(self.grid_size)]

            # Populate new_grid from shuffled existing_pieces
            for r in range(self.grid_size):
                for c in range(self.grid_size):
                    if temp_grid_flat_idx < len(existing_pieces):
                        new_grid[r][c] = existing_pieces[temp_grid_flat_idx]
                        temp_grid_flat_idx += 1
                    else:
                        new_grid[r][c] = random.choice(self.theme_pieces)  # Fallback if not enough pieces

            if not self.check_match(new_grid, initial_check=True)[0]:  # Ensure no matches on reshuffle
                self.grid = new_grid
                break
            random.shuffle(existing_pieces)  # Shuffle again if a match was found

    def get_tiles_to_clear_from_special(self, r, c, target_piece_type=None):
        """
        Calculates which tiles are affected by a special tile's activation.
        Returns a set of (row, col) coordinates to be cleared.
        This method itself does NOT recursively activate other specials it clears,
        that's handled in the Game._handle_tile_swap cascade loop.
        """
        tiles_to_clear_this_activation = set()
        tile_type = self.get_piece(r, c)  # Get the type of the special tile itself

        if tile_type is None or tile_type not in ALL_SPECIAL_TILE_TYPES:
            return tiles_to_clear_this_activation  # Not a special tile or already cleared

        # Add the special tile itself to be cleared
        tiles_to_clear_this_activation.add((r, c))

        if tile_type == SPECIAL_H_LINE_TILE:
            for col_idx in range(self.grid_size):
                tiles_to_clear_this_activation.add((r, col_idx))
        elif tile_type == SPECIAL_V_LINE_TILE:
            for row_idx in range(self.grid_size):
                tiles_to_clear_this_activation.add((row_idx, c))
        elif tile_type == SPECIAL_BOMB_TILE:
            for row_offset in range(-1, 2):
                for col_offset in range(-1, 2):
                    clear_r, clear_c = r + row_offset, c + col_offset
                    if 0 <= clear_r < self.grid_size and 0 <= clear_c < self.grid_size:
                        tiles_to_clear_this_activation.add((clear_r, clear_c))
        elif tile_type == SPECIAL_COLOR_BOMB_TILE:
            color_to_clear = target_piece_type

            # If no target provided (e.g., activated by cascade), or target is also a special tile,
            # then randomly pick a regular piece type from the current board.
            if color_to_clear is None or color_to_clear in ALL_SPECIAL_TILE_TYPES:
                available_regular_pieces_on_board = list(set([self.get_piece(r_idx, c_idx)
                                                              for r_idx in range(self.grid_size)
                                                              for c_idx in range(self.grid_size)
                                                              if self.get_piece(r_idx, c_idx) in self.theme_pieces]))
                if available_regular_pieces_on_board:
                    color_to_clear = random.choice(available_regular_pieces_on_board)
                else:  # No regular pieces left on board, nothing to clear by color
                    color_to_clear = None

            if color_to_clear:
                for row_idx in range(self.grid_size):
                    for col_idx in range(self.grid_size):
                        if self.get_piece(row_idx, col_idx) == color_to_clear:
                            tiles_to_clear_this_activation.add((row_idx, col_idx))
            # If no color to clear (e.g., board empty of regular tiles), it just clears itself (already added)

        return tiles_to_clear_this_activation