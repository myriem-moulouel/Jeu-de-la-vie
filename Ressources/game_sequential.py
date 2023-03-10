import pygame
import time
from .variables import Black, White
import threading

pygame.init()

class Game():

    # Initialisation du jeu
    def __init__(self, n_rows, n_cols):
        self.display_surface = pygame.display.get_surface()
        self.w = self.display_surface.get_width()
        self.h = self.display_surface.get_height()
        self.n_rows = n_rows
        self.n_cols = n_cols

        self.row = self.create_cell(1)
        self.col = self.create_cell(0)

        self.grid_cells = self.create_grid()
        self.grid_neighbors = self.create_grid()

    # Indexation des cellules de la grille
    def create_cell(self, type):
        if type:
            if self.n_rows%self.h != 0:
                return (self.h//self.n_rows)+1
            else:
                return (self.h//self.n_rows)

        else:
            if self.n_cols%self.w != 0:
                return (self.w//self.n_cols)+1
            else:
                return (self.w//self.n_cols)

    # Création de la grille (matrice de 0)
    def create_grid(self):
        return [[0 for i in range(self.n_cols)] for j in range(self.n_rows)]

    # Dessiner la grille
    def draw_grid(self):
        self.display_surface.fill(White)

        for row in range(self.n_rows):
            pygame.draw.line(self.display_surface, Black, (0, row*self.row), (self.w, row*self.row))

        for col in range(self.n_cols):
            pygame.draw.line(self.display_surface, Black, (col*self.col, 0), (col*self.col, self.h))

        for row in range(len(self.grid_cells)):
            for col in range(len(self.grid_cells[row])):
                if self.grid_cells[row][col]:
                    Rect = pygame.Rect( col*self.col, row*self.row, self.col, self.row)
                    pygame.draw.rect(self.display_surface, Black, Rect)

    # Mettre une cellule vivante dans la case (i, j)
    def draw_pattern(self, i, j):
        self.grid_cells[i][j] = 1


    # mettre à jour la grille du nombre de voisins
    def update_grid_neighbors(self):
        def countNeighbors(r,c):
            nei = 0

            for i in range(r-1, r+2):
                for j in range(c-1, c+2):
                    if ((i == r and j == c) or i < 0 or j < 0 or
                        i == len(self.grid_cells) or j == len(self.grid_cells[0])):
                        continue

                    if self.grid_cells[i][j]:
                        nei += 1
            return nei

        for r in range(self.n_rows):
            for c in range(self.n_cols):
                nei = countNeighbors(r,c)
                self.grid_neighbors[r][c] = nei


        

    # Mise-à-jour de la grille de cellules
    def update_grid_cells(self):
        self.update_grid_neighbors()
        
        for r in range(self.n_rows):
            for c in range(self.n_cols):
                if self.grid_cells[r][c]:
                    if self.grid_neighbors[r][c] in [2,3]:
                        self.grid_cells[r][c] = 1
                    else:
                        self.grid_cells[r][c] = 0
                else:
                    if self.grid_neighbors[r][c] == 3:
                        self.grid_cells[r][c] = 1
                    else:
                        self.grid_cells[r][c] = 0
        time.sleep(0.4)
