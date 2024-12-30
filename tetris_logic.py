""""
CMSC 495 7384 Capstone in Computer Science (2248)
University of Maryland Global Campus

Group 3: Ronald Parra De Jesus, Anthony Petrowich, Colton Purdy, Kelvin Rubio-Amaya, Asher Russell, Philip Seisman
and Julian Sotelo
Professor Davis

Project File: tetris_logic.py
File Description: Controls the logic for every feature in the tetris game.
"""
from grid import Grid
from pieces import *
import random
import pygame
import os



def load_high_score():
    """Loads the high score from high_score.txt if it exists."""
    if os.path.exists("high_score.txt"):
        with open("high_score.txt", "r") as file:
            return int(file.read())
    return 0


class TetrisLogic:
    def __init__(self):
        """Initializes every variable the tetris logic."""
        self.grid = Grid(1)
        self.available_pieces = []
        self.current_piece = self.random_piece()
        self.next_piece = self.random_piece()
        self.game_over = False
        self.game_over_sound_played = False
        self.movement = True
        self.current_score = 0
        self.high_score = load_high_score()
        self.sounds = {}
        self.AUTO_MOVE = pygame.USEREVENT + 1  # Custom event for automatic piece movement.
        self.set_auto_move_timer(2000)  # Set initial drop speed to 2000 ms (2 seconds).

    def get_scores(self):
        """Returns the current score and high score."""
        return self.current_score, self.high_score

    def save_high_score(self):
        """Saves the high score to high_score.txt if the current score exceeds it."""
        if self.current_score > self.high_score:
            self.high_score = self.current_score
            with open("high_score.txt", "w") as file:
                file.write(str(self.high_score))

    def play_sound(self,sound_name,file_path):
        """Plays a sound, loading it dynamically if not already loaded."""
        if sound_name not in self.sounds:
            self.sounds[sound_name]=pygame.mixer.Sound(file_path)
        self.sounds[sound_name].play()

    def set_auto_move_timer(self, interval):
        """Sets the interval for the AUTO_MOVE timer."""
        pygame.time.set_timer(self.AUTO_MOVE, interval)  # Set timer for automatic piece movement

    def random_piece(self):
        """Randomly selects a piece to remove from available pieces and returns it."""
        if len(self.available_pieces) == 0:
            self.available_pieces = [IPiece(), JPiece(), LPiece(), OPiece(), SPiece(), TPiece(), ZPiece()]
        piece = random.choice(self.available_pieces)
        self.available_pieces.remove(piece)
        return piece

    def collision(self):
        """Checks for collision of the current piece with the grid borders is True."""
        cells = self.current_piece.get_position()
        for x, y in cells:
            if not self.grid.border_collision(x, y):
                return False
        return True

    def move_left(self):
        """Moves the current piece left if no collision occurs."""
        self.current_piece.move(-1, 0)
        if not self.collision() or not self.empty_space():
            self.current_piece.move(1, 0)

    def move_right(self):
        """Moves the current piece right if no collision occurs."""
        self.current_piece.move(1, 0)
        if not self.collision() or not self.empty_space():
            self.current_piece.move(-1, 0)

    def move_down(self):
        """Moves the current piece down and locks it when it collides with non-empty space."""
        self.current_piece.move(0, 1)
        if not self.collision() or not self.empty_space():
            self.current_piece.move(0, -1)
            self.lock()
            self.play_sound('collision_sound','woosh-230554.mp3')

    def lock(self):
        """Locks the current piece into the grid and checks for row clears."""
        # Lock the piece in current position.
        cells = self.current_piece.get_position()
        for x, y in cells:
            self.grid.grid[x][y] = self.current_piece.piece_type
        self.current_piece = self.next_piece  # Replaces current piece with next piece
        self.next_piece = self.random_piece()  # Replaces next piece with random piece.

        # Checks for cleared rows and updates score if True.
        rows_cleared = self.grid.clear_rows()
        if rows_cleared > 0:
            self.update_score(rows_cleared)
            self.play_sound('line_clear_sound','076833_magic-sfx-for-games-86023.mp3')

        # Check if there's no space for new pieces and updates game over if True.
        if not self.empty_space():
            self.game_over = True
            if not self.game_over_sound_played:
                self.play_sound('game_over_sound','game-over-arcade-6435.mp3')
                self.game_over_sound_played = True
            self.save_high_score()

    def update_score(self, rows_cleared):
        """Updates the score based on the number of rows cleared."""
        points = {1: 100, 2: 300, 3: 500, 4: 800}
        self.current_score += points.get(rows_cleared, 0)

    def empty_space(self):
        """Checks if the current piece has empty space to move into."""
        cells = self.current_piece.get_position()
        for x, y in cells:
            if not self.grid.empty_space(x, y):
                return False
        return True

    def auto_move(self, event):
        """Handles automatic downward movement of the current piece."""
        if event.type == self.AUTO_MOVE and not self.game_over:
            self.move_down()

    def rotate_right(self):
        """Rotates the current piece to the right."""
        self.current_piece.right_rotate()
        if not self.collision() or not self.empty_space():
            self.current_piece.left_rotate()

    def rotate_left(self):
        """Rotates the current piece to the left."""
        self.current_piece.left_rotate()
        if not self.collision() or not self.empty_space():
            self.current_piece.right_rotate()

    def draw_ghost(self, screen):
        """Creates a ghost showing where current piece will drop based on its position."""
        ghost_offset = self.grid.total_y
        ghost_collision = False
        ghost_cells = self.current_piece.get_rotation()
        current_offset = self.current_piece.get_x_offset()

        # Determines y offset for the ghost piece if it collides with the grid or piece.
        for ghost_x, ghost_y in ghost_cells:
            for i in range(self.grid.total_y):
                if (not self.grid.border_collision(ghost_x + current_offset, ghost_y + i)
                        and self.grid.empty_space(ghost_x + current_offset, i)):
                    if not ghost_collision:
                        ghost_offset = i - ghost_y
                if not self.grid.empty_space(ghost_x + current_offset, i):
                    ghost_collision = True
                    if i - (ghost_y + 1) < ghost_offset:
                        ghost_offset = i - (ghost_y + 1)
                    break

        # Draws a ghost piece using ghost offsets.
        for ghost_x, ghost_y in ghost_cells:
            surface = pygame.Surface((self.grid.cell_size, self.grid.cell_size))
            surface.set_alpha(155)
            cell_rect = pygame.Rect((ghost_x + current_offset)
                                    * self.grid.cell_size + self.grid.offset,
                                    (ghost_y + ghost_offset)
                                    * self.grid.cell_size + self.grid.offset,
                                    self.grid.cell_size - 1, self.grid.cell_size - 1)
            surface.fill((92, 97, 102))
            screen.blit(surface, cell_rect)

    def draw_next_piece(self, screen):
        """Draws the next piece preview on the side."""
        # Set the position and size for the next piece preview box.
        next_piece_x = 450
        next_piece_y = 80
        box_width = self.next_piece.cell_size * 3
        box_height = self.next_piece.cell_size * 3
        box_color = (255, 255, 255)

        # Draw the box for the next piece.
        pygame.draw.rect(screen, box_color,
                         pygame.Rect(next_piece_x - 35,
                                     next_piece_y - 10,
                                     box_width + 55,
                                     box_height + 55), 3)

        # Draw the next piece within the box.
        for x, y in self.next_piece.cells[1]:
            pygame.draw.rect(
                screen,
                self.next_piece.color[self.next_piece.piece_type],
                pygame.Rect(
                    next_piece_x + x * self.next_piece.cell_size - 10,
                    next_piece_y + y * self.next_piece.cell_size,
                    self.next_piece.cell_size - 1,
                    self.next_piece.cell_size - 1))

    def draw(self, screen):
        """Draws the main game grid, current piece, and upcoming piece."""
        self.grid.draw(screen)
        self.current_piece.draw(screen)
        self.draw_ghost(screen)
        self.draw_next_piece(screen)
        self.draw_score(screen)

    def draw_score(self, screen):
        """Display current score and high score with customized fonts."""


        # Load fonts
        font_path = 'PressStart2P-Regular.ttf'
        # Load a custom font or fall back to a default one if not found.
        try:
            font = pygame.font.Font(font_path, 13)  # Path to a custom font file.
        except FileNotFoundError:
            font = pygame.font.Font(None, 50)  # Default font with larger size if custom font is not found.

        # Render the score and high score texts with the chosen font.
        score_text = font.render(f"Score: {self.current_score}", True,
                                 (255, 215, 0))  # Gold color for better visibility.
        high_score_text = font.render(f"High Score: {self.high_score}", True, (255, 69, 0))  # Orange-red color.

        # Display the texts on the screen.
        screen.blit(score_text, (10, 10))  # Current score in top-left corner.
        screen.blit(high_score_text, (420, 10))  # High score on the top-right corner.

    def reset_game(self):
        """Resets the game state to start a new game."""
        self.grid = Grid(1)
        self.available_pieces = []
        self.current_piece = self.random_piece()
        self.next_piece = self.random_piece()
        self.game_over = False
        self.current_score = 0
        self.save_high_score()

