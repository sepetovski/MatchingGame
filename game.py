import pygame
import time
import json
import random
from board import Board
from constants import *


# Removed: from pygame import mixer

class Game:
    def __init__(self):
        pygame.init()
        # Removed: mixer.init()
        pygame.display.set_caption("Pygame Match-3")

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        self.default_font = pygame.font.Font(pygame.font.get_default_font(), 24)
        self.font26 = pygame.font.Font(pygame.font.get_default_font(), 26)
        self.font32 = pygame.font.Font(pygame.font.get_default_font(), 32)

        self.current_state = GAME_STATE_START
        self.game_mode = MODE_TIME
        self.selected_theme_name = list(THEMES.keys())[0]
        self.selected_theme_pieces = THEMES[self.selected_theme_name]

        self.board = None
        self.score = 0
        self.high_score = self._load_high_score()
        self.total_time = DEFAULT_TIME
        self.moves_left = DEFAULT_MOVES
        self.start_time = 0
        self.selected_tile = None

        # Removed: self._load_sounds()

    # Removed: _load_sounds method
    # Removed: _play_sound method

    def _load_high_score(self):
        try:
            with open(HIGH_SCORE_FILE, 'r') as f:
                return int(f.read())
        except (FileNotFoundError, ValueError):
            return 0

    def _save_high_score(self):
        with open(HIGH_SCORE_FILE, 'w') as f:
            f.write(str(self.high_score))

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self._handle_input(event)

            self._update()
            self._draw()

            self.clock.tick(30)
        pygame.quit()
        self._save_high_score()

    def _handle_input(self, event):
        if self.current_state == GAME_STATE_START:
            self._handle_start_screen_input(event)
        elif self.current_state == GAME_STATE_PLAYING:
            self._handle_game_play_input(event)
        elif self.current_state == GAME_STATE_GAME_OVER:
            self._handle_game_over_input(event)

    def _handle_start_screen_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                self.game_mode = MODE_TIME
            elif event.key == pygame.K_2:
                self.game_mode = MODE_MOVES
            elif event.key == pygame.K_LEFT:
                themes = list(THEMES.keys())
                current_idx = themes.index(self.selected_theme_name)
                self.selected_theme_name = themes[(current_idx - 1) % len(themes)]
                self.selected_theme_pieces = THEMES[self.selected_theme_name]
            elif event.key == pygame.K_RIGHT:
                themes = list(THEMES.keys())
                current_idx = themes.index(self.selected_theme_name)
                self.selected_theme_name = themes[(current_idx + 1) % len(themes)]
                self.selected_theme_pieces = THEMES[self.selected_theme_name]
            elif event.key == pygame.K_RETURN:
                self._start_game()

    def _handle_game_play_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            row, col = (y - GAME_BOARD_OFFSET_Y) // (TILE_SIZE + PADDING), x // (TILE_SIZE + PADDING)

            if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
                if self.selected_tile:
                    if self.board.valid_swap_positions(self.selected_tile, (row, col)):
                        self._handle_tile_swap(self.selected_tile, (row, col))
                        self.selected_tile = None
                    else:
                        self.selected_tile = (row, col)
                else:
                    self.selected_tile = (row, col)

    def _handle_game_over_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.current_state = GAME_STATE_START

    def _start_game(self):
        self.board = Board(self.selected_theme_pieces)
        self.score = 0
        self.total_time = DEFAULT_TIME if self.game_mode == MODE_TIME else 0
        self.moves_left = DEFAULT_MOVES if self.game_mode == MODE_MOVES else 0
        self.start_time = time.time()
        self.selected_tile = None
        self.current_state = GAME_STATE_PLAYING
        # Removed: mixer.music.play(-1)

    def _update(self):
        if self.current_state == GAME_STATE_PLAYING:
            self._update_game_play()

    def _update_game_play(self):
        if self.game_mode == MODE_TIME:
            elapsed_time = int(time.time() - self.start_time)
            remaining = max(0, self.total_time - elapsed_time)
            if remaining == 0:
                self._end_game()
                return
            self.moves_left_or_time = remaining
        else:
            self.moves_left_or_time = self.moves_left
            if self.moves_left <= 0:
                self._end_game()
                return

        if not self.board.has_valid_moves():
            self.board.reshuffle_board()

    def _end_game(self):
        self.high_score = max(self.high_score, self.score)
        self._save_high_score()
        self.current_state = GAME_STATE_GAME_OVER
        # Removed: mixer.music.stop()
        # Removed: self._play_sound("game_over")

    def _draw(self):
        self.screen.fill(MUTED_BLUE)
        if self.current_state == GAME_STATE_START:
            self._draw_start_screen()
        elif self.current_state == GAME_STATE_PLAYING:
            self._draw_game_play()
        elif self.current_state == GAME_STATE_GAME_OVER:
            self._draw_game_over_screen()
        pygame.display.flip()

    def _draw_start_screen(self):
        self._draw_text("Select Game Mode:", self.font32, BLACK, (SCREEN_WIDTH // 2, 50))
        self._draw_text("1. Play with Time", self.font26, BLACK, (SCREEN_WIDTH // 2, 100))
        self._draw_text("2. Play with Moves", self.font26, BLACK, (SCREEN_WIDTH // 2, 150))

        self._draw_text("Select Theme:", self.font32, BLACK, (SCREEN_WIDTH // 2, 300))
        self._draw_text("Left/Right to Change", self.font26, BLACK, (SCREEN_WIDTH // 2, 350))

        self._draw_text(f"Mode: {self.game_mode}", self.default_font, BLACK, (SCREEN_WIDTH - 100, 450))
        self._draw_text(f"Theme: {self.selected_theme_name}", self.default_font, BLACK, (125, 450))

        self._draw_text("Press Enter to Start", self.default_font, BLACK, (SCREEN_WIDTH // 2, 500))

    def _draw_game_play(self):
        self.board.draw(self.screen, self.selected_tile)
        self._draw_score_and_time()

    def _draw_game_over_screen(self):
        self.screen.fill(BLACK)
        self._draw_text("GAME OVER", self.font32, WHITE, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60))
        self._draw_text(f"Your Score: {self.score}", self.default_font, WHITE,
                        (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
        self._draw_text(f"High Score: {self.high_score}", self.default_font, WHITE,
                        (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        self._draw_text("Click to PLAY AGAIN", self.default_font, WHITE, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))

    def _draw_text(self, text, font, color, center):
        render = font.render(text, True, color)
        rect = render.get_rect(center=center)
        self.screen.blit(render, rect)

    def _draw_score_and_time(self):
        pygame.draw.rect(self.screen, LIGHT_GRAY, (0, 0, SCREEN_WIDTH, GAME_BOARD_OFFSET_Y))
        pygame.draw.line(self.screen, BLACK, (0, GAME_BOARD_OFFSET_Y), (SCREEN_WIDTH, GAME_BOARD_OFFSET_Y), 2)
        score_text = self.default_font.render(f"Score: {self.score}", True, SCORE_TEXT_COLOR)
        time_text = self.default_font.render(f"{self.game_mode}: {self.moves_left_or_time}", True, TIME_TEXT_COLOR)
        self.screen.blit(score_text, (20, 30))
        self.screen.blit(time_text, (SCREEN_WIDTH - 120, 30))

    def _handle_tile_swap(self, pos1, pos2):
        # Store original piece types at positions for potential swap-back or color bomb target
        original_piece1_type = self.board.get_piece(pos1[0], pos1[1])
        original_piece2_type = self.board.get_piece(pos2[0], pos2[1])

        # Temporarily perform the swap on the board
        self.board.swap_tiles(pos1, pos2)

        # List of special tiles that *will activate* in this cascade step
        # Each entry: (r, c, target_type_for_color_bomb or None)
        activated_specials_this_round = set()

        # --- Initial Activation Check (direct swap of a special tile) ---
        # Get the types *after* the swap to handle cases where a special tile was newly created
        current_piece1_after_swap = self.board.get_piece(pos1[0], pos1[1])
        current_piece2_after_swap = self.board.get_piece(pos2[0], pos2[1])

        if current_piece1_after_swap in ALL_SPECIAL_TILE_TYPES:
            # If swapped a special with a regular tile, target is the regular tile's type
            target = original_piece2_type if original_piece2_type not in ALL_SPECIAL_TILE_TYPES else None
            activated_specials_this_round.add((pos1[0], pos1[1], target))

        if current_piece2_after_swap in ALL_SPECIAL_TILE_TYPES:
            # If swapped a special with a regular tile, target is the regular tile's type
            target = original_piece1_type if original_piece1_type not in ALL_SPECIAL_TILE_TYPES else None
            activated_specials_this_round.add((pos2[0], pos2[1], target))

        # Get initial matches after swap (regular + potential special creation)
        current_matched_coords, special_creation_data = self.board.check_match()

        # If no immediate matches AND no immediate special activations, it's an invalid swap.
        if not current_matched_coords and not activated_specials_this_round:
            self._animate_shake(pos1, pos2)
            self.board.swap_tiles(pos1, pos2)  # Swap back to original state
            # Removed: self._play_sound("invalid_swap")
            return

        # Valid move: Animate the swap
        # Removed: self._play_sound("swap")
        self._animate_swap(pos1, pos2)

        # Deduct move count for the initial successful swap
        if self.game_mode == MODE_MOVES:
            self.moves_left -= 1

        # --- Main Cascade Loop ---
        while True:
            tiles_to_clear_in_this_cascade_step = set()
            new_special_tiles_to_create = []  # List of (pos, type) for special tiles to be created after drops

            # 1. Process all special tile activations for this step
            if activated_specials_this_round:
                # Removed: self._play_sound("special_activate")
                for r, c, target_type in activated_specials_this_round:
                    # To handle recursive activation (special clears special),
                    # we first get the affected tiles based on the current board state *before* nulling out the special tile.
                    affected_by_this_special = self.board.get_tiles_to_clear_from_special(r, c, target_type)
                    tiles_to_clear_in_this_cascade_step.update(affected_by_this_special)
                    tiles_to_clear_in_this_cascade_step.add((r, c))  # Ensure the special tile itself is cleared
                activated_specials_this_round.clear()  # Processed all activations for this step

            # 2. Add regular matched tiles to the set of tiles to clear
            if current_matched_coords:
                tiles_to_clear_in_this_cascade_step.update(current_matched_coords)
                # If a special tile should be created from these matches
                if special_creation_data[0] is not None:
                    new_special_tiles_to_create.append(special_creation_data)

            # 3. Check for termination condition for cascades
            if not tiles_to_clear_in_this_cascade_step:
                break  # No more tiles to clear from matches or special activations

            # 4. Score update & animation
            self.score += len(tiles_to_clear_in_this_cascade_step) * POINTS_PER_TILE
            if self.game_mode == MODE_TIME:
                self.total_time += BONUS_TIME_PER_MATCH

            # Removed: self._play_sound("match")
            self._animate_removal(list(tiles_to_clear_in_this_cascade_step))

            # 5. Identify new special tiles that will activate by being cleared in THIS step
            specials_cleared_in_this_step_to_activate_next = set()
            for r, c in tiles_to_clear_in_this_cascade_step:
                piece_being_cleared = self.board.get_piece(r, c)
                if piece_being_cleared in ALL_SPECIAL_TILE_TYPES:
                    # If this special tile is being cleared, it should activate its effect in the NEXT cascade step.
                    # For color bombs activated this way, target_type is None, leading to random color clear.
                    specials_cleared_in_this_step_to_activate_next.add((r, c, None))

            # 6. Remove tiles from the board
            self.board.remove_tiles(tiles_to_clear_in_this_cascade_step)

            # 7. Create newly generated special tiles (from previous matches)
            for pos, type_name in new_special_tiles_to_create:
                # Only place if the spot is currently empty (not cleared by another special that activates later)
                if self.board.get_piece(pos[0], pos[1]) is None:
                    self.board.set_piece(pos[0], pos[1], type_name)
                    print(f"Created special tile {type_name} at {pos}")
                else:
                    print(f"Skipped creating {type_name} at {pos}, spot was occupied/cleared.")

            # 8. Drop and Refill
            self.board.drop_pieces()
            self._animate_drop()
            self.board.refill_grid()
            # Removed: self._play_sound("drop") # Re-play drop sound for each cascade

            # 9. Prepare for next iteration: Find new regular matches and add newly activated specials
            current_matched_coords, special_creation_data = self.board.check_match()

            # Add specials that were cleared in THIS step to the set for activation in the NEXT step.
            activated_specials_this_round.update(specials_cleared_in_this_step_to_activate_next)

        # After the cascade loop finishes
        if not self.board.has_valid_moves():
            self.board.reshuffle_board()

    # --- Animation Methods (No changes needed in these, but removed internal sound calls) ---
    def _animate_swap(self, pos1, pos2):
        piece1_name = self.board.get_piece(pos1[0], pos1[1])
        piece2_name = self.board.get_piece(pos2[0], pos2[1])

        # Temporarily swap them back to animate from initial to swapped position
        self.board.swap_tiles(pos1, pos2)  # Swap them back for animation starting point

        x1_start, y1_start = pos1[1] * (TILE_SIZE + PADDING), pos1[0] * (TILE_SIZE + PADDING) + GAME_BOARD_OFFSET_Y
        x2_start, y2_start = pos2[1] * (TILE_SIZE + PADDING), pos2[0] * (TILE_SIZE + PADDING) + GAME_BOARD_OFFSET_Y

        dx = x2_start - x1_start
        dy = y2_start - y1_start

        for i in range(10):
            self.screen.fill(MUTED_BLUE)
            self._draw_game_play()

            current_x1 = x1_start + (dx * i / 10)
            current_y1 = y1_start + (dy * i / 10)
            current_x2 = x2_start - (dx * i / 10)
            current_y2 = y2_start - (dy * i / 10)

            if piece1_name and piece1_name in self.board.images:
                self.screen.blit(self.board.images[piece1_name], (current_x1, current_y1))
            if piece2_name and piece2_name in self.board.images:
                self.screen.blit(self.board.images[piece2_name], (current_x2, current_y2))

            pygame.display.flip()
            pygame.time.delay(ANIM_SWAP_SPEED)

        # After animation, ensure tiles are in their final swapped state
        self.board.swap_tiles(pos1, pos2)  # Swap them *back* to the final state for game logic

    def _animate_shake(self, pos1, pos2):
        shake_offsets = [5, -5, 3, -3, 0]

        for offset in shake_offsets:
            self.screen.fill(MUTED_BLUE)
            self._draw_game_play()

            x1, y1 = pos1[1] * (TILE_SIZE + PADDING), pos1[0] * (TILE_SIZE + PADDING) + GAME_BOARD_OFFSET_Y
            x2, y2 = pos2[1] * (TILE_SIZE + PADDING), pos2[0] * (TILE_SIZE + PADDING) + GAME_BOARD_OFFSET_Y

            piece1_name = self.board.get_piece(pos1[0], pos1[1])
            piece2_name = self.board.get_piece(pos2[0], pos2[1])

            if piece1_name and piece1_name in self.board.images:
                self.screen.blit(self.board.images[piece1_name], (x1 + offset, y1))
            if piece2_name and piece2_name in self.board.images:
                self.screen.blit(self.board.images[piece2_name], (x2 - offset, y2))

            pygame.display.flip()
            pygame.time.delay(ANIM_SHAKE_SPEED)

    def _animate_removal(self, matches):
        fading_surfaces = []
        for r, c in matches:
            x = c * (TILE_SIZE + PADDING)
            y = r * (TILE_SIZE + PADDING) + GAME_BOARD_OFFSET_Y
            piece_name = self.board.get_piece(r, c)
            if piece_name and piece_name in self.board.images:
                fading_surfaces.append((self.board.images[piece_name].copy(), (x, y)))

        for alpha in range(255, 0, -25):
            self.screen.fill(MUTED_BLUE)
            self._draw_game_play()

            for surface, pos in fading_surfaces:
                surface.set_alpha(alpha)
                self.screen.blit(surface, pos)

            pygame.display.flip()
            pygame.time.delay(ANIM_REMOVAL_SPEED)

    def _animate_drop(self):
        for _ in range(3):
            self.screen.fill(MUTED_BLUE)
            self._draw_game_play()
            pygame.display.flip()
            pygame.time.delay(ANIM_DROP_SPEED)
        # Removed: self._play_sound("drop")