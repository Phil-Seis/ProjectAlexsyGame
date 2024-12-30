""""
CMSC 495 7384 Capstone in Computer Science (2248)
University of Maryland Global Campus

Group 3:Ronald Parra De Jesus, Anthony Petrowich, Colton Purdy, Kelvin Rubio-Amaya, Asher Russell, Philip Seisman
and Julian Sotelo
Professor Davis

Project File: tetris.py
File Description: Manages the main game loop and any additional GUI for each state.
"""

import pygame
import time
from tetris_logic import TetrisLogic

# Initialize Pygame and Pygame Mixer
pygame.init()
pygame.mixer.init()

# Load sounds
pygame.mixer.music.load('8bit-music-for-game-68698.mp3')


# Set up the screen
COLOR = (33, 46, 59)
screen_width, screen_height = 640, 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Tetris: Project Alexey")
clock = pygame.time.Clock()
start_time = 0
elapsed_time = 0



# Load fonts
font_path = 'PressStart2P-Regular.ttf'
try:
    title_font = pygame.font.Font(font_path, 40)  # Larger font for titles
    start_font = pygame.font.Font(font_path, 16)  # Regular size for "Press ENTER to Start"
    timer_font = pygame.font.Font(font_path, 24)  # Smaller size for the timer
    font = pygame.font.Font(font_path, 15)  # Default size
    large_font = pygame.font.Font(font_path, 50)  # Large font for other text
    print("Custom font loaded successfully.")
except FileNotFoundError:
    print(f"Font file not found at: {font_path}. Using default font.")
    title_font = pygame.font.Font(None, 48)
    start_font = pygame.font.Font(None, 36)
    timer_font = pygame.font.Font(None, 24)
    font = pygame.font.Font(None, 15)
    large_font = pygame.font.Font(None, 30)

# Start background music and loop indefinitely
pygame.mixer.music.play(-1)

# Initialize game logic
game_logic = TetrisLogic()
game_state = "TITLE"
normal_drop_speed = 800
fast_drop_speed = 100


def draw_title_screen():
    screen.fill((0,0,0))
    title_text = title_font.render("Project Alexey", True, (50, 205, 50))
    start_text = start_font.render("Press ENTER to Start", True, (255, 255, 255))
    quit_text = start_font.render("Press Q to Quit", True, (255, 255, 255))

    # Font for controls
    controls_font_size = 10
    controls_font = pygame.font.Font(font_path, controls_font_size)

    # Display game controls
    controls_title = controls_font.render("Controls:", True, (255, 255, 255))
    move_text = controls_font.render("A/D | Arrow Left/Arrow Right - Move Left/Right", True, (200, 200, 200))
    rotate_text = controls_font.render("W | Arrow Up - Rotate Right", True, (200, 200, 200))
    drop_text = controls_font.render("S | Arrow Down - Speed Up Drop", True, (200, 200, 200))
    pause_text = controls_font.render("P - Pause", True, (200, 200, 200))

    # Center and display all text
    screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 200))
    screen.blit(start_text, (screen_width // 2 - start_text.get_width() // 2, 300))
    screen.blit(quit_text, (screen_width // 2 - quit_text.get_width() // 2, 350))
    screen.blit(controls_title, (screen_width // 2 - controls_title.get_width() // 2, 450))
    screen.blit(move_text, (screen_width // 2 - move_text.get_width() // 2, 500))
    screen.blit(rotate_text, (screen_width // 2 - rotate_text.get_width() // 2, 550))
    screen.blit(drop_text, (screen_width // 2 - drop_text.get_width() // 2, 600))
    screen.blit(pause_text, (screen_width // 2 - pause_text.get_width() // 2, 650))
    pygame.display.update()


# Main game loop
running = True
while running:
    screen.fill((0, 0, 0))  # Clear the screen for each frame

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle game states and user input
        if game_state == "TITLE":
            if event.type == pygame.KEYDOWN:
                # Start the game
                if event.key == pygame.K_RETURN:
                    game_state = "PLAYING"
                    game_logic.reset_game()
                    start_time = time.time()
                    pygame.time.set_timer(game_logic.AUTO_MOVE, normal_drop_speed)
                # Quit the game
                elif event.key == pygame.K_q:
                    running = False

        elif game_state == "PLAYING":
            elapsed_time = time.time() - start_time
            minutes = int(elapsed_time) // 60
            seconds = int(elapsed_time) % 60
            timer_text = font.render(f"Time: {minutes:02}:{seconds:02}", True, (255, 255, 255))

            # Increase speed every 25 seconds by 25ms without dropping below 150 ms.
            if int(elapsed_time) % 25 == 0 and normal_drop_speed > 150:
                normal_drop_speed -= 25
                pygame.time.set_timer(game_logic.AUTO_MOVE, normal_drop_speed)
            game_logic.auto_move(event)

            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_a, pygame.K_LEFT):
                    game_logic.move_left()
                elif event.key in (pygame.K_d, pygame.K_RIGHT):
                    game_logic.move_right()
                elif event.key in (pygame.K_s, pygame.K_DOWN):
                    pygame.time.set_timer(game_logic.AUTO_MOVE, fast_drop_speed)
                elif event.key in (pygame.K_w, pygame.K_UP):
                    game_logic.rotate_right()
                elif event.key == pygame.K_p:
                    game_state = "PAUSED"
            elif event.type == pygame.KEYUP and event.key in (pygame.K_s, pygame.K_DOWN):
                pygame.time.set_timer(game_logic.AUTO_MOVE, normal_drop_speed)

            # Checks if the game is over
            if game_logic.game_over:
                game_state = "GAME_OVER"
                game_logic.play_sound('game_over_sound','game-over-arcade-6435.mp3')

        elif game_state == "PAUSED":
            # Unpause the game with a 1-second delay.
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                start_time = time.time() - elapsed_time
                game_state = "PLAYING"

        elif game_state == "GAME_OVER":
            if event.type == pygame.KEYDOWN:
                # Restart the game
                if event.key == pygame.K_r:
                    start_time = time.time()
                    normal_drop_speed = 800
                    game_logic.reset_game()
                    game_state = "PLAYING"
                # Quit the game
                elif event.key == pygame.K_q:
                    running = False

    # Displays the relevant game screen based on the current state.
    if game_state == "TITLE":
        draw_title_screen()
    elif game_state == "PLAYING":
        game_logic.draw(screen)

        # Calculate elapsed time and format it
        elapsed_time = time.time() - start_time
        minutes = int(elapsed_time) // 60
        seconds = int(elapsed_time) % 60
        timer_text = font.render(f"Time: {minutes:02}:{seconds:02}", True, (255, 255, 255))

        # Draw the timer in the bottom-right corner
        timer_position = (screen_width - timer_text.get_width() - 10, screen_height - timer_text.get_height() - 10)
        screen.blit(timer_text, timer_position)

    elif game_state == "PAUSED":
        paused_text = font.render("Paused", True, (255, 255, 0))
        unpause_text = font.render("P - Unpause", True, (200, 200, 200))
        screen.blit(paused_text, (screen_width // 2 - paused_text.get_width() // 2, screen_height // 2))
        screen.blit(unpause_text, (screen_width // 2 - unpause_text.get_width() // 2, 500))
    elif game_state == "GAME_OVER":
        # Retrieve scores
        current_score, high_score = game_logic.get_scores()

        # Display Game Over Text
        game_over_text = large_font.render("Game Over", True, (255, 0, 0))
        screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 4))

        # Display Current Score and High Score
        score_text = font.render(f"Your Score: {current_score}", True, (255, 215, 0))
        high_score_text = font.render(f"High Score: {high_score}", True, (255, 69, 0))
        screen.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, screen_height // 2))
        screen.blit(high_score_text, (screen_width // 2 - high_score_text.get_width() // 2, screen_height // 2 + 50))

        # Restart or Quit Instructions
        restart_text = font.render("Press 'R' to Restart or 'Q' to Quit", True, (200, 200, 200))
        screen.blit(restart_text, (screen_width // 2 - restart_text.get_width() // 2, screen_height // 2 + 100))

    pygame.display.flip()  # Refreshes the screen once per loop iteration.

    clock.tick(60)  # Limits the frame rate to 60 FPS.

pygame.quit()
