""""
CMSC 495 7384 Capstone in Computer Science (2248)
University of Maryland Global Campus

Group 3: Ronald Parra De Jesus, Anthony Petrowich, Colton Purdy, Kelvin Rubio-Amaya, Asher Russell, Philip Seisman
and Julian Sotelo
Professor Davis

Project File: grid.py
File Description: Creates a grid that will be used to display the tetris game.
"""
import pygame
from color import Color

class Grid:
    def __init__(self,screen_offset):
        """Initializes every variable for the grid."""
        self.total_x = 10
        self.total_y = 20
        self.offset = screen_offset
        self.grid = [[0 for _ in range(self.total_y)] for _ in range(self.total_x)]
        self.cell_size = 40
        self.color = Color.get_color()

    def border_collision(self,x,y):
        """Checks if a cell is outside given grid."""
        if 0 <= x < self.total_x and 0 <= y < self.total_y:
            return True
        return False

    def empty_space(self,x,y):
        """Checks if given x,y is an empty space."""
        if self.grid[x][y] == 0:
            return True
        return False

    def complete_line(self,y):
        """Checks for a complete line on row y."""
        for x in range(self.total_x):
            if self.grid[x][y] == 0:
                return False
        return True

    def delete_row(self,y):
        """Deletes any cells on row y."""
        for x in range(self.total_x):
            self.grid[x][y] = 0

    def move_rows(self,y,rows):
        """Moves row y a total of passed rows down."""
        for x in range(self.total_x):
           self.grid[x][y+rows] = self.grid[x][y]
           self.grid[x][y] = 0

    def clear_rows(self):
        """Clears any rows that are considered complete and
        moves every row down for each complete line.
        """
        complete = 0
        #Checks every row in the grid for complete lines.
        for y in range(self.total_y-1,-1,-1):
            if self.complete_line(y):
                self.delete_row(y)
                complete += 1
            elif complete > 0:
               self.move_rows(y,complete)
        return complete

    def draw(self,screen):
        """Draws the grid onto a passed screen."""
        for x in range(self.total_x):
            for y in range(self.total_y):
                current_cell = self.grid[x][y]
                cell_rect = pygame.Rect(x*self.cell_size + self.offset, y*self.cell_size+ self.offset,
                                        self.cell_size-1,self.cell_size-1)
                pygame.draw.rect(screen,self.color[current_cell], cell_rect)

    def reset(self):
        """Resets grid by emptying every cell."""
        for column in range(self.total_x):
            for row in range(self.total_y):
                self.grid[column][row] = 0
