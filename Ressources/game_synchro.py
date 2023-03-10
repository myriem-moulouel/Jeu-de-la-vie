import pygame
import time
from .variables import Black, White
import threading

pygame.init()


class Game:

    # Initialisation du jeu
    def __init__(self, n_rows, n_cols, refresh_rate):
        self.display_surface = pygame.display.get_surface()
        self.w = self.display_surface.get_width()
        self.h = self.display_surface.get_height()
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.refresh_rate = refresh_rate

        self.row = self.create_cell(1)
        self.col = self.create_cell(0)

        self.grid_cells = self.create_grid()
        self.grid_neighbors = self.create_grid()

        self.stop_event = threading.Event()
        self.list_thread = [
            [
                threading.Thread(target=self.count_cells, args=(i, j))
                for j in range(self.n_cols)
            ] for i in range(self.n_rows)
        ]

        # +1 car on attends aussi la time barrier
        self.barrier = threading.Barrier((n_rows * n_cols))

    def quit(self):
        self.stop_event.set()
        self.barrier.abort()

    # Indexation des cellules de la grille
    def create_cell(self, cell_type):
        if cell_type:
            if self.n_rows % self.h != 0:
                return (self.h // self.n_rows) + 1
            else:
                return self.h // self.n_rows

        else:
            if self.n_cols % self.w != 0:
                return (self.w // self.n_cols) + 1
            else:
                return self.w // self.n_cols

    # Création de la grille (matrice de 0)
    def create_grid(self):
        return [[0 for _ in range(self.n_cols)] for _ in range(self.n_rows)]

    # Dessiner la grille
    def draw_grid(self):
        self.display_surface.fill(White)

        for row in range(self.n_rows):
            pygame.draw.line(self.display_surface, Black, (0, row * self.row), (self.w, row * self.row))

        for col in range(self.n_cols):
            pygame.draw.line(self.display_surface, Black, (col * self.col, 0), (col * self.col, self.h))

        for row in range(len(self.grid_cells)):
            for col in range(len(self.grid_cells[row])):
                if self.grid_cells[row][col]:
                    Rect = pygame.Rect(col * self.col, row * self.row, self.col, self.row)
                    pygame.draw.rect(self.display_surface, Black, Rect)

    # mettre à jour la grille du nombre de voisins
    def update_grid(self):
        for r in range(self.n_rows):
            for c in range(self.n_cols):
                self.list_thread[r][c].start()

    def count_cells(self, r, c):
        while not self.stop_event.is_set():
            nei = 0
            for i in range(r - 1, r + 2):
                for j in range(c - 1, c + 2):
                    if ((i == r and j == c) or i < 0 or j < 0 or i == len(self.grid_cells) or j == len(self.grid_cells[0])):
                        continue
                    if self.grid_cells[i][j]:
                        nei += 1
            self.grid_neighbors[r][c] = nei
            try:
                self.barrier.wait()
            except threading.BrokenBarrierError:
                return

            if self.grid_cells[r][c]:
                if self.grid_neighbors[r][c] in [2, 3]:
                    self.grid_cells[r][c] = 1
                else:
                    self.grid_cells[r][c] = 0
            else:
                if self.grid_neighbors[r][c] == 3:
                    self.grid_cells[r][c] = 1
                else:
                    self.grid_cells[r][c] = 0
            if self.barrier.n_waiting == self.n_rows * self.n_cols-1:
                time.sleep(self.refresh_rate)
                self.draw_grid()

            try:
                self.barrier.wait()
            except threading.BrokenBarrierError:
                return
