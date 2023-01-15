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
        self.time_barrier = threading.Thread(target=self.refresh_barrier)

        # +1 car on attends aussi la time barrier
        self.barrier_nei = threading.Barrier((n_rows * n_cols))
        self.barrier_cell = threading.Barrier((n_rows * n_cols) + 1)

    def quit(self):
        self.stop_event.set()
        self.barrier_nei.abort()
        self.barrier_cell.abort()
        for sub_list in self.list_thread:
            for thread in sub_list:
                thread.join()

    # Bloque pendant self.refresh_rate
    # pour que les frames ne s'enchainent pas trop vite
    def refresh_barrier(self):
        while not self.stop_event.is_set():
            time.sleep(self.refresh_rate)
            try:
                self.barrier_cell.wait()
            except threading.BrokenBarrierError:
                return

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
            pygame.draw.line(self.display_surface, Black, (0, row * self.row),
                             (self.w, row * self.row))

        for col in range(self.n_cols):
            pygame.draw.line(self.display_surface, Black, (col * self.col, 0),
                             (col * self.col, self.h))

        for row in range(len(self.grid_cells)):
            for col in range(len(self.grid_cells[row])):
                if self.grid_cells[row][col]:
                    Rect = pygame.Rect(col * self.col, row * self.row,
                                       self.col, self.row)
                    pygame.draw.rect(self.display_surface, Black, Rect)

    # Mettre une cellule vivante dans la case (i, j)
    def draw_pattern(self, i, j):
        self.grid_cells[i][j] = 1

    # mettre à jour la grille du nombre de voisins
    def update_grid(self):
        for r in range(self.n_rows):
            for c in range(self.n_cols):
                self.list_thread[r][c].start()
        self.time_barrier.start()

    def count_cells(self, r, c):
        while not self.stop_event.is_set():
            nei = 0
            for i in range(r - 1, r + 2):
                for j in range(c - 1, c + 2):
                    if ((i == r and j == c) or i < 0 or j < 0 or
                            i == len(self.grid_cells) or j == len(
                                self.grid_cells[0])):
                        continue
                    if self.grid_cells[i][j]:
                        nei += 1
            self.grid_neighbors[r][c] = nei
            try:
                self.barrier_nei.wait()
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
            if self.barrier_cell.n_waiting == self.n_rows * self.n_cols:
                self.draw_grid()

            try:
                self.barrier_cell.wait()
            except threading.BrokenBarrierError:
                return
